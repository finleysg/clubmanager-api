from rest_framework import permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import get_object_or_404

from .models import Club, Member
from .serializers import ClubSerializer, MemberSerializer

@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def api_root(request):
    return Response({
        'clubs': reverse('club-list', request=request),
        'members': reverse('member-list', request=request),
        'courses': reverse('course-list', request=request),
        'course-setups': reverse('coursesetup-list', request=request),
        'holes': reverse('hole-list', request=request),
        'course-setup-holes': reverse('coursesetuphole-list', request=request),
        'events': reverse('event-list', request=request),
        'event-templates': reverse('eventtemplate-list', request=request),
        'policies': reverse('policy-list', request=request),
    })


class ClubList(generics.ListAPIView):
    """ API endpoint to view Clubs
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class ClubDetail(generics.RetrieveUpdateAPIView):
    """ API endpoint to edit Clubs
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class MemberList(generics.ListAPIView):
    """ API endpoint to view Members
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class MemberDetail(generics.RetrieveAPIView):
    """ API endpoint to view a single Member
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


@api_view(['GET', ])
@permission_classes((permissions.IsAuthenticated,))
def friends(request):
    """ API endpoint to view the current member's favorites
    """
    member = get_object_or_404(Member, pk=request.user.id)
    serializer = MemberSerializer(member.favorites, context={'request': request}, many=True)
    return Response(serializer.data)
