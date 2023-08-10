from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms import DateInput
from datetime import date


class CustomInput(forms.widgets.Input):
    def render(self, name, value, attrs=None, renderer=None):
        span_html = '<span class="input-group-text bg-transparent"><i class="ti-{icon}"></i></span>'.format(icon=self.attrs.get('icon', 'user'))
        input_html = super().render(name, value, attrs=attrs, renderer=renderer)
        return f'<div class="form-group"><div class="input-group mb-3">{span_html}{input_html}</div></div>'
    

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        widget=CustomInput(attrs={'class': 'form-control ps-15 bg-transparent', 'type': 'text', 'placeholder': 'Username', 'icon': 'user'})
    )
    first_name = forms.CharField(
        label='First name',
        widget=CustomInput(attrs={'class': 'form-control ps-15 bg-transparent', 'type': 'text', 'placeholder': 'First name', 'icon': 'user'})
    )
    last_name = forms.CharField(
        label='Last name',
        widget=CustomInput(attrs={'class': 'form-control ps-15 bg-transparent', 'type': 'text', 'placeholder': 'Last name', 'icon': 'user'})
    )
    email = forms.CharField(
        label='Email',
        widget=CustomInput(attrs={'class': 'form-control ps-15 bg-transparent', 'type': 'text', 'placeholder': 'Email', 'icon': 'email'})
    )
    password = forms.CharField(
        label='Password',
        widget=CustomInput(attrs={'class': 'form-control ps-15 bg-transparent', 'type': 'password', 'placeholder': 'Password', 'icon': 'lock'})
    )
    password2 = forms.CharField(
        label='Retype password',
        widget=CustomInput(attrs={'class': 'form-control ps-15 bg-transparent', 'type': 'password', 'placeholder': 'Retype password', 'icon': 'lock'})
    )
   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    

class ActivityForm(forms.ModelForm):
    name = forms.CharField(
        label='Add new Activity',
        widget=CustomInput(attrs={'class': 'form-control ps-15 bg-transparent', 'type': 'text', 'placeholder': 'Enter value', 'icon': 'text'})
    )
    class Meta:
        model = models.Activities
        fields = ('name',)


class FacilityForm(forms.ModelForm):
    name = forms.CharField(
        label='Add new Facility',
        widget=CustomInput(attrs={'class': 'form-control ps-15 bg-transparent', 'type': 'text', 'placeholder': 'Enter value', 'icon': 'text'})
    )
    class Meta:
        model = models.Facilities
        fields = ('name',)


class WorkLogForm(forms.ModelForm):
    date = forms.DateField(
        label='Date',
        widget=DateInput(attrs={'class': 'form-control ps-15 bg-transparent', 'style': 'width: 150px;', 'type': 'date', 'placeholder': 'Enter value'}),
        initial=date.today(),
        input_formats=['%Y-%m-%d']
    )
    volume = forms.DecimalField(
        label='Volume',
        widget=forms.NumberInput(attrs={'class': 'form-control ps-15 bg-transparent', 'style': 'width: 150px;', 'type': 'number', 'placeholder': 'Enter value', 'step': 'any'})
    )
    hours_worked = forms.DecimalField(
        label='Hours Worked',
        widget=forms.NumberInput(attrs={'class': 'form-control ps-15 bg-transparent', 'style': 'width: 150px;', 'type': 'number', 'placeholder': 'Enter value', 'step': 'any'})
    )
    earned_hours = forms.DecimalField(
        label='Earned Hours',
        widget=forms.NumberInput(attrs={'class': 'form-control ps-15 bg-transparent', 'style': 'width: 150px;', 'type': 'number', 'placeholder': 'Enter value', 'step': 'any'})
    )
    pgl = forms.DecimalField(
        label='PGL',
        widget=forms.NumberInput(attrs={'class': 'form-control ps-15 bg-transparent', 'style': 'width: 150px;', 'type': 'number', 'placeholder': 'Enter value', 'step': 'any'})
    )
    comments = forms.CharField(
        label='Comments',
        widget=forms.Textarea(attrs={'class': 'form-control ps-15 bg-transparent', 'placeholder': 'Enter comments'}),
        required=False, 
    )

    class Meta:
        model = models.Worklog
        fields = ('date','volume','hours_worked','comments','earned_hours','pgl')