# import random
# from django.conf import settings
# from django.core.mail import send_mail
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required

# # --- Import all the necessary forms and models ---
# from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
# from .models import CustomUser

# # --- REFACTORED REGISTRATION VIEW ---
# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             # Store all data, including the extra year and department, in the session
#             request.session['temp_user_data'] = {
#                 'username': form.cleaned_data['username'],
#                 'email': form.cleaned_data['email'],
#                 'password': form.cleaned_data['password2'], # Use password2 for confirmation
#                 'year': form.cleaned_data['year'],
#                 'department': form.cleaned_data['department'],
#             }
            
#             # OTP Logic remains the same
#             otp = str(random.randint(100000, 999999))
#             request.session['otp'] = otp
#             send_mail(
#                 subject="CampusConnect Email Verification OTP",
#                 message=f"Your OTP for CampusConnect is {otp}",
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[form.cleaned_data['email']],
#             )
#             messages.success(request, 'Registration successful! Please check your email for an OTP to verify your account.')
#             return redirect('users:verify_otp')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'users/register.html', {'form': form})

# # --- REFACTORED OTP VERIFICATION VIEW ---
# def verify_otp(request):
#     if request.method == 'POST':
#         entered_otp = request.POST.get('otp')
#         if entered_otp == request.session.get('otp'):
#             data = request.session.get('temp_user_data')
#             if data:
#                 # 1. Create the CustomUser object with user-specific fields
#                 user = CustomUser.objects.create_user(
#                     username=data['username'],
#                     email=data['email'],
#                     password=data['password'],
#                     is_otp_verified=True  # Set the user as verified
#                 )
                
#                 # 2. Update the automatically created Profile with profile-specific fields
#                 user.profile.year = data['year']
#                 user.profile.department = data['department']
#                 user.profile.save()

#                 messages.success(request, "Account created and verified successfully! Please log in.")
                
#                 # Clean up session data
#                 request.session.pop('temp_user_data', None)
#                 request.session.pop('otp', None)
                
#                 return redirect('users:login')
#         else:
#             messages.error(request, "Incorrect OTP. Please try again.")
#     return render(request, 'users/verify_otp.html')

# # --- REFACTORED LOGIN VIEW ---
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if user.is_otp_verified or user.is_superuser:
#                 login(request, user)
#                 return redirect('users:dashboard')
#             else:
#                 # This case is unlikely if registration forces OTP, but good to have
#                 messages.error(request, 'Your account is not verified. Please complete the OTP verification.')
#                 return redirect('users:login')
#         else:
#             messages.error(request, 'Invalid username or password.')
#     return render(request, 'users/login.html')

# # --- REFACTORED DASHBOARD VIEW (ACCESSING PROFILE) ---
# @login_required
# def dashboard_view(request):
#     # The view itself is simple. The change is in the template.
#     # We pass the full user object, which has access to .profile
#     return render(request, 'users/dashboard.html', {'user': request.user})

# # --- LOGOUT VIEW (NO CHANGES NEEDED) ---
# def logout_view(request):
#     logout(request)
#     messages.info(request, "You have been logged out successfully.")
#     return redirect('users:login')

# # --- NEW VIEW FOR PROFILE EDITING ---
# @login_required
# def profile_view(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, 'Your profile has been updated!')
#             return redirect('users:profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {
#         'u_form': u_form,
#         'p_form': p_form
#     }
#     return render(request, 'users/profile.html', context)


import random
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count  # --- ADD THIS IMPORT ---

# --- Import all the necessary forms and models ---
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from .models import CustomUser

# --- ADD THESE IMPORTS FROM YOUR FORUM APP ---
from forum.models import Question, Answer, Tag

# --- REGISTRATION AND OTP VIEWS (NO CHANGES NEEDED) ---
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            request.session['temp_user_data'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password2'],
                'year': form.cleaned_data.get('year'), # .get() is safer
                'department': form.cleaned_data.get('department'),
            }
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            send_mail(
                subject="CampusConnect Email Verification OTP",
                message=f"Your OTP for CampusConnect is {otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.cleaned_data['email']],
            )
            messages.success(request, 'Registration successful! Please check your email for an OTP.')
            return redirect('users:verify_otp')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == request.session.get('otp'):
            data = request.session.get('temp_user_data')
            if data:
                user = CustomUser.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    is_otp_verified=True
                )
                user.profile.year = data.get('year')
                user.profile.department = data.get('department')
                user.profile.save()
                messages.success(request, "Account verified! Please log in.")
                request.session.pop('temp_user_data', None)
                request.session.pop('otp', None)
                return redirect('users:login')
        else:
            messages.error(request, "Incorrect OTP. Please try again.")
    return render(request, 'users/verify_otp.html')

# --- LOGIN AND LOGOUT VIEWS (NO CHANGES NEEDED) ---
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_otp_verified or user.is_superuser:
                login(request, user)
                return redirect('users:dashboard')
            else:
                messages.error(request, 'Your account is not verified.')
                return redirect('users:login')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('users:login')

# --- THIS IS THE NEW, DYNAMIC DASHBOARD VIEW ---
@login_required
def dashboard_view(request):
    # Get PERSONAL stats for the logged-in user
    user_question_count = Question.objects.filter(author=request.user).count()
    user_answer_count = Answer.objects.filter(author=request.user).count()

    # Get COMMUNITY stats
    # Find recent questions that have zero answers yet
    unanswered_questions = Question.objects.filter(answers__isnull=True).order_by('-created_at')[:5]

    # Find the most popular tags by counting how many questions are associated with each
    popular_tags = Tag.objects.annotate(
        num_questions=Count('question')
    ).order_by('-num_questions')[:7]

    context = {
        'user': request.user,
        'user_question_count': user_question_count,
        'user_answer_count': user_answer_count,
        'unanswered_questions': unanswered_questions,
        'popular_tags': popular_tags,
    }
    return render(request, 'users/dashboard.html', context)

# --- PROFILE EDITING VIEW (NO CHANGES NEEDED) ---
@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)