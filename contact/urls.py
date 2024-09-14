from contact import views
from django.urls import path

app_name = 'contact'

urlpatterns = [
    path('', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.user_logout, name='logout'),
    path('account/', views.account, name='account'),
    path('account_update/', views.account_update, name='account_update'),
    path('account_delete/', views.account_delete, name='account_delete'),
    path('password_reset/', views.password_reset, name='password_reset'),




    path('index/', views.index, name='index'),
    path('my_contact/', views.my_contact, name='my_contact'),
    path('search/', views.search, name='search'),

    path('contact/<int:contact_id>/', views.contact, name='contact'),
    path('contact/create/', views.create, name='create'),
    path('contact/<int:contact_id>/update/', views.update, name='update'),
    path('contact/<int:contact_id>/delete/', views.delete, name='delete'),





]
