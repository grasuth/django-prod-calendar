Django Production Calendar
==========================

A simple calendar for scheduling production of real things.

The key idea
------------

Say I'm building widgets, and I can only build so many per period. I need a way
to schedule making widgets so that I don't blow my capacity, and also, so I can
schedule a holiday ahead in time and not fill it with widgets to make.

Or, when I'm close to capacity for delivery on a certain date, I can increase
my prices to match demand.  This is an aspect of demand management, as
popularized by low cost airlines.

In either case, you need a firm calendar with slots in it, a default allocation
of production capacity into slots, a way to allocate slots, and an ability to
manually adjust it at will.  That's the aim of this app.

How does it work
----------------

There are standard sized slots, a multiple of a day, and each slot has
a capacity (a number of spaces).

Spaces, when allocated, have a value assigned from a table of SpaceValues that
increase as more spaces are used.

Status
------

In development. Feel free to have a look, but don't expect it to work.  As at
23 Jul 2012, the models are complete, and I'm a adding tests around the
functionality that seems to be needed.


There will be lots of changes before this hits alpha.

