# forum/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages  # --- THIS IS THE LINE THAT FIXES THE ERROR ---

from .models import Question, Answer 
from .forms import QuestionForm, AnswerForm

@login_required
def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'forum/question_list.html', {'questions': questions})

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_m2m() # Important for saving tags

            # This line will now work because 'messages' is imported
            messages.success(request, 'Your question has been posted successfully!')
            return redirect('forum:question_list')
    else:
        form = QuestionForm()
    return render(request, 'forum/ask_question.html', {'form': form})

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            messages.success(request, 'Your answer has been submitted.')
            return redirect('forum:question_detail', pk=pk)
    else:
        form = AnswerForm()
    answers = question.answers.all().order_by('created_at')
    return render(request, 'forum/question_detail.html', {'question': question, 'answers': answers, 'form': form})

@login_required
def search_results(request):
    query = request.GET.get('q', '')
    if query:
        questions = Question.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    else:
        questions = Question.objects.none()
    context = {
        'questions': questions,
        'query': query,
    }
    return render(request, 'forum/search_results.html', context)