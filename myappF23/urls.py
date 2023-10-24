from django.urls import path
from myappF23 import views

app_name = 'myappF23'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('<int:category_no>/', views.detail, name='detail'),
    path('instructor/<int:instructor_id>/',
         views.instructor, name='instructor'),
]
