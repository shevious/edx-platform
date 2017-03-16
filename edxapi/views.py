#from django.shortcuts import render

# Create your views here.
"""
Course API Views
"""

from django.core.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from openedx.core.lib.api.paginators import NamespacedPageNumberPagination
from openedx.core.lib.api.view_utils import view_auth_classes, DeveloperErrorViewMixin

#from course_api.api import course_detail, list_courses
#from course_api.forms import CourseDetailGetForm, CourseListGetForm
#from course_api.serializers import CourseSerializer, CourseDetailSerializer
from .serializers import CreateCourseSerializer, UserProgressSerializer

from rest_framework.response import Response

from rest_framework import status

@view_auth_classes(is_authenticated=False)
#class CreateCourseView(DeveloperErrorViewMixin, RetrieveAPIView):
class CreateCourseView(DeveloperErrorViewMixin, CreateAPIView):
    """
    **Use Cases**

        Request create course

    **Example Requests**

        POST /edxapi/createcourse/

    **Response Values**

        Body consists of the following fields:

        * effort: A textual description of the weekly hours of effort expected
            in the course.
        * end: Date the course ends, in ISO 8601 notation
        * enrollment_end: Date enrollment ends, in ISO 8601 notation
        * enrollment_start: Date enrollment begins, in ISO 8601 notation
        * id: A unique identifier of the course; a serialized representation
            of the opaque key identifying the course.
        * media: An object that contains named media items.  Included here:
            * course_image: An image to show for the course.  Represented
              as an object with the following fields:
                * uri: The location of the image
        * name: Name of the course
        * number: Catalog number of the course
        * org: Name of the organization that owns the course
        * overview: A possibly verbose HTML textual description of the course.
            Note: this field is only included in the Course Detail view, not
            the Course List view.
        * short_description: A textual description of the course
        * start: Date the course begins, in ISO 8601 notation
        * start_display: Readably formatted start of the course
        * start_type: Hint describing how `start_display` is set. One of:
            * `"string"`: manually set by the course author
            * `"timestamp"`: generated from the `start` timestamp
            * `"empty"`: no start date is specified
        * pacing: Course pacing. Possible values: instructor, self

        Deprecated fields:

        * blocks_url: Used to fetch the course blocks
        * course_id: Course key (use 'id' instead)

    **Parameters:**

        username (optional):
            The username of the specified user for whom the course data
            is being accessed. The username is not only required if the API is
            requested by an Anonymous user.

    **Returns**

        * 200 on success with above fields.
        * 400 if an invalid parameter was sent or the username was not provided
          for an authenticated request.
        * 403 if a user who does not have permission to masquerade as
          another user specifies a username other than their own.
        * 404 if the course is not available or cannot be seen.

        Example response:

            {
                "blocks_url": "/api/courses/v1/blocks/?course_id=edX%2Fexample%2F2012_Fall",
                "media": {
                    "course_image": {
                        "uri": "/c4x/edX/example/asset/just_a_test.jpg",
                        "name": "Course Image"
                    }
                },
                "description": "An example course.",
                "end": "2015-09-19T18:00:00Z",
                "enrollment_end": "2015-07-15T00:00:00Z",
                "enrollment_start": "2015-06-15T00:00:00Z",
                "course_id": "edX/example/2012_Fall",
                "name": "Example Course",
                "number": "example",
                "org": "edX",
                "overview: "<p>A verbose description of the course.</p>"
                "start": "2015-07-17T12:00:00Z",
                "start_display": "July 17, 2015",
                "start_type": "timestamp",
                "pacing": "instructor"
            }
    """

    serializer_class = CreateCourseSerializer

    def create(self, request):
        return Response({ "result": "ok" , "course": {"id": "course-v1:lgek+temp+2017"}})

    def get_object(self):
        """
        Return the requested course object, if the user has appropriate
        permissions.
        """
#        requested_params = self.request.query_params.copy()
#        requested_params.update({'course_key': self.kwargs['course_key_string']})
#        form = CourseDetailGetForm(requested_params, initial={'requesting_user': self.request.user})
#        if not form.is_valid():
#            raise ValidationError(form.errors)

#        return course_detail(
#            self.request,
#            form.cleaned_data['username'],
#            form.cleaned_data['course_key'],
#        )
        return { "effort": "2 hours"}

@view_auth_classes(is_authenticated=False)
#class CreateCourseView(DeveloperErrorViewMixin, RetrieveAPIView):
class UserProgressView(DeveloperErrorViewMixin, CreateAPIView):
    """
    **Use Cases**

        Request user progress

    **Example Requests**

        POST /edxapi/userprogress/

    **Response Values**

        Body consists of the following fields:

        * progress: points in 100%
        * video_progress: points in 100%

    **Parameters:**
        id:
            Course ID
        username:
            unique user id

    **Returns**

        * 200 on success with above fields.
        * 400 if an invalid parameter was sent or the username was not provided
          for an authenticated request.
        * 403 if a user who does not have permission to masquerade as
          another user specifies a username other than their own.
        * 404 if the course is not available or cannot be seen.

        Example response:

            {
                "blocks_url": "/api/courses/v1/blocks/?course_id=edX%2Fexample%2F2012_Fall",
                "media": {
                    "course_image": {
                        "uri": "/c4x/edX/example/asset/just_a_test.jpg",
                        "name": "Course Image"
                    }
                },
                "description": "An example course.",
                "end": "2015-09-19T18:00:00Z",
                "enrollment_end": "2015-07-15T00:00:00Z",
                "enrollment_start": "2015-06-15T00:00:00Z",
                "course_id": "edX/example/2012_Fall",
                "name": "Example Course",
                "number": "example",
                "org": "edX",
                "overview: "<p>A verbose description of the course.</p>"
                "start": "2015-07-17T12:00:00Z",
                "start_display": "July 17, 2015",
                "start_type": "timestamp",
                "pacing": "instructor"
            }
    """

    serializer_class = UserProgressSerializer
#    def get_object(self):
#        return { "effort": "2 hours"}
#    def get(self, request):
#        return { "effort": "2 hours"}
#    def create(self, request):
#        print '#####3'
#        return super(CreateAPIView, self).create(request)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"progress":100, "video_progress":100,"input":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
#        return Response({ "progress": 100, "video_progress": 100, "course": {"id": "course-v1:lgek+temp+2017"}})
#        return Response({ "result": "ok" , "course": {"id": "course-v1:lgek+temp+2017"}})
#    def create(self, request):
#        return Response(self.create(request))
#        print '#####3'
#        print self.serializer_class.data
#        return Response(self.serializer_class.data)
#        return Response({ "result": "ok" , "course": {"id": "course-v1:lgek+temp+2017"}})
