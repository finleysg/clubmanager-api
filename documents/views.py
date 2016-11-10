from rest_framework import generics
# from datetime import datetime

from .models import Document
from .serializers import DocumentSerializer


class DocumentDetail(generics.RetrieveAPIView):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()


class DocumentList(generics.ListAPIView):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    # def get_queryset(self):
    #     today = datetime.now()
    #     queryset = Document.objects.all()
    #     queryset = queryset.filter(starts__lte=today, expires__gte=today)
    #     print(queryset.query)
    #     return queryset
