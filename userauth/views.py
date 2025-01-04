from django.shortcuts import redirect, render
from userauth.forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import logging

logger = logging.getLogger(__name__)

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(data = request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            new_user.first_name = form.cleaned_data['firstname']
            new_user.last_name = form.cleaned_data['lastname']
            new_user.save()

            messages.success(request, f"Tạo tài khoản thành công cho {username}!")
            
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            
            login(request, new_user)
            return redirect('core:index')

    else:   
        form = UserRegisterForm()

    context = {
        'register_form': form,
        'login_form': UserLoginForm(),
    }
    return render(request, 'userauth/auth.html', context)

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('core:index')
    else:
        form = UserLoginForm()

    context = {
        'register_form': form,
        'login_form': UserLoginForm(),
    }
    return render(request, 'userauth/auth.html', context)

def logout_view(request):
    logout(request)
    return redirect('core:index')

@login_required
def user_profile(request):
    user = request.user  
    context = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, 'userauth/user_profile.html', context)

def edit_profile(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        
        try:
            user.save()
            messages.success(request, "Cập nhật thông tin thành công!")
        except Exception as e:
            messages.error(request, "Có lỗi xảy ra khi cập nhật thông tin.")
            render(request, 'userauth/user_profile.html', {'user': request.user, 'error-message': 'Có lỗi xảy ra khi cập nhật thông tin.'})
        
    return render(request, 'userauth/user_profile.html', {'user': request.user})

def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user
        
        if not user.check_password(current_password):
            messages.error(request, "Mật khẩu hiện tại không đúng!")
            return render(request, 'userauth/user_profile.html', {'message_status': 'Mật khẩu hiện tại không đúng!'})
            
        if new_password != confirm_password:
            messages.error(request, "Mật khẩu mới không khớp!")
            return render(request, 'userauth/user_profile.html', {'message_status': 'Mật khẩu mới không khớp!'})
            
        user.set_password(new_password)
        user.save()
        
        messages.success(request, "Đổi mật khẩu thành công!")
        login(request, user)
        
        return redirect('userauth:my-account')
