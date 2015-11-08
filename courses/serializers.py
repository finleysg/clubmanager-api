from .models import Course, Hole, CourseSetup, CourseSetupHole
from rest_framework import serializers


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ("url", "id", "name", "description")


class HoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hole
        fields = ("url", "id", "course", "default_hole_number", "tee_name", "par", "default_handicap", "yardage")


class CourseSetupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseSetup
        fields = ("url", "id", "name", "holes", "slope", "rating", "is_standard")


class CourseSetupHoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseSetupHole
        fields = ("url", "id", "course_setup", "hole", "handicap", "hole_number")
