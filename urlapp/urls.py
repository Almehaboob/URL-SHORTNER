from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup_page, name='signup'),
    path('add/', views.add_url, name='add_url'),
    path('list/', views.url_list, name='url_list'),
    path('edit/<int:pk>/', views.edit_url, name='edit_url'),
    path('delete/<int:pk>/', views.delete_url, name='delete_url'),
    path('search/', views.search_url, name='search_url'),
    path('logout/', views.logout_page, name='logout'),
]
