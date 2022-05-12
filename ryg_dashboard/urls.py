from django.urls import path

from . import views

urlpatterns = [
    path('', views.ryg_dashboard, name='index'),
    path('greens_by_date', views.greens_by_date_view, name='greens_by_date'),
    path('greens_by_team', views.greens_by_team_view, name='greens_by_team'),
    path('emot_by_date', views.emot_by_date_view, name='emot_by_team'),
    path('num_check_ins', views.num_check_ins_view, name='num_check_ins'),
]