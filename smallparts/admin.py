from django.contrib import admin
from .models import Partlist, Specification, SheetConfig, Record, Group
# Register your models here.

class Partlists(admin.ModelAdmin):
	list_display = ('name', 'group_id')

class Specifications(admin.ModelAdmin):
	list_display = ('part', 'machine')

class SheetConfigs(admin.ModelAdmin):
	list_display = ('id','title', 'group', 'version', 'is_active')

class Records(admin.ModelAdmin):
	list_display = ('id','serial_no', 'part', 'result', 'operator')

class Groups(admin.ModelAdmin):
	list_display = ('id', 'group_name')

admin.site.register(Partlist, Partlists)
admin.site.register(Specification, Specifications)
admin.site.register(SheetConfig, SheetConfigs)
admin.site.register(Record, Records)
admin.site.register(Group, Groups)