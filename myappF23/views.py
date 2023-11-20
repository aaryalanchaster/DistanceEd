from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .forms import OrderForm, InterestForm
from .models import Category, Course, Instructor, Order

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    category_list = Category.objects.all().order_by('id')[:10]
    visits = request.COOKIES.get('user_visits', 0)
    visits = int(visits) + 1

    # Set the 'user_visits' cookie with the updated count and expiration time
    expiration_time = timezone.now() + timedelta(minutes=5)

    last_login_info = request.session.get('last_login_info')

    if last_login_info:
        # Check if the last login is more than one hour ago
        last_login_time = timezone.datetime.strptime(last_login_info, "%Y-%m-%d %H:%M:%S")
        one_hour_ago = timezone.now() - timezone.timedelta(hours=1)

        if last_login_time >= one_hour_ago:
            message = f"Last Login: {last_login_info}"
        else:
            message = "Your last login was more than one hour ago."
    else:
        message = "You haven't logged in yet."

    # Set the 'user_visits' cookie with the updated count
    response = render(request, 'myappF23/index.html', {'visits': visits,
                                                       'category_list': category_list, 'message': message})
    response.set_cookie('user_visits', visits, expires=expiration_time)

    return response


def about(request):
    visits = request.COOKIES.get('user_visits', 0)
    return render(request, "myappF23/about.html", {'visits': visits})


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

            if int(order.levels) > int(order.course.level):
                order.delete()
                msg = 'You exceeded the number of levels for this course.'
                return render(request, 'myappF23/order_response.html', {'msg': msg})
            # Check if the course price is greater than $150 and call discount() if true
            if order.course.price > 150.00:
                order.discount()

            msg = 'Your course has been ordered successfully.'
            return render(request, 'myappF23/order_response.html', {'msg': msg})

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
                return redirect('myappF23:index')  # Redirect to the main index page after updating interested count

    return render(request, 'myappF23/coursedetail.html', {'course': course, 'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                current_login_info = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

                # Store this value as a session parameter (last_login_info)
                request.session['last_login_info'] = current_login_info

                # Set the session expiry to 1 hour (3600 seconds)
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myappF23:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myappF23/login.html')


@login_required
def user_logout(request):
    logout(request)
    request.session.flush()

    return HttpResponseRedirect(reverse('myappF23:index'))


@login_required
def myaccount(request):
    user = request.user
    if hasattr(user, 'student'):
        student = user.student
        orders = Order.objects.filter(student=student)
        interested_courses = student.course_set.all()
        return render(request, 'myappF23/myaccount.html',
                      {'student': student, 'orders': orders, 'interested_courses': interested_courses})
    else:
        return HttpResponse('You are not a registered student!')


def set_cookie(request):
    response = HttpResponse("Setting test cookie.")
    response.set_cookie('test_cookie', 'cookie_value')
    return response


# Example view to check if the test cookie worked
def check_cookie(request):
    if 'test_cookie' in request.COOKIES:
        return HttpResponse("Test cookie is working.")
    else:
        return HttpResponse("Test cookie is not set.")


# Example view to delete the test cookie
def delete_cookie(request):
    response = HttpResponse("Deleting test cookie.")
    response.delete_cookie('test_cookie')
    return response

