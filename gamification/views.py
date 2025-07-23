from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from users.models import UserProfile
from .models import QuizSession
from .forms import QuizForm
from ai_assistant.rag_utils import generate_quiz_with_gemini, validate_answer_semantically
from django.utils import timezone

@login_required
def gamification_dashboard(request):
    return render(request, "gamification/dashboard.html")

@login_required
def financial_quiz_view(request):
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, _("Please complete your profile to access the quiz."))
        return redirect('profile')

    if request.method == 'POST':
        questions = request.session.get('quiz_questions', [])
        unanswered = False
        answers = []

        for i, q in enumerate(questions):
            user_ans = request.POST.get(f"answer_{i}")
            if not user_ans:
                unanswered = True
                break
            answers.append((q, user_ans))

        if unanswered:
            messages.error(request, "⚠️ Please answer all questions before submitting the quiz.")
            return redirect('financial_quiz_view')

        # Evaluate answers
        score = 0
        feedback = []
        total = len(questions)

        for i, (q, user_ans) in enumerate(answers):
            is_correct, explanation = validate_answer_semantically(
                user_ans, q['answer'], q['question'], user_profile.language)
            feedback.append({
                "question": q['question'],
                "your_answer": user_ans,
                "is_correct": is_correct,
                "explanation": explanation
            })
            if is_correct:
                score += 1

        percentage = int((score / total) * 100)
        badge = "Gold" if percentage == 100 else "Silver" if percentage >= 80 else "Bronze" if percentage >= 60 else None

        # Save session
        QuizSession.objects.create(
            user=request.user,
            score=percentage,
            total_questions=total,
            correct_answers=score,
            badge=badge
        )

        return render(request, 'gamification/quiz_result.html', {
            'score': score,
            'total': total,
            'correct': score,
            'percentage': percentage,
            'badge': badge,
            'feedback': feedback
        })

    else:
        quiz_questions = generate_quiz_with_gemini(user_profile)
        request.session['quiz_questions'] = quiz_questions
        return render(request, 'gamification/quiz.html', {
            'quiz_questions': quiz_questions
        })



@login_required
def submit_quiz_view(request):
    if request.method == 'POST':
        questions = request.session.get('quiz_questions', [])
        form = QuizForm(request.POST, questions=questions)

        if form.is_valid():
            total = len(questions)
            correct = 0
            feedback = []

            for i, q in enumerate(questions):
                user_answer = form.cleaned_data.get(f"answer_{i}")
                correct_answer = q['answer']
                is_correct, explanation = validate_answer_semantically(
                    user_answer, correct_answer, q['question'], request.user.profile.language
                )
                if is_correct:
                    correct += 1
                feedback.append({
                    'question': q['question'],
                    'your_answer': user_answer,
                    'correct_answer': correct_answer,
                    'is_correct': is_correct,
                    'explanation': explanation
                })

            percentage = round((correct / total) * 100, 2) if total else 0
            badge = None
            if percentage == 100:
                badge = "Gold"
            elif percentage >= 80:
                badge = "Silver"
            elif percentage >= 60:
                badge = "Bronze"

            QuizSession.objects.create(
                user=request.user,
                score=percentage,
                total_questions=total,
                taken_on=timezone.now()
            )

            return render(request, 'gamification/quiz_result.html', {
                'score': percentage,
                'total': total,
                'correct': correct,
                'feedback': feedback,
                'badge': badge
            })

    return redirect('financial_quiz_view')

@login_required
def quiz_result_view(request):
    result = request.session.get('quiz_result', {})
    return render(request, "gamification/quiz_result.html", {
        "score": result.get('score'),
        "total": result.get('total'),
        "percentage": result.get('percentage'),
        "badge": result.get('badge'),
        "feedback": result.get('feedback', [])
    })

@login_required
def quiz_history_view(request):
    sessions = QuizSession.objects.filter(user=request.user).order_by('-taken_on')
    return render(request, 'gamification/quiz_history.html', {'sessions': sessions})
