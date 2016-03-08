"""
Module Placeholder Docstring
"""
import unittest

import cgi
import mock
from django.test.client import Client
from django.utils.translation import ugettext as _
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from xblock.field_data import DictFieldData

from .submit_and_compare import SubmitAndCompareXBlock


class SubmitAndCompareXblockTestCase(unittest.TestCase):
    # pylint: disable=too-many-instance-attributes, too-many-public-methods
    """
    A complete suite of unit tests for the Free-text Response XBlock
    """
    @classmethod
    def make_an_xblock(cls, **kw):
        """
        Helper method that creates a Free-text Response XBlock
        """
        course_id = SlashSeparatedCourseKey('foo', 'bar', 'baz')
        runtime = mock.Mock(course_id=course_id)
        scope_ids = mock.Mock()
        field_data = DictFieldData(kw)
        xblock = SubmitAndCompareXBlock(runtime, field_data, scope_ids)
        xblock.xmodule_runtime = runtime
        return xblock

    def setUp(self):
        # pylint: disable=super-method-not-called
        self.xblock = SubmitAndCompareXblockTestCase.make_an_xblock()
        self.client = Client()

    def test_student_view(self):
        # pylint: disable=protected-access
        """
        Checks the student view for student specific instance variables.
        """
        student_view_html = self.student_view_html()
        self.assertIn(self.xblock.display_name, student_view_html)
        self.assertIn(
            self.xblock._get_body(self.xblock.question_string),
            student_view_html,
        )
        self.assertIn(self.xblock._get_problem_progress(), student_view_html)

    def test_studio_view(self):
        """
        Checks studio view for instance variables specified by the instructor.
        """
        studio_view_html = self.studio_view_html()
        self.assertIn(self.xblock.display_name, studio_view_html)
        self.assertIn(
            cgi.escape(self.xblock._get_body(self.xblock.question_string)),
            studio_view_html,
        )
        self.assertIn(str(self.xblock.max_attempts), studio_view_html)

    def test_initialization_variables(self):
        """
        Checks that all instance variables are initialized correctly
        """
        self.assertEquals('Submit and Compare', self.xblock.display_name)
        self.assertIn(
            'Before you begin the simulation',
            self.xblock.question_string,
        )
        self.assertEquals(0.0, self.xblock.score)
        self.assertEquals(0, self.xblock.max_attempts)
        self.assertEquals('', self.xblock.student_answer)
        self.assertEquals(0, self.xblock.count_attempts)

    def student_view_html(self):
        """
        Helper method that returns the html of student_view
        """
        return self.xblock.student_view().content

    def studio_view_html(self):
        """
        Helper method that returns the html of studio_view
        """
        return self.xblock.studio_view(context=None).content

    def test_problem_progress_score_zero_weight_singular(self):
        # pylint: disable=invalid-name, protected-access
        """
        Tests that the the string returned by get_problem_progress
        when the weight of the problem is singular, and the score is zero
        """
        self.xblock.score = 0
        self.xblock.weight = 1
        self.assertEquals(
            _('1 point possible'),
            self.xblock._get_problem_progress(),
        )

    def test_problem_progress_score_zero_weight_plural(self):
        # pylint: disable=invalid-name, protected-access
        """
        Tests that the the string returned by get_problem_progress
        when the weight of the problem is plural, and the score is zero
        """
        self.xblock.score = 0
        self.xblock.weight = 3
        self.assertEquals(
            _('3 points possible'),
            self.xblock._get_problem_progress(),
        )

    def test_problem_progress_score_positive_weight_singular(self):
        # pylint: disable=invalid-name, protected-access
        """
        Tests that the the string returned by get_problem_progress
        when the weight of the problem is singular, and the score is positive
        """
        self.xblock.score = 1
        self.xblock.weight = 1
        self.assertEquals(
            _('1/1 point'),
            self.xblock._get_problem_progress(),
        )

    def test_problem_progress_score_positive_weight_plural(self):
        # pylint: disable=invalid-name, protected-access
        """
        Tests that the the string returned by get_problem_progress
        when the weight of the problem is plural, and the score is positive
        """
        self.xblock.score = 1.5
        self.xblock.weight = 3
        self.assertEquals(
            _('1.5/3 points'),
            self.xblock._get_problem_progress(),
        )
