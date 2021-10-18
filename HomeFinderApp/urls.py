from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('agents_grid/', views.agents_grid, name='agents_grid'),
    path('agent_single/', views.agent_single, name='agent_single'),
    path('property_grid/', views.property_grid, name='property_grid'),
    path('property_single/', views.property_single, name='property_single'),
    path('post_property/', views.post_property, name='post_property'),
    path("password_reset/", views.password_reset_request, name="password_reset"),

]
