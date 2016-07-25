from rest_framework.relations import StringRelatedField

from .models import Course, Hole, CourseSetup, CourseSetupHole
from rest_framework import serializers


class HoleDetailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Hole
        fields = ("url", "id", "course", "tee_name", "yardage", "par",
                  "default_hole_number", "default_handicap")


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ("url", "id", "name", "description")


class CourseDetailSerializer(serializers.HyperlinkedModelSerializer):

    holes = HoleDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ("url", "id", "name", "description", "holes")


class HoleListSerializer(serializers.HyperlinkedModelSerializer):

    course = StringRelatedField()

    class Meta:
        model = Hole
        fields = ("url", "id", "course", "tee_name", "yardage", "par",
                  "default_hole_number", "default_handicap")


class CourseSetupHoleSerializer(serializers.HyperlinkedModelSerializer):

    hole = HoleDetailSerializer()

    class Meta:
        model = CourseSetupHole
        fields = ("url", "id", "course_setup", "hole", "handicap", "hole_number")


class CourseSetupSerializer(serializers.HyperlinkedModelSerializer):

    holes = CourseSetupHoleSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSetup
        fields = ("url", "id", "name", "number_of_holes", "slope", "rating", "yardage", "holes")


class CourseSetupDetailSerializer(serializers.HyperlinkedModelSerializer):

    holes = CourseSetupHoleSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSetup
        fields = ("url", "id", "name", "number_of_holes", "slope", "rating", "holes")
