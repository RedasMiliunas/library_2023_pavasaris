from django import forms
from .models import BookReview, Profile, BookInstance
from django.contrib.auth.models import User


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['content']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class DateInput(forms.DateInput):
    input_type = 'date'

# Dėmesio: jei lauke norite nustatyti DateTime lauką,
# tai yra ir datą ir laiką, DateInput klasėje input_type reikšmę
# pakeiskite iš 'date' į "datetime-local".

class InstanceCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'due_back']
        widgets = {'due_back': DateInput()}