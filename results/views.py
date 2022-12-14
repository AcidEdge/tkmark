import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Goal, GreenRed, Second, Champ, Mention, Survey, Stars, Updated
from .forms import GoalsForm, GreenUpdate, SecondUpdate, ChampUpdate, MentionUpdate, SurveyUpdate
from updates.models import Post
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas 
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

def home(request):
    context = {
        'greenresult' : GreenRed.objects.all().order_by('-green_percent', '-total_dayparts', '-green'),
        'secondresult' : Second.objects.all().order_by('seconds_avg', 'seconds'),
        'champs' : Champ.objects.all().order_by('-champs_percent', '-champs', '-shift'),
        'mention' : Mention.objects.all().order_by('-mention'),
        'fivebells': Survey.objects.all().order_by('-five_bells'),
        'dissat' : Survey.objects.all().order_by('dissat', '-five_bells'),
        'goals': Goal.objects.first(),
        'starsresult' :Stars.objects.all().order_by('-stars_avg'),
        'updated' : Updated.objects.first(),
        'news' : Post.objects.order_by('-date_posted').first()
    }
    return render(request, 'results/home.html', context)



def about(request):
    context = {
        'goals': Goal.objects.first(),
        'updated' : Updated.objects.first(),
        'news' : Post.objects.order_by('-date_posted').first()
    }
    return render(request, 'results/about.html', context)
    

#method for updating goals - gets goal update form and overwrites/updates goal table
@login_required
def update_goals(request):
    if request.method == 'POST':
        form = GoalsForm(request.POST)
        if form.is_valid():
            green = form.cleaned_data['green_goal']
            seconds = form.cleaned_data['seconds_goal']
            champs = form.cleaned_data['champs_goal']
            mention = form.cleaned_data['mention_goal']
            five = form.cleaned_data['five_bells_goal']
            diss = form.cleaned_data['dissat_goal']
            star = form.cleaned_data['star_goal']
            update= Goal(id=1,green_goal=green, seconds_goal=seconds, champs_goal=champs, 
                            mention_goal=mention, five_bells_goal=five, dissat_goal=diss, star_goal=star)
            update.save()
            #form.save()
            messages.success(request, f'Goals have been updated!')
            return redirect('results-home')
    else:
        form = GoalsForm()
        
    context = {
        'updated' : Updated.objects.first(),
        'form' : GoalsForm,
        'news' : Post.objects.order_by('-date_posted').first()
    }
    return render(request, 'results/goal_form.html', context)


@login_required
def new_results(request):
    if request.method == 'POST':
        green_form = GreenUpdate(request.POST)
        seconds_form = SecondUpdate(request.POST)
        champ_form = ChampUpdate(request.POST)
        mention_form = MentionUpdate(request.POST)
        survey_form = SurveyUpdate(request.POST)
        if green_form.is_valid() and seconds_form.is_valid() and champ_form.is_valid() and mention_form.is_valid() and survey_form.is_valid():
            manager = green_form.cleaned_data['manager']
            
        #import old results:
            oldgreen = GreenRed.objects.filter(manager=manager).get()
            oldsec = Second.objects.filter(manager=manager).get()
            oldchamp = Champ.objects.filter(manager=manager).get()
            oldmention = Mention.objects.filter(manager=manager).get()
            oldsurvey = Survey.objects.filter(manager=manager).get()
          #uses dictionary, so to access use oldgreen['green']

        #add new to old, calculate new
            newgreen = oldgreen.green + green_form.cleaned_data['green']
            newred = oldgreen.red + green_form.cleaned_data['red']
            total = newgreen + newred
            newsecond = oldsec.seconds + seconds_form.cleaned_data['seconds']
            newshift = oldchamp.shift + champ_form.cleaned_data['shift']
            newchamp = oldchamp.champs + champ_form.cleaned_data['champs']
            newones = oldsurvey.ones + survey_form.cleaned_data['ones']
            newtwos = oldsurvey.twos + survey_form.cleaned_data['twos']
            newthrees = oldsurvey.threes + survey_form.cleaned_data['threes']
            newfours = oldsurvey.fours + survey_form.cleaned_data['fours']
            newfives = oldsurvey.fives + survey_form.cleaned_data['fives']
            surveytotal=(newones+newtwos+newthrees+newfours+newfives)
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
                mentions=mention_form.cleaned_data['mention'] + oldmention.mention
            if (surveytotal == 0):
                fivebells=0
                diss=0
            else:
                fivebells=(newfives/surveytotal)*100
                diss = ((newones+newtwos+newthrees)/surveytotal)*100
            if champspercent > 100:
                champspercent = 100
        #save updated results:
            GreenRed.objects.filter(manager=manager).update(red=newred, green=newgreen, total_dayparts=total, green_percent=greenpercent)
            Second.objects.filter(manager=manager).update(seconds=newsecond, seconds_avg=secondsAvg, total_dayparts=total, green_percent=greenpercent)
            Champ.objects.filter(manager=manager).update(shift=newshift, champs=newchamp, champs_percent=champspercent, green_percent=greenpercent)
            Mention.objects.filter(manager=manager).update(mention=mentions, green_percent=greenpercent)
            Survey.objects.filter(manager=manager).update(ones=newones, twos=newtwos, threes=newthrees, 
                            fours=newfours, fives=newfives, five_bells=fivebells, dissat=diss, green_percent=greenpercent)
#get data for points loop:            
            green_results = GreenRed.objects.values_list('manager').order_by('green_percent', 'green', 'total_dayparts')
            second_results = Second.objects.values_list('manager').order_by('-seconds_avg', 'green_percent', '-seconds')
            champs_results = Champ.objects.values_list('manager').order_by('champs_percent', 'green_percent', 'champs', 'shift')
            mention_results = Mention.objects.values_list('manager').order_by('mention', 'green_percent')
            fivebells_results = Survey.objects.values_list('manager').order_by('five_bells', 'green_percent',)
            dissat_results = Survey.objects.values_list('manager').order_by('-dissat', 'green_percent', 'five_bells')
#loop through results and assign points:
            point =0
            Stars.objects.all().update(stars_total=point)
            for result in green_results:
                Stars.objects.filter(manager=result).update(green_stars=point)
                point +=1
            point=0
            for result in second_results:
                Stars.objects.filter(manager=result).update(second_stars=point)
                point +=1
            point=0
            for result in champs_results:
                Stars.objects.filter(manager=result).update(champ_stars=point)
                point +=1
            point=0
            for result in mention_results:
                Stars.objects.filter(manager=result).update(mention_stars=point)
                point +=1
            point=0
            for result in fivebells_results:
                Stars.objects.filter(manager=result).update(fivebell_stars=point)
                point +=1
            point=0
            for result in dissat_results:
                Stars.objects.filter(manager=result).update(dissat_stars=point)
                point +=1
#iterate through managers in stars, getting tuple of stars, adds together, calculates average, saves avg and totals
            star_results = Stars.objects.values_list('manager')
            for name in star_results:
                total_stars = 0
                results = Stars.objects.filter(manager=name).values_list('green_stars', 'second_stars', 'champ_stars', 'mention_stars', 'fivebell_stars', 'dissat_stars')
                for point in results:
                    for x in point:
                        total_stars = total_stars + x
                total_avg = total_stars / 6
                Stars.objects.filter(manager=name).update(stars_total=total_stars, stars_avg=total_avg, green_percent=greenpercent)
            updated_by = request.user
            time = datetime.datetime.now()
            Updated.objects.filter(id=1).update(update_by=updated_by, date_updated=time)
            messages.success(request, f'New Results Entered for ' + str(manager.first_name).title())
            return redirect('results-home')
    else:
        green_form = GreenUpdate()
        seconds_form = SecondUpdate()
        champ_form = ChampUpdate()
        mention_form = MentionUpdate()
        survey_form = SurveyUpdate()
    
    context = {
        'green_form': green_form,
        'seconds_form': seconds_form,
        'champ_form': champ_form,
        'mention_form': mention_form,
        'survey_form': survey_form,
        'updated' : Updated.objects.first(),
        'news' : Post.objects.order_by('-date_posted').first()
    }

    return render(request, 'results/new-results.html', context)


@login_required
def clear_results(request):
    context = {
        'updated' : Updated.objects.first(),
        'news' : Post.objects.order_by('-date_posted').first()
    }
    if request.method == 'POST':
        manager_list = GreenRed.objects.values_list('manager').order_by('green_percent')
        for man in manager_list:
            GreenRed.objects.filter(manager=man).update(red=0, green=0, total_dayparts=0, green_percent=0)
            Second.objects.filter(manager=man).update(seconds=0, seconds_avg=0, total_dayparts=0)
            Champ.objects.filter(manager=man).update(shift=0, champs=0, champs_percent=0)
            Mention.objects.filter(manager=man).update(mention=0)
            Survey.objects.filter(manager=man).update(ones=0, twos=0, threes=0, fours=0, fives=0, five_bells=0, dissat=0)
            Stars.objects.filter(manager=man).update(stars_total=0, stars_avg=0, green_stars=0, second_stars=0, 
                                champ_stars=0, mention_stars=0, fivebell_stars=0, dissat_stars=0)
        messages.warning(request, f'All results have been cleared.')
        return redirect('results-home')
    return render(request, 'results/clear_results.html', context)


#generate pdf report 
def results_pdf(request):
    context = {
        'updated' : Updated.objects.first(),
        'news' : Post.objects.order_by('-date_posted').first()
    }
    return render(request,'results/result_pdf.html', context )
