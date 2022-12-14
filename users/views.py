from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from results.models import *
from updates.models import Post


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('first_name')
            messages.success(request, f'User account has been created for {username}!')
            return redirect('results-home')
    else:
        form = UserRegisterForm()
    context = {
        'updated' : Updated.objects.first(),
        'form' : UserRegisterForm,
        'news' : Post.objects.order_by('-date_posted').first()
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    context = {
        'updated' : Updated.objects.first(),
        'news' : Post.objects.order_by('-date_posted').first()
    }
    return render(request, 'users/profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'updated' : Updated.objects.first(),
        'news' : Post.objects.order_by('-date_posted').first()
    }

    return render(request, 'users/update_profile.html', context)
