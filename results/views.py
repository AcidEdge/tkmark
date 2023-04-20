import datetime 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Goal, GreenRed, Second, Champ, Mention, Survey, Stars, Updated, SOS, User, Zenput, Period, Streak, Audits
from .forms import GoalsForm, GreenUpdate, SecondUpdate, ChampUpdate, MentionUpdate, SurveyUpdate, SOSUpdate, ZenputUpdate, SelfAuditUpdate
from updates.models import Post
from attendance.models import Attendance
from django.db.models import Sum
from .utilities import get_start_date, get_current_quarter, set_current_streak




#get average speed here.... need to add filter for current period. 
#current error: cannot use Avg on date/time field, sqlite3 saves as text/str
#def get_avg_sos():
   # sos = SOS.objects.first()
   # return sos.day.hour



#get current period:
#returns current period number by looking up dates in period model/table
def get_current_period():
    today = datetime.date.today()
    current_period = Period.objects.filter(start_date__lte=today, end_date__gte=today).get()
    return current_period.period



#function/method to update quarterly results, based on input
def update_results(new_results):
    #import old results:
    oldgreen = GreenRed.objects.filter(manager=new_results[0], period=new_results[1]).get()
    oldsec = Second.objects.filter(manager=new_results[0], period=new_results[1]).get()
    oldchamp = Champ.objects.filter(manager=new_results[0], period=new_results[1]).get()
    oldmention = Mention.objects.filter(manager=new_results[0], period=new_results[1]).get()
    oldsurvey = Survey.objects.filter(manager=new_results[0], period=new_results[1]).get()
    oldzenput = Zenput.objects.filter(manager=new_results[0], period=new_results[1]).get()
    oldaudit = Audits.objects.filter(manager=new_results[0], period=new_results[1]).get()

    #add new to old, calculate new
    
    newgreen = oldgreen.green + new_results[2]
    newred = oldgreen.red + new_results[3]
    total = newgreen + newred
    newsecond = oldsec.seconds + new_results[4]
    newshift = oldchamp.shift + new_results[5]
    newchamp = oldchamp.champs + new_results[6]
    newones = oldsurvey.ones + new_results[7]
    newtwos = oldsurvey.twos + new_results[8]
    newthrees = oldsurvey.threes + new_results[9]
    newfours = oldsurvey.fours + new_results[10]
    newfives = oldsurvey.fives + new_results[11]
    surveytotal=(newones+newtwos+newthrees+newfours+newfives)
    newzenput = oldzenput.missed + new_results[12]
    if new_results[14] == True:
        newaudit = oldaudit.completed + 1
    if new_results[14] == False:
        newaudit = oldaudit.completed
    if(total == 0):
        greenpercent=0
        secondsAvg=0
        champspercent=0
        mentions=0
        fivebells=0
    else:
        greenpercent = (newgreen/total)*100
        secondsAvg = newsecond/total
        champspercent=(newchamp/newshift)*100
        mentions=new_results[13] + oldmention.mention
    if (surveytotal == 0):
        fivebells=0
        diss=0
    else:
        fivebells=(newfives/surveytotal)*100
        diss = newones+newtwos+newthrees
    if champspercent > 100:
        champspercent = 100

    #save updated results:
    GreenRed.objects.filter(manager=new_results[0], period=new_results[1]).update(red=newred, green=newgreen, total_dayparts=total, green_percent=greenpercent)
    Second.objects.filter(manager=new_results[0], period=new_results[1]).update(seconds=newsecond, seconds_avg=secondsAvg, total_dayparts=total, green_percent=greenpercent)
    Champ.objects.filter(manager=new_results[0], period=new_results[1]).update(shift=newshift, champs=newchamp, champs_percent=champspercent, green_percent=greenpercent)
    Mention.objects.filter(manager=new_results[0], period=new_results[1]).update(mention=mentions, green_percent=greenpercent)
    Survey.objects.filter(manager=new_results[0], period=new_results[1]).update(ones=newones, twos=newtwos, threes=newthrees, 
                    fours=newfours, fives=newfives, five_bells=fivebells, dissat=diss, green_percent=greenpercent)
    Zenput.objects.filter(manager=new_results[0], period=new_results[1]).update(missed=newzenput, green_percent=greenpercent)
    Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(green_percent=greenpercent)
    Audits.objects.filter(manager=new_results[0], period=new_results[1]).update(completed=newaudit)
    #get data for points loop:            
    green_results = GreenRed.objects.filter(manager=new_results[0], period=new_results[1]).get()
    second_results = Second.objects.filter(manager=new_results[0], period=new_results[1]).get()
    champs_results = Champ.objects.filter(manager=new_results[0], period=new_results[1]).get()
    mention_results = Mention.objects.filter(manager=new_results[0], period=new_results[1]).get()
    dissat_results = Survey.objects.filter(manager=new_results[0], period=new_results[1]).get()
    zenput_results = Zenput.objects.filter(manager=new_results[0], period=new_results[1]).get()
    audit_results = Audits.objects.filter(manager=new_results[0], period=new_results[1]).get()


    if int(new_results[1]) == 14:  #ytd divide results by 13:
        mention_results.mention = mention_results.mention / 13
        zenput_results.missed = zenput_results.missed / 13
        audit_results.completed = audit_results.completed / 13
        dissat_results.dissat = dissat_results.dissat / 13
    if int(new_results[1]) > 14 and int(new_results[1]) <=17:       #qtd div results by periods in qtd:
        mention_results.mention = mention_results.mention / 3
        zenput_results.missed = zenput_results.missed / 3
        audit_results.completed = audit_results.completed / 3
        dissat_results.dissat = dissat_results.dissat / 3
    if int(new_results[1]) == 18:
        mention_results.mention = mention_results.mention / 4
        zenput_results.missed = zenput_results.missed / 4
        audit_results.completed = audit_results.completed / 4
        dissat_results.dissat = dissat_results.dissat / 4

#go through results and assign stars for each result area
    if green_results.green_percent >= 95.00:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(green_stars=5)
    elif green_results.green_percent >=85.00 and green_results.green_percent <=94.99:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(green_stars=4)
    elif green_results.green_percent >=75.00 and green_results.green_percent <=84.99:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(green_stars=3)
    elif green_results.green_percent >=65.00 and green_results.green_percent <=74.99:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(green_stars=2)
    else:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(green_stars=1)
    if second_results.seconds_avg <= -25.00:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(second_stars=5)
    elif second_results.seconds_avg <= -15.01 and second_results.seconds_avg >= -24.99:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(second_stars=4)
    elif second_results.seconds_avg <=0.00 and second_results.seconds_avg >= -15:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(second_stars=3)
    elif second_results.seconds_avg > 0.00 and second_results.seconds_avg <= 9.99:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(second_stars=2)
    else:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(second_stars=1)
    if champs_results.champs_percent >= 85.00:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(champ_stars=5)
    elif champs_results.champs_percent >= 80.00 and champs_results.champs_percent <= 84.99:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(champ_stars=4)
    elif champs_results.champs_percent >=75.00 and champs_results.champs_percent <= 79.99:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(champ_stars=3)
    elif champs_results.champs_percent >= 70.00 and champs_results.champs_percent <= 74.99:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(champ_stars=2)
    else:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(champ_stars=1)
    if mention_results.mention <=1:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(mention_stars=5)
    elif mention_results.mention == 2:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(mention_stars=4)
    elif mention_results.mention == 3:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(mention_stars=2)
    else:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(mention_stars=1)
    if dissat_results.dissat <=1:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(dissat_stars=5)
    elif dissat_results.dissat >=1.01 and dissat_results.dissat <= 2:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(dissat_stars=4)
    elif dissat_results.dissat >=2.01 and dissat_results.dissat <= 3:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(dissat_stars=3)
    else:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(dissat_stars=1)
    if zenput_results.missed == 0:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(zenput_stars=5)
    elif zenput_results.missed == 1:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(zenput_stars=3)
    else:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(zenput_stars=1)
    if audit_results.completed >= 1:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(audit_stars=5)
    else:
        Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(audit_stars=1)
#iterate through managers in stars, getting tuple of stars, adds together, calculates average, saves avg and totals
    stars = Stars.objects.filter(manager=new_results[0], period=new_results[1]).get()
    total_stars = stars.green_stars + stars.second_stars + stars.champ_stars + stars.mention_stars + stars.dissat_stars + stars.zenput_stars + stars.audit_stars
    total_avg = total_stars / 7
    Stars.objects.filter(manager=new_results[0], period=new_results[1]).update(stars_total=total_stars, stars_avg=total_avg)




@login_required(login_url='login')
def home(request):
    if request.user.is_staff:
        current_period = get_current_period()
        context = {
            ## need to filter by date, get period number from period table and use to filter the results
            'greenresult' : GreenRed.objects.filter(period=current_period).all().order_by('-green_percent', '-total_dayparts', '-green'),
            'secondresult' : Second.objects.filter(period=current_period).all().order_by('seconds_avg', '-green_percent', 'seconds'),
            'champs' : Champ.objects.filter(period=current_period).all().order_by('-champs_percent', '-green_percent', '-champs', '-shift'),
            'mention' : Mention.objects.filter(period=current_period).all().order_by('mention', '-green_percent'),
            'dissat' : Survey.objects.filter(period=current_period).all().order_by('dissat', '-green_percent', '-five_bells'),
            'goals': Goal.objects.first(),
            'starsresult' :Stars.objects.filter(period=current_period).all().order_by('-stars_avg', '-green_percent'),
            'updated' : Updated.objects.first(),
            'news' : Post.objects.order_by('-date_posted').first(),
            'period': current_period,
            'zenput': Zenput.objects.filter(period=current_period).all().order_by('missed', '-green_percent'),
            'audit' : Audits.objects.filter(period=current_period).all().order_by('-completed'),
            'absence': Attendance.objects.order_by('-entered_on').first(),
            'team_absent': Attendance.objects.filter(date__range=[get_start_date(30), datetime.date.today()]).order_by('-date'),
            'title': "Manager Results - Home",
            'streak': Streak.objects.first(),
           # 'sos': get_avg_sos(),
            #add sos here once working
        }
        return render(request, 'results/home.html', context)
    else:
        context={
            'attendance': Attendance.objects.filter(employee=request.user, date__range=[get_start_date(30), datetime.date.today()]).order_by('-date'),
            'points_total': Attendance.objects.filter(employee=request.user, date__range=[get_start_date(30), datetime.date.today()]).aggregate(Sum('points')),
            'title': "Attendance - Home",
            'streak': Streak.objects.first(),
        }
        return render(request, 'attendance/home.html', context)
    



def about(request):
    if request.user.is_staff:
        context = {
            'goals': Goal.objects.first(),
            'updated' : Updated.objects.first(),
            'news' : Post.objects.order_by('-date_posted').first(),
            'absence': Attendance.objects.order_by('-entered_on').first(),
            'streak': Streak.objects.first(),
            'title': "M.A.S.O.N. System - About"
        }
        return render(request, 'results/about.html', context)
    else:
        context={
            'attendance': Attendance.objects.filter(employee=request.user).all().order_by('-date'),
            'points_total': Attendance.objects.filter(employee=request.user).aggregate(Sum('points')),
            'title': "Attendance - About & Policy Page",
            'streak': Streak.objects.first(),
        }
        return render(request, 'attendance/about.html', context)



#method for updating goals - gets goal update form and overwrites/updates goal table
@login_required(login_url='login')
def update_goals(request):
    if request.method == 'POST':
        form = GoalsForm(request.POST)
        if form.is_valid():
            green = form.cleaned_data['green_goal']
            seconds = form.cleaned_data['seconds_goal']
            champs = form.cleaned_data['champs_goal']
            mention = form.cleaned_data['mention_goal']
            diss = form.cleaned_data['dissat_goal']
            star = form.cleaned_data['star_goal']
            audit = form.cleaned_data['audit_goal']
            zenput = form.cleaned_data['zenput_goal']
            update= Goal(id=1,green_goal=green, seconds_goal=seconds, champs_goal=champs, 
                            mention_goal=mention, dissat_goal=diss, star_goal=star, audit_goal = audit, zenput_goal=zenput)
            update.save()
            #form.save()
            messages.success(request, f'Goals have been updated!')
            return redirect('results-home')
    else:
        form = GoalsForm()
        
    context = {
        'updated' : Updated.objects.first(),
        'form' : GoalsForm,
        'news' : Post.objects.order_by('-date_posted').first(),
        'absence': Attendance.objects.order_by('-entered_on').first(),
        'streak': Streak.objects.first(),
        'title': "Update Goals"
    }
    return render(request, 'results/goal_form.html', context)


@login_required(login_url='login')
def new_results(request):
    if request.method == 'POST':
    #save current period:
        green_form = GreenUpdate(request.POST)
        seconds_form = SecondUpdate(request.POST)
        champ_form = ChampUpdate(request.POST)
        zenput_form = ZenputUpdate(request.POST)
        mention_form = MentionUpdate(request.POST)
        survey_form = SurveyUpdate(request.POST)
        audit_form = SelfAuditUpdate(request.POST)
        if green_form.is_valid() and seconds_form.is_valid() and champ_form.is_valid() and mention_form.is_valid() and survey_form.is_valid() and zenput_form.is_valid() and audit_form.is_valid():
            manager = green_form.cleaned_data['manager']
            period = green_form.cleaned_data['period']
            form_green = green_form.cleaned_data['green']
            form_red = green_form.cleaned_data['red']
            form_sec = seconds_form.cleaned_data['seconds']
            form_shift = champ_form.cleaned_data['shift']
            form_champ = champ_form.cleaned_data['champs']
            form_one = survey_form.cleaned_data['ones']
            form_two = survey_form.cleaned_data['twos']
            form_three = survey_form.cleaned_data['threes']
            form_four = survey_form.cleaned_data['fours']
            form_five = survey_form.cleaned_data['fives']
            form_missed = zenput_form.cleaned_data['missed']
            form_mention = mention_form.cleaned_data['mention']
            form_audit = audit_form.cleaned_data['completed']
            form_results = [manager, period, form_green, form_red, form_sec, form_shift, form_champ, form_one, form_two, form_three, form_four, form_five, form_missed, form_mention, form_audit]
            ytd_results = [manager, 14, form_green, form_red, form_sec, form_shift, form_champ, form_one, form_two, form_three, form_four, form_five, form_missed, form_mention, form_audit]
            current_period=get_current_period()
            current_quarter = get_current_quarter(current_period) + 14
            qtd_results = [manager, current_quarter, form_green, form_red, form_sec, form_shift, form_champ, form_one, form_two, form_three, form_four, form_five, form_missed, form_mention, form_audit]
            update_results(form_results)
            update_results(ytd_results)
            update_results(qtd_results)

            manager_name = User.objects.filter(id=manager).get()
            updated_by = request.user
            time = datetime.datetime.now()
            Updated.objects.filter(id=1).update(update_by=updated_by, date_updated=time)
            messages.success(request, f'New Results Entered for ' + str(manager_name.first_name).title() +' for Period ' + str(period))
            return redirect('results-home')
    else:
        green_form = GreenUpdate()
        seconds_form = SecondUpdate()
        champ_form = ChampUpdate()
        mention_form = MentionUpdate()
        survey_form = SurveyUpdate()
        zenput_form = ZenputUpdate()
        audit_form = SelfAuditUpdate()
    
    context = {
        'green_form': green_form,
        'seconds_form': seconds_form,
        'champ_form': champ_form,
        'mention_form': mention_form,
        'survey_form': survey_form,
        'zenput_form': zenput_form,
        'updated' : Updated.objects.first(),
        'news' : Post.objects.order_by('-date_posted').first(),
        'absence': Attendance.objects.order_by('-entered_on').first(),
        'audit_form' : audit_form,
        'title': "Enter Manager Results",
        'streak': Streak.objects.first(),
    }

    return render(request, 'results/new-results.html', context)

    
@login_required(login_url='login')
def view_past_results(request, **kwargs):
    selected_period = kwargs.get('pk')
    ytd=14
    if selected_period == ytd:
        title = 'Year-to-Date Results'
    elif selected_period == 15:
        title = "Quarter 1 Results"
    elif selected_period == 16:
        title = "Quarter 2 Results"
    elif selected_period == 17:
        title = "Quarter 3 Results"
    elif selected_period == 18:
        title = "Quarter 4 Results"
    else:
        title = "Period " + str(selected_period) + " Results"
    context = {
        'greenresult' : GreenRed.objects.filter(period=selected_period).all().order_by('-green_percent', '-total_dayparts', '-green'),
        'secondresult' : Second.objects.filter(period=selected_period).all().order_by('seconds_avg', '-green_percent', 'seconds'),
        'champs' : Champ.objects.filter(period=selected_period).all().order_by('-champs_percent', '-green_percent', '-champs', '-shift'),
        'mention' : Mention.objects.filter(period=selected_period).all().order_by('mention', '-green_percent'),
        'dissat' : Survey.objects.filter(period=selected_period).all().order_by('dissat', '-green_percent', '-five_bells'),
        'goals': Goal.objects.first(),
        'starsresult' :Stars.objects.filter(period=selected_period).all().order_by('-stars_avg', '-green_percent'),
        'zenput': Zenput.objects.filter(period=selected_period).all().order_by('missed', '-green_percent'),
        'period': selected_period,
        'ytd': ytd,
        'updated' : Updated.objects.first(),
        'news' : Post.objects.order_by('-date_posted').first(),
        'absence': Attendance.objects.order_by('-entered_on').first(),
        'title': title,
        'streak': Streak.objects.first(),
        'audit' : Audits.objects.filter(period=selected_period).all().order_by('-completed'),
    }
   
    return render(request, 'results/period.html', context)

@login_required(login_url='login')
def enter_sos(request):
    if request.method == 'POST':
        form = SOSUpdate(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            breakfast = form.cleaned_data['breakfast']
            lunch = form.cleaned_data['lunch']
            snack = form.cleaned_data['snack']
            dinner = form.cleaned_data['dinner']
            evening = form.cleaned_data['evening']
            close = form.cleaned_data['close']
            day = form.cleaned_data['day']
            grn_brk = form.cleaned_data['brk_green']
            grn_lnch = form.cleaned_data['lunch_green']
            grn_snk = form.cleaned_data['snack_green']
            grn_din = form.cleaned_data['dinner_green']
            grn_eve = form.cleaned_data['eve_green']
            grn_cl = form.cleaned_data['cl_green']
            current = Streak.objects.first()
            current_streak = current.current
            longest = current.longest
            sos = [current_streak, grn_brk, grn_lnch, grn_snk, grn_din, grn_eve, grn_cl, longest]
            new_streak = set_current_streak(sos)
            if new_streak > longest:
                Streak.objects.filter(id=1).update(current=new_streak, longest=new_streak)
            else:
                Streak.objects.filter(id=1).update(current=new_streak, longest=longest)
            SOS.objects.update_or_create(date=date, breakfast=breakfast, lunch=lunch, snack=snack, dinner=dinner, evening= evening, close=close, day=day)
            date_message = str(date)
            messages.success(request, f'SOS for ' + date_message + ' has been updated!')
            return redirect('results-home')
    else:
        form = SOSUpdate()
        
    context = {
        'updated' : Updated.objects.first(),
        'form' : SOSUpdate,
        'news' : Post.objects.order_by('-date_posted').first(),
        'absence': Attendance.objects.order_by('-entered_on').first(),
        'title': "Enter S.O.S.",
        'streak': Streak.objects.first(),
    }
    return render(request, 'results/sos_update.html', context)



