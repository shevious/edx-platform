"""
Course API URLs
"""
from django.conf import settings
from django.conf.urls import patterns, url, include

#from course_api.views import CourseDetailView, CourseListView
from .views import CreateCourseView, UserProgressView

urlpatterns = patterns(
    '',
    url(r'^createcourse/$', CreateCourseView.as_view(), name="course-list"),
    url(r'^userprogress/$', UserProgressView.as_view()),
#    url(r'', include('course_api.blocks.urls'))
)
