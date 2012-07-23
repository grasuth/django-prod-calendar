from datetime import date
from decimal import Decimal
from django.conf import settings
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
        self.assertEqual(6, Defaults.get_default_spaces())

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


class TestSlot(TestCase):

    def test_slot_create_simple(self):
        """
        Test ``Slot`` model constructor.

        """
        slot = Slot(start_date=date(2012, 7, 19),
                    spaces=5,
                    note='SlotNote')
        slot.save()
        self.assertEqual(date(2012, 7, 19), slot.start_date)
        self.assertEqual(5, slot.spaces)
        self.assertEqual(0, slot.used_spaces)
        self.assertEqual('SlotNote', slot.note)

    def test_slot_book_space_basic(self):
        """
        Test booking a space in a slot.

        """
        slot = Slot(start_date=date(2012, 7, 19),
                    spaces=5,
                    note='SlotNote')
        slot.save()
        sv = SpaceValue(spaces=1,
                        value=Decimal('4.99'),
                        note='Note')
        sv.save()
        val = slot.book_space()
        self.assertEqual(1, slot.used_spaces)
        self.assertEqual(Decimal('4.99'), val)

    def test_slot_book_no_space(self):
        """
        Test booking a space in a slot when there is no space.

        ``book_space`` should return None.

        """
        slot = Slot(start_date=date(2012, 7, 19),
                    spaces=5,
                    used_spaces=5,
                    note='SlotNote')
        slot.save()
        sv = SpaceValue(spaces=1,
                        value=Decimal('4.99'),
                        note='Note')
        sv.save()
        val = slot.book_space()
        self.assertEqual(5, slot.used_spaces)
        self.assertEqual(None, val)

    def test_slot_get_space_value(self):
        """
        Test ``get_space_value`` adds multiple slot values.

        """
        slot = Slot(start_date=date(2012, 7, 19),
                    spaces=2,
                    used_spaces=0,
                    note='SlotNote')
        slot.save()
        sv = SpaceValue(spaces=1,
                        value=Decimal('4.99'),
                        note='Note')
        sv.save()
        sv2 = SpaceValue(spaces=1,
                        value=Decimal('11.99'),
                        note='Note')
        sv2.save()
        val = slot.get_space_value(2)
        self.assertEqual(Decimal('16.98'), val)

    def test_book_2_spaces(self):
        """
        Test ``get_space_value`` adds multiple slot values.

        """
        defaults = Defaults(spaces=5)
        defaults.save()
        slot = Slot(start_date=date(2012, 7, 19),
                    spaces=2,
                    used_spaces=0,
                    note='SlotNote')
        slot.save()
        sv = SpaceValue(spaces=1,
                        value=Decimal('4.99'),
                        note='Note')
        sv.save()
        sv2 = SpaceValue(spaces=1,
                        value=Decimal('11.99'),
                        note='Note')
        sv2.save()
        val = slot.book_space(2)
        self.assertEqual(Decimal('16.98'), val)
        self.assertEqual(2, slot.used_spaces)

    def test_get_slot_for_date_exists(self):
        """
        Test get_slot_for_date returns actual existing slot.

        """
        defaults = Defaults(spaces=5)
        defaults.save()
        slot = Slot(start_date=date(2012, 7, 19),
                    spaces=2,
                    used_spaces=0,
                    note='SlotNote')
        slot.save()
        sv = SpaceValue(spaces=1,
                        value=Decimal('4.99'),
                        note='Note')
        sv.save()
        ret_slot = Slot.get_slot_for_date(date(2012, 7, 19))
        self.assertEqual(slot, ret_slot)

    def test_slot_for_date_missing(self):
        """
        Test ``get_slot_for_date`` when slot doesn't exist

        """
        settings.SLOT_LENGTH_DAYS = 1
        defaults = Defaults(spaces=5)
        defaults.save()
        slot = Slot(start_date=date(2012, 7, 19),
                    spaces=2,
                    used_spaces=0,
                    note='SlotNote')
        slot.save()
        sv = SpaceValue(spaces=1,
                        value=Decimal('4.99'),
                        note='Note')
        sv.save()
        ret_slot = Slot.get_slot_for_date(date(2012, 7, 21))
        self.assertEqual(date(2012, 7, 21), ret_slot.start_date)
        self.assertEqual(5, ret_slot.spaces)
        ret_slot = Slot.get_slot_for_date(date(2012, 7, 20))
        self.assertEqual(date(2012, 7, 20), ret_slot.start_date)
        self.assertEqual(5, ret_slot.spaces)
        self.assertEqual(3, Slot.objects.all().count())

    def test_slot_for_date_missing_no_slots(self):
        """
        Test ``get_slot_for_date`` when no slots defined.

        """
        settings.SLOT_LENGTH_DAYS = 1
        settings.SLOT_START_DATE = '07/01/2012'
        settings.DATE_INPUT_FORMATS = ('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y')
        defaults = Defaults(spaces=5)
        defaults.save()
        sv = SpaceValue(spaces=1,
                        value=Decimal('4.99'),
                        note='Note')
        sv.save()
        ret_slot = Slot.get_slot_for_date(date(2012, 7, 21))
        self.assertEqual(date(2012, 7, 21), ret_slot.start_date)
        self.assertEqual(5, ret_slot.spaces)
        self.assertEqual(21, Slot.objects.all().count())
