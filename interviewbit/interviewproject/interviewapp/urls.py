from django.urls import path
from . import views
from .views import InterviewList, InterviewCreate,ParticipantRegister,Update,DeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',InterviewList.as_view(),name='interviews'),
    path('interview-create/',InterviewCreate.as_view(),name='interview-create'),
    path('participant-create/',ParticipantRegister.as_view(),name='participant-create'),
    path('interview-update/<int:pk>/',Update.as_view(),name='interview-update'),
    path('interview-delete/<int:pk>/',DeleteView.as_view(),name='interview-delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
