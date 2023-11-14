from django import forms
from django.forms import RadioSelect, SelectDateWidget, ModelForm

from myappF23.models import Order


class InterestForm(forms.Form):

    INTEREST_CHOICES = [
        (1, 'Yes'),
        (0, 'No'),
    ]

    interested = forms.ChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )

    levels = forms.IntegerField(
        initial=1,
        min_value=1
    )

    comments = forms.CharField(
        widget=forms.Textarea(attrs={'label': 'Additional Comments'}),
        required=False
    )

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['student', 'course', 'levels', 'order_date']

        widgets = {
            'student': RadioSelect,
            'order_date': SelectDateWidget,
        }