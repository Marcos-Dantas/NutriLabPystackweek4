from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.patients, name='patients'),
    path('patient-info-list/', views.patient_info_list, name="patient_info_list"),
    path('patient/<str:id>/', views.patient_information, name="patient_information"),
    path('data-graph/<str:id>/', views.data_graph, name="data_graph"),
    path('food-plan-list/', views.food_plan_list, name="food_plan_list"),
    path('food-plan/<str:id>/', views.food_plan, name="food_plan"),
    path('meal/<str:id_patient>/', views.meal, name="meal"),
    path('option/<str:id_patient>/', views.option, name="option"),
    path('generate-meals-pdf/<str:id_patient>/', views.generate_meals_pdf, name="generate_meals_pdf")

]