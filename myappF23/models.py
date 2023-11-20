# Create your models here.
from django.db import models


class Student(models.Model):
    STUDENT_STATUS_CHOICES = [
        ('ER', 'Enrolled'), ('SP', 'Suspended'), ('GD', 'Graduated'), ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    status = models.CharField(max_length=10, choices=STUDENT_STATUS_CHOICES,
                              default='enrolled')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(max_length=300)
    students = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    COURSE_LEVEL_CHOICE = [
        ('BE', 'Beginner'), ('IN', 'Intermediate'), ('AD', 'Advanced')]
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # level = models.CharField(
    #     max_length=10, choices=COURSE_LEVEL_CHOICE, default='Beginner')
    level = models.PositiveIntegerField(default=0)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (0, 'Order Confirmed'),
        (1, 'Order Cancelled'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    order_date = models.DateField()
    order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    levels = models.PositiveBigIntegerField(default=1)
    
    def __str__(self):
        return f"Order for {self.student} - {self.course} - Status: {self.get_order_status_display()}"

    def discount(self):
        discount_value = 0.10 * float(self.course.price) * float(self.levels)
        self.order_price = float(self.course.price) * float(self.levels) - discount_value
        self.save()
        
    def save(self, *args, **kwargs):
        if self.course.price > 150.0:
            discount_amount = 0.10 * float(self.course.price) * float(self.levels)
            self.order_price = float(self.course.price) * float(self.levels) - discount_amount
        else:
            self.order_price = self.course.price
        super().save(*args, **kwargs)

   