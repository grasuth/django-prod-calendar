from django.db import models

"""
Production calendar models.

Core concepts are:

    * There are slots that can have a capacity.
    * Slots have a fixed time period (day, week, month)
    * Slots are allocated lazily: the don't exist until referenced, then
      that slot is created.
    * Slots can be filled with a recipe of different types of item

"""


class Defaults(models.Model):
    available = models.IntegerField()


class Slot(models.Model):
    number = IntegerField()
    available = models.IntegerField()
    used = models.IntegerField()


class SlotValue(models.Model):
    quantity = models.IntegerField()
    value = models.DecimalField()
