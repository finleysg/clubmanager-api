from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from core.forms import Member2Form, User2Form
from core.models import Member
from events.models import Event


def index(request):
    context = {
        # TODO: the user object should go here
    }
    return render(request, "web/index.html", context)


@login_required
def account(request):
    context = {
        "changed": False
    }
    if request.method == 'POST':
        existing_user = User.objects.get(pk=request.user.id)
        existing_member = Member.objects.get(user_id=request.user.id)
        form1 = Member2Form(instance=existing_member, data=request.POST, files=request.FILES)
        form2 = User2Form(instance=existing_user, data=request.POST)
        if form1.is_valid() and form2.is_valid():
            form2.save()
            form1.save()
            context["changed"] = True
    else:
        form1 = Member2Form(instance=request.user.member)
        form2 = User2Form(instance=request.user)

    return render(request, "web/account.html", {"form1": form1, "form2": form2, "context": context})


def calendar(request):
    context = {
        # TODO: any data here?
    }
    return render(request, "web/calendar.html", context)


def contact(request):
    context = {
        # TODO: any data here?
    }
    return render(request, "web/contact.html", context)


@login_required
def dam_cup(request):
    context = {
        # TODO: any data here?
    }
    return render(request, "web/dam-cup.html", context)


@login_required
def directory(request):
    context = {
        # TODO: any data here?
    }
    return render(request, "web/directory.html", context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {
        "event": event
    }
    return render(request, "web/event-detail.html", context)


@login_required
def forum(request):
    context = {
        # TODO: any data here?
    }
    return render(request, "web/forum.html", context)


@login_required
def league_results(request):
    context = {
        # TODO: any data here?
    }
    return render(request, "web/league-results.html", context)


def local_rules(request):
    context = {
        # TODO: any data here?
    }
    return render(request, "web/local-rules.html", context)


@login_required
def major_results(request):
    context = {
        # TODO: any data here?
    }
    return render(request, "web/major-results.html", context)


@login_required
def match_play(request):
    context = {
        # TODO: any data here?
    }
    return render(request, "web/match-play.html", context)


def policies(request):
    context = {
        # TODO: any data here?
    }
    return render(request, "web/policies.html", context)


@login_required
def profile(request, user_id):
    this_profile = request.user
    if user_id != "0":
        this_profile = get_object_or_404(User, id=user_id)

    context = {
        "profile": this_profile,
        "member_image": this_profile.member.profile_image
    }
    return render(request, "web/profile.html", context)


@login_required
def profile_default(request):
    this_profile = request.user
    context = {
        "profile": this_profile,
        "member_image": this_profile.member.profile_image
    }
    return render(request, "web/profile.html", context)


@login_required
def register(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {
        "event": event
    }
    return render(request, "web/register.html", context)


@login_required
def results(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {
        "event": event
    }
    return render(request, "web/results.html", context)


@login_required
def season_long_points(request):
    context = {
        # TODO: any data here?
    }
    return render(request, "web/season-long-points.html", context)


@login_required
def teetimes(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {
        "event": event
    }
    return render(request, "web/results.html", context)
