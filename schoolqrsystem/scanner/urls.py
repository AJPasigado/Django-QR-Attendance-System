from django.urls import re_path

from . import views

app_name = 'scanner'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path('logs', views.logs, name='logs'),
    re_path('add', views.add, name='add'),
    re_path('generator', views.generator, name='generator'),
    re_path('export', views.export, name='export'),
]
