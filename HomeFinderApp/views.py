import uuid

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
    return render(request, 'index.html')


def signin(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already Logged in !!')
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                account = Account.objects.get(user=user)
                if account.verify:
                    auth.login(request, user)
                    messages.info(request, 'Login Successful !!!')
                    return redirect('home')
                else:
                    messages.info(request,
                                  'Your account is not verified ,please check your email and verify your Account!!!')
                    return redirect('signin')
            else:
                messages.info(request, 'Invalid Credentials ! ! !')
                return redirect('signin')
    return render(request, 'signin.html')


def register(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are currently logged in, To register a new user kindly logout from the system.')
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
                uid = uuid.uuid4()
                new_user = user_form.save()
                acc_form = form.save(commit=False)
                acc_form.user = new_user
                acc_form.token = uid
                acc_form.save()
                send_email_after_registration(new_user.email, uid)
                messages.info(request, "Your Account Created Successful,to verify your account check email !!!")
                return redirect('signin')
        context = {'form': form, 'user_form': user_form}
        return render(request, 'register.html', context)


def send_email_after_registration(email, token):
    subject = "Verify Email"
    message = f'Hi Click on the link to verify your account http://127.0.0.1:8000/account_verify/{token}'
    from_email = 'mailtohomefinder@gmail.com'
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)


def account_verify(request, token):
    account = Account.objects.filter(token=token).first()
    account.verify = True
    account.save()
    messages.info(request, "Your Account has been verified, you can login !!!")
    return redirect('signin')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are Logged out Successfully ! ! !')
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


def agent_single(request, pk):
    if request.user.is_authenticated:
        if request.method == 'GET':
            form = SearchForm()
        else:
            form = SearchForm(request.POST)
            if form.is_valid():
                status_name = form.cleaned_data['filter_status_by']
                if status_name == 'Rent':
                    try:
                        post = Post.objects.get(id=pk)
                        user = post.user_id
                        property = Post.objects.filter(user_id=user, status='Rent')
                        context = {'post': post, 'property': property}
                        return render(request, 'agent_single.html', context)
                    except:
                        messages.info(request, 'No Homes for rent are available from this owner.')
                elif status_name == 'Sale':
                    try:
                        post = Post.objects.get(id=pk)
                        user = post.user_id
                        property = Post.objects.filter(user_id=user, status='Sale')
                        context = {'post': post, 'property': property}
                        return render(request, 'agent_single.html', context)
                    except:
                        messages.info(request, 'No Homes for sale are available from this owner.')
                else:
                    post = Post.objects.get(id=pk)
                    user = post.user_id
                    property = Post.objects.filter(user_id=user)
                    context = {'post': post, 'property': property}
                    return render(request, 'agent_single.html', context)
        post = Post.objects.get(id=pk)
        user = post.user_id
        property = Post.objects.get(user_id=user)
        context = {'post': post, 'property': property}
        return render(request, 'agent_single.html', context)
    else:
        messages.info(request, 'Login to view more Details....')
        return render(request, 'signin.html')


def agents_grid(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, 'agents_grid.html', context)
    else:
        messages.info(request, 'Login to view more Owners....')
        return render(request, 'signin.html')


def property_grid(request):
    if request.method == 'GET':
        form = SearchForm()
    else:
        form = SearchForm(request.POST)
        if form.is_valid():
            status_name = form.cleaned_data['filter_status_by']
            if status_name == 'Rent':
                posts = Post.objects.filter(status='Rent')
                context = {'posts': posts}
                return render(request, 'property_grid.html', context)
            elif status_name == 'Sale':
                posts = Post.objects.filter(status='Sale')
                context = {'posts': posts}
                return render(request, 'property_grid.html', context)
            else:
                posts = Post.objects.all()
                context = {'posts': posts}
                return render(request, 'property_grid.html', context)
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'property_grid.html', context)


def property_grid_search(request):
    if request.method == 'GET':
        form = FilterForm()
    else:
        form = FilterForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            types = form.cleaned_data['types']
            bedroom = form.cleaned_data['bedroom']
            parking = form.cleaned_data['parking']
            city = form.cleaned_data['city']
            price = form.cleaned_data['price']
            print(status, types, bedroom, parking, city, price)
            if status or types or bedroom or parking or city or price:
                posts = Post.objects.filter(status=status, property_type=types, beds=bedroom,
                                            parking=parking, location=city, price__gte=price)
                context = {'posts': posts}
                return render(request, 'property_grid.html', context)
        else:
            posts = Post.objects.all()
            context = {'posts': posts}
            return render(request, 'property_grid.html', context)


def property_single(request, pk):
    if request.user.is_authenticated:
        post = Post.objects.get(id=pk)
        post1 = PostImages.objects.filter(post_id=pk)
        context = {'post': post,'post1': post1}
        return render(request, 'property_single.html', context)
    else:
        messages.info(request, 'Login to view more Details....')
        return render(request, 'signin.html')


def post_property(request):
    if request.user.is_authenticated:
        form = PostForm()
        image_form = ImageForm()
        username = request.user.username
        user_obj = User.objects.get(username=username)
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            image_form = ImageForm(request.POST, request.FILES)
            images = request.FILES.getlist('imagefile')
            print(images)
            property_id = request.POST.get('property_id')
            if form.errors:
                message = form.errors
                messages.info(request, message)
                return redirect('post_property')
            if image_form.errors:
                message = image_form.errors
                messages.info(request, message)
                return redirect('post_property')
            print(form.is_valid())
            print(image_form.is_valid())
            if form.is_valid() and image_form.is_valid():
                if len(property_id) > 1:
                    post_form = form.save(commit=False)
                    post_form.user = user_obj
                    post = form.save()
                    for image in images:
                        PostImages.objects.create(imagefile=image, post=post)
                    messages.info(request, 'Property Posted Successfully.')
                    return redirect('post_property')
                else:
                    messages.info(request, 'Invalid Property Id')
        property = Post.objects.all()
        context = {'form': form, 'property': property}
        return render(request, 'post_property.html', context)
    else:
        messages.info(request, 'Login to Post your own Property ..')
        return render(request, 'signin.html')


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
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'HomeFinder',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
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
