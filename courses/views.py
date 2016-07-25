from .models import Course, Hole, CourseSetup, CourseSetupHole
from events.models import Event
from .serializers import CourseSerializer, CourseDetailSerializer, CourseSetupSerializer, CourseSetupHoleSerializer, \
    HoleListSerializer, HoleDetailSerializer, CourseSetupDetailSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404


class CourseList(generics.ListCreateAPIView):
    """ API endpoint to view Courses
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    """ API endpoint to edit Courses
    """
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


class CourseSetupList(generics.ListCreateAPIView):
    """ API endpoint to view Course Setups
    """
    # queryset = CourseSetup.objects.all()
    serializer_class = CourseSetupSerializer

    def get_queryset(self):
        """
        Optionally restricts the list of course setups for a given event.
        """
        queryset = CourseSetup.objects.all()
        event_id = self.request.query_params.get('event', None)
        if event_id is not None:
            event = get_object_or_404(Event, pk=event_id)
            queryset = queryset.filter(pk__in=event.course_setups.all())
        return queryset


class CourseSetupDetail(generics.RetrieveUpdateDestroyAPIView):
    """ API endpoint to edit Course Setups
    """
    queryset = CourseSetup.objects.all()
    serializer_class = CourseSetupDetailSerializer


class HoleList(generics.ListCreateAPIView):
    serializer_class = HoleListSerializer

    def get_queryset(self):
        """
        Optionally restricts the list of holes for
        a course as determined by a course query parameter.
        """
        queryset = Hole.objects.all()
        course = self.request.query_params.get('course', None)
        tees = self.request.query_params.get('tees', None)
        if course is not None:
            queryset = queryset.filter(course=course)
        if tees is not None:
            queryset = queryset.filter(tee_name=tees)
        return queryset


class HoleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hole.objects.all()
    serializer_class = HoleDetailSerializer


class CourseSetupHoleList(generics.ListCreateAPIView):
    serializer_class = CourseSetupHoleSerializer

    def get_queryset(self):
        """
        Optionally restricts the list of holes for
        a course setup as determined by a setup query parameter.
        """
        queryset = CourseSetupHole.objects.all()
        setup = self.request.query_params.get('setup', None)
        if setup is not None:
            queryset = queryset.filter(course_setup=setup)
        return queryset


class CourseSetupHoleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseSetupHole.objects.all()
    serializer_class = CourseSetupHoleSerializer
