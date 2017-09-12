from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Document, Sponsor, Photo
from .serializers import DocumentDetailSerializer, SponsorSerializer, PhotoDetailSerializer, PhotoSerializer


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentDetailSerializer
    queryset = Document.objects.all()
    parser_classes = (MultiPartParser, FormParser, )


class DocumentList(generics.ListCreateAPIView):
    serializer_class = DocumentDetailSerializer
    parser_classes = (MultiPartParser, FormParser, )

    def get_queryset(self):
        queryset = Document.objects.all()
        year = self.request.query_params.get('year', None)
        doc_type = self.request.query_params.get('dtype', None)
        event_type = self.request.query_params.get('etype', None)
        if year is not None:
            queryset = queryset.filter(year=year)
        if doc_type is not None:
            queryset = queryset.filter(document_type=doc_type)
        if event_type is not None:
            queryset = queryset.filter(event__event_type=event_type)
        return queryset.order_by('title')


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoDetailSerializer
    queryset = Photo.objects.all()
    parser_classes = (MultiPartParser, FormParser, )


class PhotoList(generics.ListCreateAPIView):
    serializer_class = PhotoDetailSerializer
    parser_classes = (MultiPartParser, FormParser, )

    def get_queryset(self):
        queryset = Photo.objects.all()
        year = self.request.query_params.get('year', None)
        pic_type = self.request.query_params.get('ptype', None)
        event_type = self.request.query_params.get('etype', None)
        if year is not None:
            queryset = queryset.filter(year=year)
        if pic_type is not None:
            queryset = queryset.filter(photo_type=pic_type)
        if event_type is not None:
            queryset = queryset.filter(event__event_type=event_type)
        return queryset.order_by('title')


class SponsorList(generics.ListAPIView):
    serializer_class = SponsorSerializer
    queryset = Sponsor.objects.all()
