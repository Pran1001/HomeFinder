from django.urls import path
from . import views
from .views import account_verify

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('account_verify/<slug:token>', account_verify, name='account_verify'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('agents_grid/', views.agents_grid, name='agents_grid'),
    path('agent_single/<int:pk>/', views.agent_single, name='agent_single'),
    path('property_grid/', views.property_grid, name='property_grid'),
    path('property_grid_search/', views.property_grid_search, name='property_grid_search'),
    path('property_single/<int:pk>/', views.property_single, name='property_single'),
    path('post_property/', views.post_property, name='post_property'),
    path("password_reset/", views.password_reset_request, name="password_reset"),

]
