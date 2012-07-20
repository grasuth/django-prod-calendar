from django.db import models
from django.utils.translation import ugettext as _

"""
Production calendar models.

Core concepts are:

    * There is a default number of places available per slot.
    * There are slots that can have a number of spaces.
    * Slots have a fixed length, to determine when the next slot can start
    * Slots are allocated lazily: the don't exist until referenced, then
      that slot is created. This makes sure we have a calandar for
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
    spaces = models.IntegerField()

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


class Slot(models.Model):
    start_date = models.DateField()
    spaces = models.IntegerField()
    used_spaces = models.IntegerField()


class SpaceValue(models.Model):
    spaces = models.IntegerField()
    value = models.DecimalField()
