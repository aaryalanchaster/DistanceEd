from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404

from .forms import OrderForm, InterestForm
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


def courses(request):
    course_list = Course.objects.all().order_by('id')
    return render(request, 'myappF23/courses.html', {'courselist':
                                                         course_list})



def place_order(request):
    msg = ''
    courselist = Course.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            # Check if the course price is greater than $150 and call discount() if true
            if order.course.price > 150.00:
                order.discount()

            msg = 'Your course has been ordered successfully.'
            return render(request, 'myappF23/order_response.html', {'msg': msg})
        else:
            msg = 'You exceeded the number of levels for this course.'
    else:
        form = OrderForm()

    return render(request, 'myappF23/placeorder.html', {'form': form, 'msg': msg, 'courselist': courselist})

def coursedetail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    form = InterestForm()

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interested = int(form.cleaned_data['interested'])
            if interested == 1:
                course.interested += 1
                course.save()
                return redirect('index')  # Redirect to the main index page after updating interested count

    return render(request, 'myappF23/coursedetail.html', {'course': course, 'form': form})