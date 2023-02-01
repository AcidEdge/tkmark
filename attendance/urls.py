from django.urls import path
from attendance import views
from .views import AttendanceDetailView, AttendanceUpdateView, AttendanceDeleteView


urlpatterns = [
    path('attendance/', views.home, name='attendance-home'),
    path('attendance/enter-absence/', views.new_absence, name='attendance-form'),
    path('attendance/about/', views.about, name='attendance-about'),
    path('attendance/employee-detail/<str:pk>', views.user_attendance_detail, name='user-attendance'),
    path('attendance/date-details/<int:pk>', views.day_attendance_detail, name='day-detail'),
    path('attendance/<int:pk>/', AttendanceDetailView.as_view(), name='absence-detail'),
    path('attendance/<int:pk>/update/', AttendanceUpdateView.as_view(), name='absence-update'),
    path('attendance/<int:pk>/delete/', AttendanceDeleteView.as_view(), name='absence-delete'),




    
]
