from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include
from calculaber_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('calculaber_app.urls')),
    path('',include('users_app.urls')),
    path('project/<int:pk>/detail/',views.ProjectDetailView.as_view(),name='project_detail'),
    path('project/<int:pk>/delete/',views.ProjectDeleteView.as_view(),name='project_delete'),
    path('project/<int:pk1>/detail/<int:pk2>/',views.ObjectDetailView.as_view(),name='object_detail'),
    path('project/<int:pk>/detail/extra_expense/',views.ExtraExpenseDetailView.as_view(),name='extra_expense_detail'),
    path('extra_expense/<int:pk>/delete',views.ExtraExpenseDeleteView.as_view(),name='extra_expense_delete'),
    path('object/<int:pk>/delete',views.ObjectDeleteView.as_view(),name='object_delete'),
    path('material/<int:pk>/delete/',views.MaterialDeleteView.as_view(),name='material_delete'),
    path('material_object/<int:pk>/delete/',views.MaterialObjectDeleteView.as_view(),name='material_object_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
