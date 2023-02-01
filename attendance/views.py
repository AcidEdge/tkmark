from django.shortcuts import render, redirect
from .models import Codes, Attendance
from results.models import Updated, Streak
from updates.models import Post
from django.db.models import Sum
from django.contrib.auth.decorators import *
from .forms import AttendanceForm
from django.contrib import messages
import datetime
from users.models import User
from results.utilities import get_start_date
from django.views.generic import (
    DetailView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



@login_required
def home(request):
    context = {
        'attendance': Attendance.objects.filter(employee=request.user, date__range=[get_start_date(30), datetime.date.today()]).all().order_by('-date'),
        'updated' : Updated.objects.first(),
        'news' : Post.objects.order_by('-date_posted').first(),
        'points_total': Attendance.objects.filter(employee=request.user, date__range=[get_start_date(30), datetime.date.today()]).aggregate(Sum('points')),
        'absence': Attendance.objects.order_by('-entered_on').first(),
        'team_absent': Attendance.objects.filter(date__range=[get_start_date(30), datetime.date.today()]).order_by('-date'),
        'title': "Attendance - Home",
        'streak': Streak.objects.first(),
    }
    return render(request, 'attendance/home.html', context)

@login_required(login_url='login')
def new_absence(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            employee = form.cleaned_data.get('employee')
            absent_employee = User.objects.filter(id=employee).get()
            type = form.cleaned_data.get('type')
            absence_type = Codes.objects.filter(code_id=type).get()
            notes = form.cleaned_data.get('notes')
            entered_by = request.user.first_name +" "+ request.user.last_name
            entered_on = datetime.datetime.now()
            point = Codes.objects.filter(code_id=type).values_list('points')
            absence = Attendance(date=date, employee=absent_employee, code=absence_type, points=point, notes=notes, entered_by=entered_by, entered_on=entered_on)
            absence.save()
            messages.success(request, f'Absence has been entered for '+ str(absent_employee.first_name)+'!')
            return redirect('results-home')
    else:
        form = AttendanceForm()
        
    context = {
        'updated' : Updated.objects.first(),
        'form' : AttendanceForm,
        'news' : Post.objects.order_by('-date_posted').first(),
        'absence': Attendance.objects.order_by('-entered_on').first(),
        'streak': Streak.objects.first(),
        'title': "Enter New Absence"
        
    }
    return render(request, 'attendance/absent_form.html', context)

def about(request):
    context={
        'updated' : Updated.objects.first(),
        'form' : AttendanceForm,
        'news' : Post.objects.order_by('-date_posted').first(),
        'absence': Attendance.objects.order_by('-entered_on').first(),
        'streak': Streak.objects.first(),
        'title': "Attendance Policy ",
    }
    return render(request, 'attendance/about.html', context)

def user_attendance_detail(request, **kwargs):
    user= kwargs.get('pk')
    context={
        'updated' : Updated.objects.first(),
        'news' : Post.objects.order_by('-date_posted').first(),
        'absence': Attendance.objects.order_by('-entered_on').first(),
        'attendance_all': Attendance.objects.filter(employee=user).all().order_by('-date'),
        'attendance': Attendance.objects.filter(employee=user, date__range=[get_start_date(30), datetime.date.today()]).all().order_by('-date'),
        'points_total': Attendance.objects.filter(employee=user, date__range=[get_start_date(30), datetime.date.today()]).aggregate(Sum('points')),
        'employee': User.objects.filter(id=user).get(),
        'streak': Streak.objects.first(),
        'title': "Attendance - User Detail"
    }
    return render(request, 'attendance/user_detail.html', context)

def day_attendance_detail(request, *args, ** kwargs):
    day = kwargs.get('pk')
    context={
        'updated' : Updated.objects.first(),
        'news' : Post.objects.order_by('-date_posted').first(),
        'absence': Attendance.objects.order_by('-entered_on').first(),
        'attendance': Attendance.objects.filter(date=day).all(),
        'day': day,
        'streak': Streak.objects.first(),
        'title': "Attendance - Day Detail"
    }
    return render(request, 'attendance/day_detail.html', context)

class AttendanceDetailView(LoginRequiredMixin, DetailView):
    model = Attendance

class AttendanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Attendance
    fields = ['date', 'code', 'notes']

    def form_valid(self, form):
        managerName = str(self.request.user.first_name) + " " + str(self.request.user.last_name)
        form.instance.entered_by = managerName
        type = form.instance.code.code_id
        form.instance.points = Codes.objects.filter(code_id=type).values_list('points')
        return super().form_valid(form)

    def test_func(self):
        attendance = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False

class AttendanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Attendance
    success_url = '/attendance/'

    def test_func(self):
        attendance = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False


