# -*- coding: utf-8 -*-
"""
Tests for custom Teams Serializers.
"""
from django.core.paginator import Paginator

from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory

from lms.djangoapps.teams.tests.factories import CourseTeamFactory
from lms.djangoapps.teams.serializers import BaseTopicSerializer, PaginatedTopicSerializer, TopicSerializer


class TopicTestCase(ModuleStoreTestCase):
    """
    Base test class to set up a course with topics
    """
    def setUp(self):
        """
        Set up a course with a teams configuration.
        """
        super(TopicTestCase, self).setUp()
        self.course = CourseFactory.create(
            teams_configuration={
                "max_team_size": 10,
                "topics": [{u'name': u'Tøpic', u'description': u'The bést topic!', u'id': u'0'}]
            }
        )


class BaseTopicSerializerTestCase(TopicTestCase):
    """
    Tests for the `BaseTopicSerializer`, which should not serialize team count
    data.
    """
    def test_team_count_not_included(self):
        """Verifies that the `BaseTopicSerializer` does not include team count"""
        with self.assertNumQueries(0):
            serializer = BaseTopicSerializer(self.course.teams_topics[0])
            self.assertEqual(
                serializer.data,
                {u'name': u'Tøpic', u'description': u'The bést topic!', u'id': u'0'}
            )


class TopicSerializerTestCase(TopicTestCase):
    """
    Tests for the `TopicSerializer`, which should serialize team count data for
    a single topic.
    """
    def test_topic_with_no_team_count(self):
        """
        Verifies that the `TopicSerializer` correctly displays a topic with a
        team count of 0, and that it only takes one SQL query.
        """
        with self.assertNumQueries(1):
            serializer = TopicSerializer(self.course.teams_topics[0], context={'course_id': self.course.id})
            self.assertEqual(
                serializer.data,
                {u'name': u'Tøpic', u'description': u'The bést topic!', u'id': u'0', u'team_count': 0}
            )

    def test_topic_with_team_count(self):
        """
        Verifies that the `TopicSerializer` correctly displays a topic with a
        positive team count, and that it only takes one SQL query.
        """
        CourseTeamFactory.create(course_id=self.course.id, topic_id=self.course.teams_topics[0]['id'])
        with self.assertNumQueries(1):
            serializer = TopicSerializer(self.course.teams_topics[0], context={'course_id': self.course.id})
            self.assertEqual(
                serializer.data,
                {u'name': u'Tøpic', u'description': u'The bést topic!', u'id': u'0', u'team_count': 1}
            )

    def test_scoped_within_course(self):
        """Verify that team count is scoped within a course."""
        duplicate_topic = self.course.teams_topics[0]
        second_course = CourseFactory.create(
            teams_configuration={
                "max_team_size": 10,
                "topics": [duplicate_topic]
            }
        )
        CourseTeamFactory.create(course_id=self.course.id, topic_id=duplicate_topic[u'id'])
        CourseTeamFactory.create(course_id=second_course.id, topic_id=duplicate_topic[u'id'])
        with self.assertNumQueries(1):
            serializer = TopicSerializer(self.course.teams_topics[0], context={'course_id': self.course.id})
            self.assertEqual(
                serializer.data,
                {u'name': u'Tøpic', u'description': u'The bést topic!', u'id': u'0', u'team_count': 1}
            )


class PaginatedTopicSerializerTestCase(TopicTestCase):
    """
    Tests for the `PaginatedTopicSerializer`, which should serialize team count
    data for many topics with constant time SQL queries.
    """
    PAGE_SIZE = 5

    def _merge_dicts(self, first, second):
        """Convenience method to merge two dicts in a single expression"""
        result = first.copy()
        result.update(second)
        return result

    def setup_topics(self, num_topics=5, teams_per_topic=0):
        """
        Helper method to set up topics on the course.  Returns a list of
        created topics.
        """
        self.course.teams_configuration['topics'] = []
        topics = [
            {u'name': u'Tøpic {}'.format(i), u'description': u'The bést topic! {}'.format(i), u'id': unicode(i)}
            for i in xrange(num_topics)
        ]
        for i in xrange(num_topics):
            topic_id = unicode(i)
            self.course.teams_configuration['topics'].append(topics[i])
            for _ in xrange(teams_per_topic):
                CourseTeamFactory.create(course_id=self.course.id, topic_id=topic_id)
        return topics

    def assert_serializer_output(self, topics, num_teams_per_topic, num_queries):
        """
        Verify that the serializer produced the expected topics.
        """
        with self.assertNumQueries(num_queries):
            page = Paginator(self.course.teams_topics, self.PAGE_SIZE).page(1)
            serializer = PaginatedTopicSerializer(instance=page, context={'course_id': self.course.id})
            self.assertEqual(
                serializer.data['results'],
                [self._merge_dicts(topic, {u'team_count': num_teams_per_topic}) for topic in topics]
            )

    def test_no_topics(self):
        """
        Verify that we return no results and make no SQL queries for a page
        with no topics.
        """
        self.course.teams_configuration['topics'] = []
        self.assert_serializer_output([], num_teams_per_topic=0, num_queries=0)

    def test_topics_with_no_team_counts(self):
        """
        Verify that we serialize topics with no team count, making only one SQL
        query.
        """
        topics = self.setup_topics(teams_per_topic=0)
        self.assert_serializer_output(topics, num_teams_per_topic=0, num_queries=1)

    def test_topics_with_team_counts(self):
        """
        Verify that we serialize topics with a positive team count, making only
        one SQL query.
        """
        teams_per_topic = 10
        topics = self.setup_topics(teams_per_topic=teams_per_topic)
        self.assert_serializer_output(topics, num_teams_per_topic=teams_per_topic, num_queries=1)

    def test_subset_of_topics(self):
        """
        Verify that we serialize a subset of the course's topics, making only
        one SQL query.
        """
        teams_per_topic = 10
        topics = self.setup_topics(num_topics=self.PAGE_SIZE + 1, teams_per_topic=teams_per_topic)
        self.assert_serializer_output(topics[:self.PAGE_SIZE], num_teams_per_topic=teams_per_topic, num_queries=1)

    def test_scoped_within_course(self):
        """Verify that team counts are scoped within a course."""
        teams_per_topic = 10
        first_course_topics = self.setup_topics(num_topics=self.PAGE_SIZE, teams_per_topic=teams_per_topic)
        duplicate_topic = first_course_topics[0]
        second_course = CourseFactory.create(
            teams_configuration={
                "max_team_size": 10,
                "topics": [duplicate_topic]
            }
        )
        CourseTeamFactory.create(course_id=second_course.id, topic_id=duplicate_topic[u'id'])
        self.assert_serializer_output(first_course_topics, num_teams_per_topic=teams_per_topic, num_queries=1)
