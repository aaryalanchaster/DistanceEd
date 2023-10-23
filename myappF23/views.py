from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, Course

# Create your views here.


def index(request):
    category_list = Category.objects.all().order_by('id')[:10]
    course_list = Course.objects.order_by('-price')[:5]
    context = {
        'category_list': category_list,
        'course_list': course_list,
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def detail(request, category_no):
    category = get_object_or_404(Category, pk=category_no)
    courses = Course.objects.filter(categories=category)
    context = {
        'category': category,
        'courses': courses,
    }
    return render(request, 'detail.html', context)
