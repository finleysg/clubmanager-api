from rest_framework import generics

from .models import Document
from .serializers import DocumentSerializer


class DocumentDetail(generics.RetrieveAPIView):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()


class DocumentList(generics.ListAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = Document.objects.all()
        year = self.request.query_params.get('year', None)
        doc_type = self.request.query_params.get('type', None)
        if year is not None:
            queryset = queryset.filter(year=year)
        if doc_type is not None:
            queryset = queryset.filter(document_type=doc_type)
        return queryset
