from django.contrib import admin

# Register your models here.

from roomexpenses.models import RoomMember, IndividualShare

admin.site.register(RoomMember)
#admin.site.register(IndividualShare)