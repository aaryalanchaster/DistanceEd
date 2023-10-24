from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Category, Course


def index(request):
    category_list = Category.objects.all().order_by('id')[:10]
    course_list = Course.objects.order_by('-price')[:5]
    response = HttpResponse(content_type='text/html')
    response.write('<h1>List of Categories:</h1>')

    if category_list:
        response.write('<ul>')
        for category in category_list:
            response.write(f'<li>{category.name}</li>')
        response.write('</ul>')
    else:
        response.write('<p>No categories found.</p>')
        
    response.write('<h1>Top 5 Most Expensive Courses:</h1>')

    if course_list:
        response.write('<ul>')
        for course in course_list:
            response.write(f'<li>{course.title} - Price: ${course.price}</li>')
        response.write('</ul>')
    else:
        response.write('<p>No courses found.</p>')

    return response


def about(request):
    response = HttpResponse(content_type='text/html')
    response.write("<h1>About Us</h1>")
    response.write(
        "<p>This is a Distance Education Website! Search our Categories to find all available Courses.</p>")
    return response


def detail(request, category_no):
    category = get_object_or_404(Category, pk=category_no)
    courses = Course.objects.filter(categories=category)

    response = HttpResponse(content_type='text/html')
    response.write(f'<h1>Category: {category.name}</h1>')

    if courses:
        response.write('<h2>Courses in this Category:</h2>')
        response.write('<ul>')
        for course in courses:
            response.write(f'<li>{course.title} - Price: ${course.price}</li>')
        response.write('</ul>')
    else:
        response.write('<p>No courses found in this category.</p>')

    return response
