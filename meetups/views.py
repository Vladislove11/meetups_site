from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth. decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Meetup, Participant
from .forms import RegistrationForm, SignUpForm, MeetupForm


# Create your views here.

def index(request):
    query = request.GET.get("q", "").strip()

    if query:
        meetups = Meetup.objects.filter(title__icontains=query).order_by("-date")
    else:
        meetups = Meetup.objects.all().order_by("-date")

    return render(request, "meetups/index.html", {
        "show_meetups": True,
        "meetups": meetups,
        "query": query,
    })

@login_required
def meetup_details(request, meetup_slug):
    selected_meetup = get_object_or_404(Meetup, slug=meetup_slug)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "register":
            participant, _ = Participant.objects.get_or_create(user=request.user)
            defaults = {"email": request.user.email or f"{request.user.username}@example.com"}
            selected_meetup.participants.add(participant)
        elif action == "unregister":
            participant = Participant.objects.filter(user=request.user).first()
            if participant:
                selected_meetup.participants.remove(participant)

        return redirect("meetup-detail", meetup_slug=meetup_slug)
    
    return render(request, "meetups/meetup-details.html", {
        "meetup": selected_meetup,
        "is_registered": selected_meetup.participants.filter(user=request.user).exists(),
    })

@login_required
def confirm_registration(request, meetup_slug):
    meetup = get_object_or_404(Meetup, slug=meetup_slug)

    return render(request, "meetups/registration-success.html", {
        "meetup": meetup,
    })

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = SignUpForm()
        
    return render(request, "meetups/register.html", {
        "form": form,
    })

@login_required
def edit_meetup(request, meetup_slug):
    meetup = get_object_or_404(Meetup, slug=meetup_slug)

    if meetup.creator != request.user:
        raise PermissionDenied("Вы не можете редактировать это собрание")
    
    if request.method == "POST":
        form = MeetupForm(request.POST, request.FILES, instance=meetup)

        if form.is_valid():
            form.save()
            return redirect("meetup-detail", meetup_slug=meetup_slug)
    else:
        form = MeetupForm(instance=meetup)

    return render(request, "meetups/edit-meetup.html", {
        "form": form,
        "meetup": meetup,
    })