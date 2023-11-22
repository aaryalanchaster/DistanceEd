from django.urls import path
from myappF23 import views

app_name = 'myappF23'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('<int:category_no>/', views.detail, name='detail'),
    path('instructor/<int:instructor_id>/', views.instructor, name='instructor'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('place_order/', views.place_order, name='place_order'),
    path('courses/<int:course_id>/', views.coursedetail, name='coursedetail'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('set_cookie/', views.set_cookie, name='set_cookie'),
    path('check_cookie/', views.check_cookie, name='check_cookie'),
    path('delete_cookie/', views.delete_cookie, name='delete_cookie'),

]
