
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SavingsGoal, Contribution
from .forms import SavingsGoalForm, ContributionForm
from django.http import JsonResponse

@login_required
def index(request):
    goals = SavingsGoal.objects.filter(user=request.user).order_by('deadline')
    form = SavingsGoalForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        goal = form.save(commit=False)
        goal.user = request.user
        goal.save()
        return redirect('savings:index')
    return render(request, 'savings/index.html', {
        'form': form,
        'goals': goals,
        'contribution_form': ContributionForm()
    })

@login_required
def contribute(request, goal_id):
    goal = get_object_or_404(SavingsGoal, pk=goal_id, user=request.user)
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.goal = goal
            contribution.save()
            goal.saved_amount += contribution.amount
            goal.save()
    return redirect('savings:index')

@login_required
def mark_complete(request, goal_id):
    goal = get_object_or_404(SavingsGoal, pk=goal_id, user=request.user)
    goal.completed = True
    goal.save()
    return redirect('savings:index')

from django.http import HttpResponse
import csv


@login_required
def export_csv(request):
    goals = SavingsGoal.objects.filter(user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="savings_goals.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Target', 'Saved', 'Progress (%)', 'Deadline', 'Monthly Needed', 'Completed'])
    for g in goals:
        progress = g.progress_percent()
        monthly = g.monthly_saving_needed() if hasattr(g, 'monthly_saving_needed') else "-"
        writer.writerow([g.title, g.description, g.target_amount, g.saved_amount, progress, g.deadline, monthly, g.completed])
    return response
