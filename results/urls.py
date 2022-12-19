from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='results-home'),

    path('about/', views.about, name='results-about'),
    path('update-goals/', views.update_goals, name='update-goals'),
    path('new-results/', views.new_results, name='new-results'),
    path('clear-results/', views.clear_results, name='clear-results'),
    path('results/', views.results_pdf, name='results-pdf' ),
    path('manager-result-report/', views.results_report, name='results-report'),

    
]
