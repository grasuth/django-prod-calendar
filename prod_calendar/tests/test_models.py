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

    def test_space_value_unicode(self):
        """
        Test unicode return value for ``SpaceValue``

        """
        sv = SpaceValue(spaces=1,
                        value=Decimal('6.99'),
                        note='Note')
        sv.save()
        self.assertEqual(u'Spaces: 1 Value: 6.99 (Note)', unicode(sv))


class DefaultsTest(TestCase):
    """
    Test Defaults defines default spaces


    """
    def test_defaults_singleton_create(self):
        """
        Test defaults can be created and is a singleton row.

        """
        defaults = Defaults(spaces=5)
        defaults.save()
        defaults2 = Defaults(spaces=6)
        defaults2.save()
        d_rows = Defaults.objects.all()
        self.assertEqual(1, len(d_rows))

    def test_defaults_cant_delete(self):
        """
        Test defaults can not be deleted.

        """
        defaults = Defaults(spaces=5)
        defaults.save()
        defaults.delete()
        d_rows = Defaults.objects.all()
        self.assertEqual(1, len(d_rows))

    def test_unicode(self):
        """
        Test defaults``unicode`` is as expected.

        """
        defaults = Defaults(spaces=5)
        defaults.save()
        self.assertEqual(u'Default spaces=5', unicode(defaults))
