from django.urls import path

from . import views

app_name = 'subscription'
urlpatterns = [
    path('', views.PlanListView.as_view(), name='plans'),
]
