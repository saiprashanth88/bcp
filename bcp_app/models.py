from django.db import models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User



from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    dob = models.DateField()
    father_name = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=20, choices=[('single', 'Single'), ('married', 'Married')])
    spouse_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    email = models.EmailField()
    password = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    aadhaar_number = models.CharField(max_length=20)
    pancard_number = models.CharField(max_length=20)
    income = models.CharField(max_length=20,null=True)
    house_number = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    unique_id = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.aadhaar_number and self.pancard_number:
            unique_id = self.aadhaar_number[:5] + self.pancard_number[:5]
            self.unique_id = unique_id
        super().save(*args, **kwargs)
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    dob = forms.DateField()
    father_name = forms.CharField(max_length=100)
    marital_status = forms.ChoiceField(choices=[('single', 'Single'), ('married', 'Married')])
    spouse_name = forms.CharField(max_length=100, required=False)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    email = forms.EmailField()
    mobile_number = forms.CharField(max_length=20)
    aadhaar_number = forms.CharField(max_length=20)
    pancard_number = forms.CharField(max_length=20)
    income = models.CharField(max_length=20,null=True)
    house_number = forms.CharField(max_length=100)
    street = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'surname', 'dob', 'father_name',
                  'marital_status', 'spouse_name', 'gender', 'email', 'mobile_number',
                  'aadhaar_number', 'pancard_number', 'house_number', 'street', 'city',
                  'state', 'country', 'pincode']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                surname=self.cleaned_data['surname'],
                dob=self.cleaned_data['dob'],
                father_name=self.cleaned_data['father_name'],
                marital_status=self.cleaned_data['marital_status'],
                spouse_name=self.cleaned_data.get('spouse_name', ''),
                gender=self.cleaned_data['gender'],
                email=self.cleaned_data['email'],
                mobile_number=self.cleaned_data['mobile_number'],
                aadhaar_number=self.cleaned_data['aadhaar_number'],
                pancard_number=self.cleaned_data['pancard_number'],
                house_number=self.cleaned_data['house_number'],
                street=self.cleaned_data['street'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                country=self.cleaned_data['country'],
                pincode=self.cleaned_data['pincode']
            )
        return user

class Application(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    yojan_name = models.CharField(max_length=100)
    application_date = models.DateTimeField(auto_now_add=True)
    acknowledge = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_profile.username} - {self.yojan_name}"
