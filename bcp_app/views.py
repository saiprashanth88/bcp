from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Application
from django.http import JsonResponse
def home(request):
    return render(request,'home.html')
def raw(request):
    return render(request,'raw.html')
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_profile = UserProfile.objects.get(email=email, password=password)
            request.session['user_email'] = email
            return redirect('user_home')
        except UserProfile.DoesNotExist:
            if (email == "saiprashanth817@gmail.com" and password == "12345") or (email == "rajnish123@gmail.com" and password == "12345"):
                request.session['user_email'] = email
                return redirect('raw')
            else:
                error_message = "Invalid email or password. Please try again."
                return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


def user_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        username = request.POST.get('username')
        dob = request.POST.get('dob')
        father_name = request.POST.get('father_name')
        marital_status = request.POST.get('marital_status')
        spouse_name = request.POST.get('spouse_name', '')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile_number = request.POST.get('mobile_number')
        aadhaar_number = request.POST.get('aadhaar_number')
        pancard_number = request.POST.get('pancard_number')
        income = request.POST.get('income')
        house_number = request.POST.get('house_number')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        if UserProfile.objects.filter(pancard_number=pancard_number).exists():
            error_message = "User with this Ration card number already exists, Please Login"
            return render(request, 'user_registration.html', {'error_message': error_message})

        user_profile = UserProfile(
            name=name,
            surname=surname,
            username=username,
            dob=dob,
            father_name=father_name,
            marital_status=marital_status,
            spouse_name=spouse_name,
            gender=gender,
            email=email,
            password=password,
            mobile_number=mobile_number,
            aadhaar_number=aadhaar_number,
            income=income,
            pancard_number=pancard_number,
            house_number=house_number,
            street=street,
            city=city,
            state=state,
            country=country,
            pincode=pincode
        )
        user_profile.save()
        request.session['user_email'] = email
        messages.success(request, 'Registration successful. You can now login.')
        return HttpResponse('Registration successful, Go back and Login')

    return render(request, 'user_registration.html')




def user_home(request):
    user_email = request.session.get('user_email', None)
    if user_email:

        return render(request, "user_home.html", {'user_email': user_email})
    else:
        return redirect('login')

def profile(request):
    user_email = request.session.get('user_email', None)
    if user_email:
        user_profile = UserProfile.objects.get(email=user_email)
        return render(request, 'myprofile.html', {'user_profile': user_profile})
    else:
        return redirect('login')
from django.http import HttpResponse

def apply_yojan(request):
    if request.method == 'POST':
        yojan_name = request.POST.get('name')
        user_email = request.session.get('user_email')
        if user_email:
            user_profile = UserProfile.objects.get(email=user_email)
            if Application.objects.filter(user_profile=user_profile, yojan_name=yojan_name).exists():
                return HttpResponse('You have already applied for this Yojana.', status=400)
            else:
                Application.objects.create(user_profile=user_profile, yojan_name=yojan_name)
                return HttpResponse('Yojana applied successfully!')
        else:
            return HttpResponse('User not logged in.', status=401)
    else:
        return HttpResponse('Invalid request method.', status=405)


def user_applications(request):
    user_email = request.session.get('user_email')
    if user_email:
        user_profile = UserProfile.objects.get(email=user_email)
        applications = Application.objects.filter(user_profile=user_profile)
        return render(request, 'user_applications.html', {'applications': applications})
    else:
        return redirect('login')
def admin_applications(request):
    applications = Application.objects.filter(acknowledge=False).select_related('user_profile')
    return render(request, 'admin_applications.html', {'applications': applications})

def accept_application(request, application_id):
    if request.method == 'POST':
        application = Application.objects.get(id=application_id)
        application.acknowledge = True
        application.accepted = True
        application.save()
        return redirect('admin_applications')
    else:
        return HttpResponse(status=405)

def reject_application(request, application_id):
    if request.method == 'POST':
        application = Application.objects.get(id=application_id)
        application.acknowledge = True
        application.accepted = False
        application.save()
        return redirect('admin_applications')
    else:
        return HttpResponse(status=405)

def contact(request):
    return render(request, 'contact.html')
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
    text = text.replace('•', ' *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


genai.configure(api_key="AIzaSyCzLk7mX5JdNa9QaPMoMV64lwLLFdV0TMY")
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def home(request):
    return render(request, 'home.html')

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        botresponse = chat.send_message(f"If the user asks any question related to how to apply the yojana, then simply give an answer: Firstly login to your account and make sure to open the home page. There you can see the yojanas and simply click on apply. In this manner, you have to respond. If the user asks any other query, then respond optimally. The user's query is: {message}")
        response = {
            'message': botresponse
        }
        return JsonResponse({'message': response})
    return JsonResponse({})

