from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.patients, name='patients'),
    path('patient-info-list/', views.patient_info_list, name="patient_info_list"),
    path('patient/<str:id>/', views.patient_information, name="patient_information"),
    path('weight-graph/<str:id>/', views.weight_graph, name="weight_graph")


]