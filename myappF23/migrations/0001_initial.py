# Generated by Django 4.2.6 on 2023-11-22 23:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('level', models.PositiveIntegerField(default=0)),
                ('interested', models.PositiveIntegerField(default=0)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myappF23.category')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('date_of_birth', models.DateField()),
                ('status', models.CharField(choices=[('ER', 'Enrolled'), ('SP', 'Suspended'), ('GD', 'Graduated')], default='enrolled', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.IntegerField(choices=[(0, 'Order Confirmed'), (1, 'Order Cancelled')], default=1)),
                ('order_date', models.DateField()),
                ('order_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('levels', models.PositiveBigIntegerField(default=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myappF23.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myappF23.student')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('bio', models.TextField(max_length=300)),
                ('students', models.ManyToManyField(blank=True, to='myappF23.student')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myappF23.instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='interested_students',
            field=models.ManyToManyField(blank=True, related_name='interested_students', to='myappF23.student'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, to='myappF23.student'),
        ),
    ]
