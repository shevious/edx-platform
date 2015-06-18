"""
Course Structure api.py tests
"""
from openedx.core.djangoapps.content.course_structures.api.v0 import api, errors
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory, ItemFactory


class CourseStructureApiTests(ModuleStoreTestCase):
    """
    CourseStructure API Tests
    """
    def setUp(self):
        """
        Test setup
        """
        super(CourseStructureApiTests, self).setUp()
        self.course = CourseFactory.create()
        self.chapter = ItemFactory.create(
            parent_location=self.course.location, category='chapter', display_name="Week 1"
        )
        self.sequential = ItemFactory.create(
            parent_location=self.chapter.location, category='sequential', display_name="Lesson 1"
        )
        self.vertical = ItemFactory.create(
            parent_location=self.sequential.location, category='vertical', display_name='Subsection 1'
        )
        self.video = ItemFactory.create(
            parent_location=self.vertical.location, category="video", display_name="My Video"
        )
        self.video = ItemFactory.create(
            parent_location=self.vertical.location, category="html", display_name="My HTML"
        )

    def _expected_blocks(self, block_types=None, get_parent=False):
        """
        Construct expected blocks.

        Arguments:
            block_types: List of required block types. Possible values include sequential,
                         vertical, html, problem, video, and discussion. The type can also be
                         the name of a custom type of block used for the course.
            get_parent: Do we need to add info about parent of an xblock. We need this
                        because doesn't give parent info in case of unordered structure

        Returns:
            dict: Information about required block types.
        """
        blocks = {}

        def add_block(xblock):
            children = xblock.get_children()

            if block_types is None or xblock.category in block_types:

                parent = None
                if get_parent:
                    item = xblock.get_parent()
                    parent = unicode(item.location) if item is not None else None

                blocks[unicode(xblock.location)] = {
                    u'id': unicode(xblock.location),
                    u'type': xblock.category,
                    u'display_name': xblock.display_name,
                    u'format': xblock.format,
                    u'graded': xblock.graded,
                    u'parent': parent,
                    u'children': [unicode(child.location) for child in children]
                }

            for child in children:
                add_block(child)

        course = self.store.get_course(self.course.id, depth=None)
        add_block(course)

        return blocks

    def test_course_structure_with_no_block_types(self):
        """
        Verify that course_structure returns info for entire course.
        """
        structure = api.course_structure(self.course.id)
        expected = {
            u'root': unicode(self.course.location),
            u'blocks': self._expected_blocks()
        }

        self.maxDiff = None
        self.assertDictEqual(structure, expected)

    def test_course_structure_with_block_types(self):
        """
        Verify that course_structure returns info for required block_types only when specific block_types are requested.
        """
        block_types = ['html', 'video']
        structure = api.course_structure(self.course.id, block_types=block_types)
        expected = {
            u'root': unicode(self.course.location),
            u'blocks': self._expected_blocks(block_types=block_types, get_parent=True)
        }

        self.maxDiff = None
        self.assertDictEqual(structure, expected)
