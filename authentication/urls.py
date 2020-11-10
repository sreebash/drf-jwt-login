from django.urls import path
from authentication import views
app_name = 'authentication'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('api/register/', views.RegisterApiView.as_view()),

]
