from prod_calendar.models import (
                                Defaults,
                                Slot,
                                SpaceValue) 
from django.contrib import admin


admin.site.register(Defaults)
admin.site.register(Slot)
admin.site.register(SpaceValue)

