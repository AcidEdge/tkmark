import datetime 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from results.models import Goal, GreenRed, Second, Champ, Mention, Survey, Stars, Updated, User, Zenput, Period, Streak, Audits
from updates.models import Post
from django.http import  HttpResponse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from attendance.models import Attendance
from django.db.models import Sum
from results.utilities import get_start_date, get_all_users

def get_current_period():
    today = datetime.date.today()
    current_period = Period.objects.filter(start_date__lte=today, end_date__gte=today).get()
    return current_period.period


#render pdf report from html using context data, returns pdf file in a reader view, 
#uses results/pdf.html to render
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

#select results html page view
@login_required(login_url='login')
def results_pdf(request, *args, **kwargs):
    context = {
        'updated' : Updated.objects.first(),
        'news' : Post.objects.order_by('-date_posted').first(),
        'absence': Attendance.objects.order_by('-entered_on').first(),
        'employee': User.objects.all(),
        'manager': User.objects.filter(groups__name='manager').all(),
        'streak': Streak.objects.first(),
        'title': "Reporting"
    }
    return render(request,'reports/result_pdf.html', context )

#generate period results report in pdf
@login_required(login_url='login')
def results_report(request, *args, **kwargs):
    selected_period = kwargs.get('pk')
    ytd=14
    if selected_period ==19:
        selected_period = get_current_period()
    context = {
        'greenresult' : GreenRed.objects.filter(period=selected_period).all().order_by('-green_percent', '-total_dayparts', '-green'),
        'secondresult' : Second.objects.filter(period=selected_period).all().order_by('seconds_avg', '-green_percent', 'seconds'),
        'champs' : Champ.objects.filter(period=selected_period).all().order_by('-champs_percent', '-green_percent', '-champs', '-shift'),
        'mention' : Mention.objects.filter(period=selected_period).all().order_by('mention', '-green_percent'),
        'dissat' : Survey.objects.filter(period=selected_period).all().order_by('dissat', '-green_percent', '-five_bells'),
        'goals': Goal.objects.first(),
        'starsresult' :Stars.objects.filter(period=selected_period).all().order_by('-stars_avg',  '-green_percent'),
        'period': selected_period,
        'ytd': ytd,
        'zenput': Zenput.objects.filter(period=selected_period).all().order_by('missed', '-green_percent'),
        'now': datetime.datetime.now(),
        'audit' : Audits.objects.filter(period=selected_period).all().order_by('-completed'),
        'title': "Results Report"

    }
    #call render to pdf with context data. 
    pdf = render_to_pdf('reports/pdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

#generate period results report in pdf
@login_required(login_url='login')
def goals_report(request):
    context = {
        'now': datetime.datetime.now(),
        'title': "5-Star Goals Matrix"
    }
    #call render to pdf with context data. 
    pdf = render_to_pdf('reports/goals.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

#generate employee level attendance report
@login_required(login_url='login')
def employee_attendance_report(request, **kwargs):
    userId = kwargs.get('pk')
    context = {
        'now': datetime.datetime.now(),
        'attendance':Attendance.objects.filter(employee=userId, date__range=[get_start_date(30), datetime.date.today()]).all().order_by('-date'),
        'attendance_all':Attendance.objects.filter(employee=userId).all().order_by('-date'),
        'points_total': Attendance.objects.filter(employee=userId, date__range=[get_start_date(30), datetime.date.today()]).aggregate(Sum('points')),
        'employee': User.objects.filter(id=userId).get(),
        'title': "Employee Attendance Report"
    }
    #call render to pdf with context data. 
    pdf = render_to_pdf('reports/user_attendance_pdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

#generate results report by individual manager
#include year-to-date and all period results
@login_required(login_url='login')
def manager_results_report(request, **kwargs):
    userId = kwargs.get('pk')
    context = {
        'now': datetime.datetime.now(),
        'manager': User.objects.filter(id=userId).get(),
        'greenresult' : GreenRed.objects.filter(manager=userId).all().order_by('period'),
        'secondresult' : Second.objects.filter(manager=userId).all().order_by('period'),
        'champs' : Champ.objects.filter(manager=userId).all().order_by('period'),
        'mention' : Mention.objects.filter(manager=userId).all().order_by('period'),
        'dissat' : Survey.objects.filter(manager=userId).all().order_by('period'),
        'goals': Goal.objects.first(),
        'starsresult' :Stars.objects.filter(manager=userId).all().order_by('period'),
        'zenput': Zenput.objects.filter(manager=userId).all().order_by('period'),
        'audit' : Audits.objects.filter(manager=userId).all().order_by('period'),
        'attendance':Attendance.objects.filter(employee=userId, date__range=[get_start_date(30), datetime.date.today()]).all().order_by('-date'),
        'points_total': Attendance.objects.filter(employee=userId, date__range=[get_start_date(30), datetime.date.today()]).aggregate(Sum('points')),
        
    }
    #call render to pdf with context data. 
    pdf = render_to_pdf('reports/manager_results_pdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

#generate period results report in pdf
@login_required(login_url='login')
def attendance_policy(request):
    context = {
        'now': datetime.datetime.now(),
        'title': "Attendance Policy"
    }
    #call render to pdf with context data. 
    pdf = render_to_pdf('reports/attendance_policy.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

def attendance_last_30(request):
    context = {
        'now': datetime.datetime.now(),
        'attendance':Attendance.objects.filter(date__range=[get_start_date(30), datetime.date.today()]).all().order_by('-date'),
        'title': "Attendance Report - Last 30 Days"
    }
    #call render to pdf with context data. 
    pdf = render_to_pdf('reports/attendance_last_30.html', context)
    return HttpResponse(pdf, content_type='application/pdf')