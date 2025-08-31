from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('apply/<int:internship_id>/', views.apply_internship, name='apply_internship'),
    path('applied-internships/', views.applied_internships, name='applied_internships'),
    path('progress/',views.progress, name='progress'),
    path('user/dashboard', views.login_page, name='home'),
]

handler403 = 'webapp.views.custom_permission_denied_view'

