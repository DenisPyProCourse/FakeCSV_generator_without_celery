from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from schemas.views import ListSchemaView, CreateSchemaView, UpdateSchemaView, DeleteSchemaView, DetailScemaView, \
    run_task # get_status


app_name = 'schemas'

urlpatterns = [
    path('', ListSchemaView.as_view(), name='list'),
    path('create/', CreateSchemaView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateSchemaView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteSchemaView.as_view(), name='delete'),
    path('detail/<int:pk>/', DetailScemaView.as_view(), name='detail'),
    # path('tasks/<task_id>/', get_status, name='get_status'),
    path('tasks/', run_task, name='run_task'),
 ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
