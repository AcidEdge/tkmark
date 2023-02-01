from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='results-home'),
    path('about/', views.about, name='results-about'),
    path('update-goals/', views.update_goals, name='update-goals'),
    path('new-results/', views.new_results, name='new-results'),
    path('period-results/<int:pk>', views.view_past_results, name='past-results'),
    path('sos-update/', views.enter_sos, name='enter-sos'),
]
