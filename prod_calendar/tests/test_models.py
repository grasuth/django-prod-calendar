from decimal import Decimal
from django.test import TestCase

from prod_calendar.models import *

class SpaceValueTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_space_value_basic(self):
        """
        Tests SpaceValue create.

        """
        sv = SpaceValue(spaces=1,
                        value=Decimal('4.99'),
                        note='Note')
        sv.save()
        self.assertEqual(1, sv.spaces)
        self.assertEqual(Decimal('4.99'), sv.value)
        self.assertEqual('Note', sv.note)

