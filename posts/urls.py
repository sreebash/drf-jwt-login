from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.posts, name='index'),
    path('<int:post_id>/', views.post_details, name='details')
]
