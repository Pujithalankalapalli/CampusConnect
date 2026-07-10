from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    # This is now the single, main URL for your forum's homepage.
    path('', views.question_list, name='question_list'),
    
    # URL for the "Ask a Question" page.
    path('ask/', views.ask_question, name='ask_question'),
    
    # URL for viewing a single question's details.
    path('<int:pk>/', views.question_detail, name='question_detail'),
    
    # --- THIS IS THE NEW, REQUIRED URL FOR THE SEARCH BAR ---
    path('search/', views.search_results, name='search'),
]