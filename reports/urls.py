from django.urls import path
from . import views


urlpatterns = [
    path('reports/', views.results_pdf, name='results-pdf' ),
    path('manager-result-report/<int:pk>', views.results_report, name='results-report'),
    path('stars-matrix/', views.goals_report, name='goals-pdf' ),
    path('employee-attendance-report/<int:pk>', views.employee_attendance_report, name='employee-attendance-report'),
    path('manager-results-report/<int:pk>', views.manager_results_report, name='manager-results-report'),
    path('attendance-policy/', views.attendance_policy, name='attendance-policy-pdf' ),
    path('attendance-report/', views.attendance_last_30, name='attendance-last-30' ),
]
