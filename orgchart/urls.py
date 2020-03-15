from django.urls import path
from . import views

urlpatterns = [
    path('',views.tree,name='tree'),
    path('employee_detail/<int:idi>/', views.employee_detail, name='employee_detail'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('search_name/',views.search_name,name='search_name'),
    path('search_location/',views.search_location,name='search_location'),
    path('search_id/',views.search_id,name='search_id'),
    path('delete_employee/',views.delete_employee,name='delete_employee'),
    path('detail_edit/<int:pk>/',views.detail_edit,name='detail_edit'),
    path('contact/',views.contact,name='contact')
]