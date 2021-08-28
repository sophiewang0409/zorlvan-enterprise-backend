from django.urls import path
from . import views

urlpatterns = [
    path('attend/', views.create_participant_view),
    path('unattend/', views.delete_participant_view)
]