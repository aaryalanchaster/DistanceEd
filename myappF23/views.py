from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Category, Course, Instructor

# Create your views here.


def index(request):
    category_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'myappF23/index.html', {'category_list': category_list})


def about(request):
    return render(request, "myappF23/about.html")


def detail(request, category_no):
    category = get_object_or_404(Category, pk=category_no)
    courses = Course.objects.filter(categories=category)

    context = {
        'category': category,
        'courses': courses,
    }

    return render(request, 'myappF23/detail.html', context)


def instructor(request, instructor_id):
    instructor = Instructor.objects.get(pk=instructor_id)
    courses_taught = instructor.course_set.all()
    students = instructor.students.all()

    context = {
        'instructor': instructor,
        'courses_taught': courses_taught,
        'students': students,
    }

    return render(request, 'myappF23/instructor0.html', context)
