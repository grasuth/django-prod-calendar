from datetime import datetime, date, timedelta

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

"""
Production calendar models.

Core concepts are:

    * There is a default number of places available per slot.
    * There are slots that can have a number of spaces.
    * Slots have a fixed length, to determine when the next slot can start
    * Slots are allocated lazily: the don't exist until referenced, then
      that slot is created. This makes sure we have a calendar for
      some number of periods in the future.
    * The Value of a space is determined by the collection of SpaceValues.
    * Lower value spaces are assigned first.

"""


class Defaults(models.Model):
    """
    Defines defaults for slots not yet created

    We want this to be user-modifiable, so there ought to be just
    one record in this table. We enforce this in admin screens and
    model save and delete.

    """
    spaces = models.IntegerField(
            help_text=_('The default number of spaces in each slot.  '
                        'New slots are created with this value.')
            )

    def save(self):
        """
        Force id to 1, to keep single row in table

        """
        self.id = 1
        super(Defaults, self).save()

    def delete(self):
        """
        Remove ability to delete single row.

        """
        pass

    def __unicode__(self):
        return ('Default spaces={0}').format(self.spaces)

    @classmethod
    def get_default_spaces(cls):
        """
        Get the default number of spaces per slot

        """
        default = cls.objects.get(id=1)
        return defaults.spaces


class Slot(models.Model):
    """
    Defines a block of production time.

    A block of production time has a date, number of spaces
    and number of used spaces.

    """
    start_date = models.DateField(
            help_text=_('Start date for this Slot.'),
            db_index=True,
            editable=False,
            unique=True)
    spaces = models.IntegerField(
            help_text=_('Total number of spaces in this Slot.'),)
    used_spaces = models.IntegerField(
            default=0,
            help_text=_('Spaces in this slot that are used.'))
    note = models.TextField(
            help_text=_('Notes about this slot')
            )

    def book_space(self, count=1):
        """
        Book a space or ``count`` spaces in this slot.

        :param count:
            The number of spaces to book

        :returns:
            The total value (as a Decimal) for the booked spaces or None if not
            enough space was available in this slot.

        """
        if self.used_spaces + count > spaces:
            return None
        else:
            value = self._get_space_value(count)
            self.used_spaces += count
            return value

    def get_space_value(self, count=1):
        """
        Calculate the value of ``count`` spaces in this slot.

        """
        value = Decimal('0')
        for s in range(self.used_spaces, self.used_spaces + count):
            value += SpaceValue.get_space_value(s)
        return value


    @classmethod
    def get_slot_for_date(cls, date):
        """
        Return a slot for the given date, creating a new
        slot and populating if needed

        """
        try:
            slot = cls.objects.get(start_date=date)
        except ObjectDoesNotExist:
            last_slot = cls.objects.all().order_by('-start_date')[0]
            slot_delta = cls.get_slot_time_delta()
            if last_slot:
                start_date = last_slot + slot_delta
            else:
                start_date = cls._get_start_date()
            default_spaces = Defaults.get_default_spaces()
            while start_date <= date:
                new_slot = Slot(
                        start_date=start_date,
                        spaces=default_spaces,
                        used_spaces=0,
                        )
                new_slot.save()
                start_date = start_date + cls.get_slot_time_delta()
            slot = new_slot
        return slot

    @classmethod
    def _get_slot_time_delta(cls):
        """
        Returns a timedelta with the size of a slot

        """
        slot_length = getattr(settings, 'SLOT_LENGTH_DAYS', 7)
        return timedelta(days=slot_length)

    @classmethod
    def _get_start_date(cls):
        """
        Returns a date object with the starting date in it.

        """
        incoming_time = getattr(settings, 'SLOT_START_DATE')
        dt = datetime.strptime(incoming_time, settings.DATE_FORMAT)
        return dt.date


class SpaceValue(models.Model):
    """
    Assigns value to spaces.  These are considered when
    spaces are (being) filled to work out the value of the
    space that we are about to fill.  We start at lowest value
    and go up.

    """
    spaces = models.IntegerField(
            help_text=_('Number of spaces.')
            )
    value = models.DecimalField(
            help_text=_('The value of each of these spaces.'),
            max_digits=10,
            decimal_places=2
            )
    note = models.TextField(
            help_text=_('Notes about this space value.'),
            )


    @classmethod
    def get_space_value(cls, space_index):
        """
        Get the value of the given space.
        
        Returns None if there are no SpaceValues, or the 
        most expensive value if above the number of allocated
        spaces.
        
        :param space_index:
            The index of the space to get a value for. Slot 
            indexes start at 1, not 0.

        :returns:
            ``None`` if no space values available, or the relevant
            value for the given space index (as a Decimal) or the 
            maximum value for that space if index is beyond the last
            space value.

        """
        values = cls.objects.all().order_by('value')
        if len(values) == 0:
            return None
        for val in values:
            if space_index <= val.spaces:
                return val.value
        biggest = cls.objects.all().order_by('-value')[0]
        return biggest.value

