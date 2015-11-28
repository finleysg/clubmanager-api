from django.shortcuts import render


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
