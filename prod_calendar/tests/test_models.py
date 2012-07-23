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


    def test_space_value_simple(self):
        """
        Test ``get_space_value`` for a simple single-value space

        """
        sv = SpaceValue(spaces=1,
                        value=Decimal('4.99'),
                        note='Note')
        sv.save()
        value = SpaceValue.get_space_value(1)
        self.assertEqual(sv.value, value)
    
    def test_space_value_no_values(self):
        """
        Test ``get_space_value`` when no ``SpaceValue`` rows exists.

        Should return None.

        """
        value = SpaceValue.get_space_value(1)
        self.assertEqual(None, value)

    def test_space_value_too_big(self):
        """
        Test ``get_space_value`` when index is large than defines spaces.
    
        Should return the biggest value.

        """
        sv = SpaceValue(spaces=1,
                        value=Decimal('6.99'),
                        note='Note')
        sv.save()
        sv = SpaceValue(spaces=1,
                        value=Decimal('4.99'),
                        note='Note')
        sv.save()
        value = SpaceValue.get_space_value(3)
        self.assertEqual(Decimal('6.99'), value)
