from django.contrib import messages, auth
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms import *
from .models import *


def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'index.html',context)


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Invalid Credentials ! ! !')
                return redirect('signin')
    return render(request, 'signin.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = AccountForm()
        user_form = UserForm()
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            form = AccountForm(request.POST, request.FILES)
            if user_form.errors:
                message = user_form.errors
                messages.info(request, message)
                return redirect('register')
            if form.errors:
                message = form.errors
                messages.info(request, message)
                return redirect('register')
            if form.is_valid() and user_form.is_valid():
                user_form.save()
                form.save()
                return redirect('signin')
        context = {'form': form, 'user_form': user_form}
        return render(request, 'register.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = name + "-" + form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['mailtohomefinder@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.info(request, 'Your message has been sent. Thank you for Connecting with us :)')
    return render(request, "contact.html", {'form': form})


def agent_single(request):
    if request.user.is_authenticated:
        return render(request, 'agent_single.html')
    else:
        return render(request, 'signin.html')


def agents_grid(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, 'agents_grid.html',context)
    else:
        return render(request, 'signin.html')


def property_grid(request):
    posts = Post.objects.all()
    context = {'posts' : posts}
    return render(request, 'property_grid.html', context)


def property_single(request):
    if request.user.is_authenticated:
        return render(request, 'property_single.html')
    else:
        return render(request, 'signin.html')


def post_property(request):
    form = PostForm()
    username = request.user.username
    user_obj = User.objects.get(username=username)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.errors:
            message = form.errors
            messages.info(request, message)
            return redirect('post_property')
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.user = user_obj
            post_form.save()
            messages.info(request, 'Property Posted Successfully.')
            return redirect('post_property')
    property = Post.objects.all()
    context = {'form': form, 'property': property}
    return render(request, 'post_property.html', context)


def about(request):
    return render(request, 'about.html')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "PasswordResetEmail.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'HomeFinder',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'mailtohomefinder@gmail.com', [user.email])
                        return redirect("password_reset_done")
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
            else:
                messages.info(request, "User with this email Id doesn't exists")
                return redirect('password_reset')

    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html",
                  context={"password_reset_form": password_reset_form})
