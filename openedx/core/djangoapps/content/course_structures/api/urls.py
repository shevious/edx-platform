"""
Course Structure API URI specification.

Patterns here should simply point to version-specific patterns.
"""
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url(r'^v0/', include('openedx.core.djangoapps.content.course_structures.api.v0.urls', namespace='v0'))
)
