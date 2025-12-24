from django.contrib.auth import logout, login
from django.shortcuts import redirect, render
from .forms import SignUpForm


def logout_view(request):
    logout(request)
    return redirect('courses:course_list')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('courses:course_list')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
