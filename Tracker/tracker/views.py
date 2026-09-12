
# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from .models import Expense
from .forms import ExpenseForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Category wise total for chart
    category_data = expenses.values('category').annotate(total=Sum('amount'))
    
    # Search
    q = request.GET.get('q')
    if q:
        expenses = expenses.filter(title__icontains=q)

    return render(request, 'tracker/dashboard.html', {
        'expenses': expenses, 'total': total, 'category_data': list(category_data)
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})

@login_required
def delete_expense(request, id):
    exp = get_object_or_404(Expense, id=id, user=request.user)
    exp.delete()
    return redirect('dashboard')