import calendar

from django.db.models import Sum 
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import GeneralCategory, Batch
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import Insert_Amount
import random
import datetime
import numpy as np
import pandas as pd
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    #return HttpResponse("<h1>Brasil</h1>")
    text = "DJANGO APP"
    return render(request, 'index.html', {'text': text})

@login_required
def insert(request):

    if request.method == 'GET':
        return render(request, 'insert.html', {
            'form': Insert_Amount
        })
    else:
        try:
            
            credit = TypeC.objects.get(name="Credito")

            form = Insert_Amount(request.POST)
            batch = add_batch()
            
            batchid = Batch.objects.get(batch_number=batch)
            moneyflow = form.save(commit=False)

            if moneyflow.type is None:
                moneyflow.pay_date = moneyflow.done_date

            moneyflow.user = request.user
            moneyflow.batch = batchid
            moneyflow.save()
            return redirect('/insert/')
        except ValueError:
            return render(request, 'insert.html', {
                'form': Insert_Amount,
                'error': 'No data'
            })

def add_batch():

    current_date = datetime.datetime.now()
    day = current_date.day
    month = current_date.month
    year = current_date.year
    number = random.randint(0, 99)
    digits = ['A', 'B', 'C', 'D', 'E', 'F']

    batch = "{}{}{}{}".format(year, month, day, number)

    if len(batch) == 8:
        d9 = random.randint(0, 5)
        d10 = random.randint(0, 5)
        batch = "{}{}{}".format(batch, digits[d9], digits[d10])

    elif len(batch) == 9:
        d10 = random.randint(0, 5)
        batch = "{}{}".format(batch, digits[d10])

    b = Batch(batch_number=batch, insert_date=datetime.datetime.now())
    b.save()
    return batch

@login_required
def show(request):

    if request.method == 'GET':
        today = datetime.datetime.now()
        income = MoneyInformation.objects.filter(user=request.user, transaction_type=1, detained=0,
                                                 pay_date__month=today.month, pay_date__year=today.year)
        outcome = MoneyInformation.objects.filter(user=request.user, transaction_type=0, detained=0,
                                                  pay_date__month=today.month, pay_date__year=today.year)

        flow = get_balance(income, outcome)
        total_income = flow['income']
        total_outcome = flow['outcome']
        balance = flow['balance']

        return render(request, 'show.html', {'income': income, 'outcome': outcome,
                                             'total_income': total_income, 'total_outcome': total_outcome,
                                             'balance': balance})
    else:

        filterdate = request.POST['date']
        new_dates = convert_date(filterdate)
        income = MoneyInformation.objects.filter(user=request.user, transaction_type=1, detained=0,
                                                 pay_date__range=(new_dates[0], new_dates[1]))
        outcome = MoneyInformation.objects.filter(user=request.user, transaction_type=0, detained=0,
                                                  pay_date__range=(new_dates[0], new_dates[1]))

        flow = get_balance(income, outcome)

        total_income = flow['income']
        total_outcome = flow['outcome']
        balance = flow['balance']

        return render(request, 'show.html', {'income': income, 'outcome': outcome,
                                             'total_income': total_income, 'total_outcome': total_outcome,
                                             'balance': balance})

@login_required
def update(request, id):
    if  request.method == 'GET':
        move = get_object_or_404(MoneyInformation,pk=id)
        form = Update_Moneyflow(instance=move)
        return render(request, 'update.html', {'form': form, 'move':move})
    else:
        move = get_object_or_404(MoneyInformation,pk=id)
        form = Update_Moneyflow(request.POST, instance=move)
        form.save()
        return redirect('/show/')

@login_required
def delete(request, id):
    
    
    task = get_object_or_404(MoneyInformation, pk=id, user=request.user)
    task.delete()
    return redirect('/show')

@login_required
def move_detail(request, id):

    move = get_object_or_404(MoneyInformation,pk=id)
    return render(request,'details.html', {'move': move})

def get_balance(income, outcome):

    total_income = income.aggregate(Sum('amount'))
    total_outcome = outcome.aggregate(Sum('amount'))

    total_outcome = total_outcome['amount__sum']
    total_income = total_income['amount__sum']

    if total_outcome is None and total_outcome is None:
        total_income = 0
        total_outcome = 0
    elif total_income is None:
        total_income = 0
    elif total_outcome is None:
        total_outcome = 0

    balance = total_income - total_outcome

    flow = {'income': total_income, 'outcome': total_outcome, 'balance': balance}
    return flow




def convert_date(filterdate):
    dates = []

    ndate = '{}-01'.format(filterdate)
    begin_date = datetime.datetime.strptime(ndate, '%Y-%m-%d').date()
    ndays = calendar.monthrange(begin_date.year, begin_date.month)
    edate = '{}-{}'.format(filterdate, ndays[1])
    end_date = datetime.datetime.strptime(edate, '%Y-%m-%d').date()

    dates.append(begin_date)
    dates.append(end_date)

    return dates

@login_required
def withheld(request):


    detained = MoneyInformation.objects.filter(user=request.user,detained=1)

    return render(request, 'withheld.html', {'detained': detained})

#Sign up en la app
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
         if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1']) #Obtener del post para crear usuario
                user.save() #guardar en la Base de datos usuario
                #login(request, user)
                return redirect('/login/')
            except:
                HttpResponse('Error')
         return render(request, 'signup.html', {
             'form': UserCreationForm,
             'error': 'No coinciden'
            })

#Log in
def log_in(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'],
                     password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Vanpiro no esite'
            })
        else:
            login(request, user)
            return redirect('/')

#log out
def log_out(request):
        logout(request)
        return redirect('/')


def about(request):
    return HttpResponse("<h2>About</h2>")

def general(request):

    #general = list(GeneralCategory.objects.values())
    general = GeneralCategory.objects.all()
    #general = GeneralCategory.objects.get(id=id)
    #general = get_object_or_404(GeneralCategory, id=id)
    return render(request, 'general.html', {
        'general': general
    })
    #return JsonResponse(general, safe=False)
    #return HttpResponse('Categoria: %s' % general.name)