from rest_framework import generics

from .models import Policy
from .serializers import PolicySerializer


class PolicyList(generics.ListAPIView):
    """ API endpoint to view Policies
    """
    serializer_class = PolicySerializer
    queryset = Policy.objects.all()


class PolicyDetail(generics.RetrieveAPIView):
    serializer_class = PolicySerializer
    queryset = Policy.objects.all()
