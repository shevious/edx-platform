"""
Course API URLs
"""
from django.conf import settings
from django.conf.urls import patterns, url, include

from course_api.views import CourseDetailView, CourseListView

urlpatterns = patterns(
    '',
    url(r'^quickstart/$', CourseListView.as_view(), name="course-list"),
#    url(r'', include('course_api.blocks.urls'))
)
