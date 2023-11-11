from django.urls import path
from myappF23 import views

app_name = 'myappF23'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('<int:category_no>/', views.detail, name='detail'),
    path('instructor/<int:instructor_id>/',
         views.instructor, name='instructor'),
    path('courses/', views.courses, name='courses'),
    path('place_order/', views.place_order, name='place_order'),
    path('courses/<int:course_id>/', views.coursedetail, name='coursedetail'),

]
