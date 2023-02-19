import time
from celery.result import AsyncResult
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from schemas.forms import UserRegistrationForm, SchemaCreateForm, ColumnsFormSet, SchemaFilterForm, \
    DatasetCreateForm
from schemas.models import Schema, Columns, DataSet
from schemas.tasks import create_csv


def index(request):
    """
    Home page
    """
    return render(
        request,
        'core/index.html',
        {'title': 'FakeCSV', 'Welcome': 'Welcome to FakeCSV!'}
    )


class AccountRegistrationView(CreateView):
    """
    Simple registration view for new users
    """
    model = User
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('index')
    form_class = UserRegistrationForm


class AccountLoginView(LoginView):
    """
    Simple login view
    """
    template_name = 'accounts/login.html'

    def get_redirect_url(self):
        """
        :return: Redirect to home page
        """
        next_value = self.request.GET.get('next')
        if next_value:
            return next_value

        return reverse('index')

    def form_valid(self, form):
        """
        :param form: form based on django User model. Located in .forms.py
        :return: valid form + message about successful login
        """
        response = super().form_valid(form)
        messages.success(self.request, f'User <{self.request.user}> has successfully logged in.')
        return response


class AccountLogoutView(LoginRequiredMixin, LogoutView):

    template_name = 'accounts/logout.html'


class ListSchemaView(LoginRequiredMixin, ListView):
    """
    List of schemas worked by FilterForm from forms.py.
    Each user see only his schemas.
    Using filter for corresct search with pagination.
    """
    model = Schema
    template_name = 'schema/list.html'
    paginate_by = 7

    def get_filter(self):
        return SchemaFilterForm(
            data=self.request.GET,
            queryset=self.model.objects.filter(author_id=self.request.user.id))

    def get_queryset(self):

        return self.get_filter().qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.get_filter().form

        return context


class DetailScemaView(LoginRequiredMixin, DetailView):
    """
    Detail view for schems.
    Instantly creat Datasets
    """
    model = Schema
    template_name = 'schema/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailScemaView, self).get_context_data(**kwargs)
        context['column'] = Columns.objects.filter(schem_id=self.object.id).select_related()
        context['datasets'] = DataSet.objects.filter(schema_id=self.object.id).select_related()
        if self.request.POST:
            context['create_dataset'] = DatasetCreateForm(self.request.POST)
        else:
            context['create_dataset'] = DatasetCreateForm()
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        time.sleep(3)
        return HttpResponseRedirect(
            reverse("schemas:detail", kwargs={"pk": self.get_object().pk})
        )


class CreateSchemaView(LoginRequiredMixin, CreateView):
    """
    Create Schema
    Using here inline formset from .form.py.
    It helps to show both forms for Schema and Columns for this schema correctly.
    Made custom layout object for crispy: Formset and use django-dynamic-formset jQuery plugin which help add more rows.
    """
    model = Schema
    form_class = SchemaCreateForm
    success_url = None
    template_name = 'schema/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateSchemaView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['columns'] = ColumnsFormSet(self.request.POST)
        else:
            context['columns'] = ColumnsFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['columns']
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()
            if columns.is_valid():
                columns.instance = self.object
                columns.save()
        return super(CreateSchemaView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('schemas:list')


class UpdateSchemaView(LoginRequiredMixin, UpdateView):
    """
    Updated Schema
    The similar logic as in create view.
    """
    model = Schema
    success_url = None
    template_name = 'schema/update.html'
    form_class = SchemaCreateForm

    def get_context_data(self, **kwargs):
        context = super(UpdateSchemaView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['columns'] = ColumnsFormSet(self.request.POST, instance=self.object)
        else:
            context['columns'] = ColumnsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['columns']
        with transaction.atomic():
            self.object = form.save()
            if columns.is_valid():
                columns.instance = self.object
                columns.save()
        return super(UpdateSchemaView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('schemas:list')


class DeleteSchemaView(LoginRequiredMixin, DeleteView):
    model = Schema
    success_url = reverse_lazy('schemas:list')
    template_name = 'schema/delete.html'


@csrf_exempt
def run_task(request):
    """
    Send an AJAX request to the server to generate the csv file with celery (status.js)
    :return: JsonResponse with data for get_status view
    """

    if request.POST:
        task_type = int(request.POST.get("ds"))
        rows = int(request.POST.get("rows"))
        task = create_csv.delay(schem=str(task_type), rows=rows)
        return JsonResponse({"task_id": task.id}, status=202, safe=False)


@csrf_exempt
def get_status(request, task_id):
    """
    Show a colored label of generation status for each dataset (processing/ready) on frontend.
    :param task_id: get it from run_task view
    :return: JsonResponse with celery task status id.
    """
    if request.method == 'GET':
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": '' if task_result.result is None else str(task_result.result)
        }
        return JsonResponse(result, status=200, safe=False)
