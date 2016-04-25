from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from events.models import Event


def index(request):
    context = {
        # TODO: the user object should go here
    }
    return render(request, "web/index.html", context)


@login_required
def account(request):
    context = {
        # TODO: any data here?
    }
    return render(request, "web/account.html", context)


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
def profile(request):
    context = {
        # TODO: any data here?
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
