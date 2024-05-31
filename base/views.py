from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Leaderboard, UserInput, SustainabilityChallenge, UserChallenge, Reward
from django.contrib.auth.models import User
from .forms import UserInputForm,ChallengeLogForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.

'''rooms= [
    {'id':1, 'name': 'Eco Profile'},
    {'id':2, 'name': 'Calcualator'},
    {'id':3, 'name': 'Leaderboard'},
    {'id':4, 'name': 'Challenges'},
    {'id':5, 'name': 'Education'},
]'''

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password= request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist")
        
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesn't exist")


    context={'page':page}
    return render(request,'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request,'base/login_register.html', {'form':form})

def home(request):
    #rooms = Room.objects.all()
    #context = {'rooms': rooms}
    return render(request,'base/home.html')

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request,'base/room.html', context)

@login_required(login_url='login')
def calculateCF(request):
    form = UserInputForm()
    if request.method == 'POST':
        form=UserInputForm(request.POST)
        if form.is_valid():
            #form.save()
            user_input = form.save(commit=False)
            user_input.user = request.user
            user_input.cf = user_input.calculate_cf()  # Assuming you have a calculate_cf method in your model
            user_input.save()
            return JsonResponse({'result': user_input.cf})
    else:
        form = UserInputForm()

    context = {'form':form}
    return render(request, 'base/calcForm.html', context)


def leaderboard(request):
    leaderboard_entries = get_leaderboard_entries()
    return render(request, 'base/leaderboard.html', {'leaderboard_entries': leaderboard_entries})


def get_leaderboard_entries():
    # Retrieve leaderboard entries and order them by total_cf
    leaderboard_entries = Leaderboard.objects.all().order_by('total_cf')
    
    # Now, leaderboard_entries is a queryset sorted by total_cf
    return leaderboard_entries
@login_required(login_url='login')
def challenges(request):
    challenges = SustainabilityChallenge.objects.all()
    user_challenges = UserChallenge.objects.filter(user=request.user)

    context = {
        'challenges': challenges,
        'user_challenges': user_challenges,
    }

    return render(request, 'base/challenges.html', context)

def join_challenge(request, challenge_id):
    challenge = SustainabilityChallenge.objects.get(pk=challenge_id)

    # Check if the user is already participating in the challenge
    if UserChallenge.objects.filter(user=request.user, challenge=challenge).exists():
        messages.warning(request, "You are already participating in this challenge.")
    else:
        # Create a UserChallenge instance for the user and challenge
        user_challenge = UserChallenge(user=request.user, challenge=challenge, status='ongoing')
        user_challenge.save()
        messages.success(request, f"You have joined the {challenge.title} challenge!")

    return redirect('challenges')

@login_required
def log_action(request, challenge_id):
    challenge = get_object_or_404(SustainabilityChallenge, pk=challenge_id)

    challenge_completed = UserChallenge.objects.filter(user=request.user, challenge=challenge, status='completed').exists()

    form = ChallengeLogForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user_challenge = form.save(commit=False)
            user_challenge.challenge = challenge

            if form.cleaned_data['confirmed']:
                # Award points based on the challenge's points
                awarded_points = challenge.points_awarded
                rewards_entry, _ = Reward.objects.get_or_create(user=request.user)
                rewards_entry.total_points += awarded_points
                rewards_entry.save()

                user_challenge.points_awarded = awarded_points
                user_challenge.status = 'completed'

            user_challenge.user = request.user

            '''if hasattr(request.user, 'reward'):
                total_points_attained = request.user.reward.total_points
            else:
                total_points_attained = 0'''
            #calculate progress as a percentage
            # Assuming you have a Reward model with total_points field
            maximum_possible_points = 500  # Adjust this based on your requirements
            rewards_entry.progress = (rewards_entry.total_points / maximum_possible_points) * 100
            rewards_entry.save()

            # Update the progress field in the UserChallenge model
            #user_challenge.progress = progress_percentage
            user_challenge.user = request.user
            user_challenge.save()
            # Update progress for all UserChallenge objects for the current user
            update_user_challenge_progress(request.user)

            return redirect('challenges')  # Redirect to a success page or the challenge page

    context = {
        'form': form,
        'challenge': challenge,
        'challenge_completed': challenge_completed,
    }
    print("Rendering log_action.html")
    return render(request, 'base/log_action.html', context)

def update_user_challenge_progress(user):
    maximum_possible_points = 500  # Adjust this based on your requirements
    total_points_attained = user.reward.total_points if hasattr(user, 'reward') else 0

    # Iterate over existing UserChallenge objects for the current user and update progress
    existing_user_challenges = UserChallenge.objects.filter(user=user)
    for user_challenge in existing_user_challenges:
        progress_percentage = (total_points_attained / maximum_possible_points) * 100
        user_challenge.progress = progress_percentage
        user_challenge.save()


@login_required
def join_challenge(request, challenge_id):
    challenge = SustainabilityChallenge.objects.get(pk=challenge_id)
    user = request.user

    if user not in challenge.participants.all():
        challenge.participants.add(user)
        user_challenge, created = UserChallenge.objects.get_or_create(user=user, challenge=challenge)

        messages.success(request, f"You've joined the {challenge.title} challenge!")
    else:
        messages.warning(request, f"You're already participating in the {challenge.title} challenge!")

    return redirect('challenges')
