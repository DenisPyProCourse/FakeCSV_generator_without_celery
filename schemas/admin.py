from django.contrib import admin
from .models import Schema, Columns, DataSet


admin.site.register(Schema)
admin.site.register(Columns)
admin.site.register(DataSet)
