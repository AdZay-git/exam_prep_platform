from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Answer, Result
from django.contrib.auth.decorators import login_required
from .models import Result, Quiz

@login_required
def my_results(request):
    results = Result.objects.select_related('quiz', 'quiz__course')\
                            .filter(user=request.user)\
                            .order_by('-completed_at')
    return render(request, 'quizzes/my_results.html', {'results': results})

@login_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.prefetch_related('answers')

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for question in questions:
            selected_id = request.POST.get(str(question.id))
            if not selected_id:
                continue
            try:
                answer = Answer.objects.get(id=selected_id, question=question)
            except Answer.DoesNotExist:
                continue
            if answer.is_correct:
                score += 1

        Result.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
        )

        return render(request, 'quizzes/quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'total': total,
        })

    return render(request, 'quizzes/quiz_detail.html', {
        'quiz': quiz,
        'questions': questions,
    })
