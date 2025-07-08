from django.shortcuts import HttpResponse, render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib import messages

import json

from .models import Authors, Publishers, Titles, Reservation
from .forms import LoginForm, ReservationForm

def home(request):
    titles = Titles.objects.order_by('?')[:3]
    return render(request, './pages/home.html', {'titles': titles, 'active_nav': 'home'})

def authorsList(request):
    authors = Authors.objects.all()
    paginator = Paginator(authors, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, './pages/authors/authors_list.html', {'authors': page_obj, 'active_nav': 'authors', 'page_obj': page_obj})

def authorsDetails(request, id):
    author = get_object_or_404(Authors, au_id=id)
    return render(request, './pages/authors/authors_details.html', {'author': author, 'active_nav': 'authors'})

def publishersList(request):
    publishers = Publishers.objects.all()
    paginator = Paginator(publishers, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, './pages/publishers/publishers_list.html', {'publishers': page_obj, 'active_nav': 'publishers', 'page_obj': page_obj})

def publishersDetails(request, pubid):
    publisher = get_object_or_404(Publishers, pubid=pubid)
    return render(request, './pages/publishers/publishers_details.html', {'publisher': publisher, 'active_nav': 'publishers'})

def titlesList(request):
    titles = Titles.objects.all()
    paginator = Paginator(titles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, './pages/titles/titles_list.html', {'titles': page_obj, 'active_nav': 'titles', 'page_obj': page_obj})

def titlesDetails(request, isbn):
    title = get_object_or_404(Titles, isbn=isbn)
    return render(request, './pages/titles/titles_details.html', {'title': title, 'active_nav': 'titles'})

def titlesResa(request, isbn):
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        title = get_object_or_404(Titles, isbn=isbn)
        title_resa_all = Reservation.objects.filter(title=title, close=False)
        title_resa_date = list(title_resa_all.values('start', 'end'))
        title_resa_blocked = []

        # prepare blocked date for vanilla calendar format
        if title_resa_date:
            for resa in title_resa_date:
                date_blocked = f"{resa['start'].strftime('%Y-%m-%d')}:{resa['end'].strftime('%Y-%m-%d')}"
                title_resa_blocked.append(date_blocked)

        # get active resa number of user
        user_resa = Reservation.objects.filter(user=request.user, close=False)

        if request.method == 'POST':
            # form is based on reservation model / django then handle save directly
            form = ReservationForm(request.POST)

            # form validation and cleaning
            if form.is_valid():

                # check if user is the connected one
                r_user = form.cleaned_data.get('user')
                if r_user != request.user:
                    raise form.ValidationError("user issue")
                
                # check if title is the chosen one
                r_title = form.cleaned_data.get('title')
                if r_title != title:
                    raise form.ValidationError("title issue")
                
                # check if close status is false
                r_close = form.cleaned_data.get('close')
                if r_close != False:
                    raise form.ValidationError("status issue")

                resa = form.save()

                return redirect('profile')
        else:
            form = ReservationForm(initial={
                'user': request.user,
                'title': title,
                'close': False
            })
            print(form)


        return render(request, './pages/titles/titles_reservation.html', 
                    {'title': title,
                    'title_resa': json.dumps(title_resa_blocked),
                    'user_resa': user_resa,
                    'active_nav': 'titles',
                    'resa_form': form})

def authentication(request):
    form=LoginForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, './pages/authentication.html', {"form":form, 'active_nav': 'authentication'})

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('authentication')
    else:
        user = request.user
        active_resa = Reservation.objects.filter(user=request.user, close=False)
        past_resa = Reservation.objects.filter(user=request.user, close=True)
    return render(request, './pages/profile.html', {'user': user, 'active_resa': active_resa, 'past_resa': past_resa, 'active_nav': 'profile'})

def user_logout(request):
    logout(request)
    return redirect('home')

def admin_interface(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Access denied")
    
    titles = Titles.objects.all()
    return render(request, './pages/administration.html', {'titles': titles, 'active_nav': 'administration'})