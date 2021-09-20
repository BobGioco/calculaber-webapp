from django.urls import path
from calculaber_app import views

app_name='calculaber_app'

urlpatterns = [
    path('',views.index,name='index'),
    path('info/',views.account_info,name='account_info'),
    path('material/',views.MaterialListView.as_view(),name='material_list'),
    #path('sensorlist/',views.SensorListView.as_view(),name='sensor_list'),
]
