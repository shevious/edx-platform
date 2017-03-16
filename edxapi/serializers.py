
#from django.contrib.auth.models import User, Group
#from rest_framework import serializers
#

#class UserSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = User
#        fields = ('url', 'username', 'email', 'groups')
#

#class GroupSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = Group
#        fields = ('url', 'name')
#


"""
CreateCourse API Serializers.  Representing course catalog data
"""

import urllib

from django.core.urlresolvers import reverse
from rest_framework import serializers

from openedx.core.djangoapps.models.course_details import CourseDetails
from openedx.core.lib.api.fields import AbsoluteURLField

class CreateCourseSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for Course objects providing minimal data about the course.
    Compare this with CourseDetailSerializer.
    """

#    blocks_url = serializers.SerializerMethodField()
    id = serializers.CharField()
#    end = serializers.DateTimeField()
#    enrollment_start = serializers.DateTimeField()
#    enrollment_end = serializers.DateTimeField()
#    id = serializers.CharField()  # pylint: disable=invalid-name
#    media = _CourseApiMediaCollectionSerializer(source='*')
#    name = serializers.CharField(source='display_name_with_default_escaped')
#    number = serializers.CharField(source='display_number_with_default')
#    org = serializers.CharField(source='display_org_with_default')
#    short_description = serializers.CharField()
#    start = serializers.DateTimeField()
#    start_display = serializers.CharField()
#    start_type = serializers.CharField()
#    pacing = serializers.CharField()

    # 'course_id' is a deprecated field, please use 'id' instead.
#    course_id = serializers.CharField(source='id', read_only=True)

#    def get_blocks_url(self, course_overview):
#        """
#        Get the representation for SerializerMethodField `blocks_url`
#        """
#        base_url = '?'.join([
#            reverse('blocks_in_course'),
#            urllib.urlencode({'course_id': course_overview.id}),
#        ])
#        return self.context['request'].build_absolute_uri(base_url)


    def create(self, validated_data):
        print validated_data
        return validated_data
#        return {"effort" : "3 hours"}


class UserProgressSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for Course objects providing minimal data about the course.
    Compare this with CourseDetailSerializer.
    """

#    blocks_url = serializers.SerializerMethodField()
    id = serializers.CharField()
    username = serializers.CharField()
#    end = serializers.DateTimeField()
#    enrollment_start = serializers.DateTimeField()
#    enrollment_end = serializers.DateTimeField()
#    id = serializers.CharField()  # pylint: disable=invalid-name
#    media = _CourseApiMediaCollectionSerializer(source='*')
#    name = serializers.CharField(source='display_name_with_default_escaped')
#    number = serializers.CharField(source='display_number_with_default')
#    org = serializers.CharField(source='display_org_with_default')
#    short_description = serializers.CharField()
#    start = serializers.DateTimeField()
#    start_display = serializers.CharField()
#    start_type = serializers.CharField()
#    pacing = serializers.CharField()

    # 'course_id' is a deprecated field, please use 'id' instead.
#    course_id = serializers.CharField(source='id', read_only=True)

#    def get_blocks_url(self, course_overview):
#        """
#        Get the representation for SerializerMethodField `blocks_url`
#        """
#        base_url = '?'.join([
#            reverse('blocks_in_course'),
#            urllib.urlencode({'course_id': course_overview.id}),
#        ])
#        return self.context['request'].build_absolute_uri(base_url)

    def create(self, validated_data):
        print validated_data
        return validated_data
