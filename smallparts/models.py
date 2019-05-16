from django.db import models
# from .additional import comboboxList

class Group(models.Model):
	group_name = models.CharField(max_length = 255)

	def __str__(self):
		return self.group_name


class Partlist(models.Model):
	group = models.ForeignKey('Group', on_delete = models.CASCADE)
	name = models.CharField(max_length = 2000)

	def __str__(self):
		return self.name


class Specification(models.Model):
	part = models.CharField(max_length = 255)
	machine = models.TextField(default = '')
	# specification = models.TextField()
	# content = models.CharField(max_length = 2000)
	# group = models.CharField(max_length = 255)

	def __str__(self):
		return self.part


class SheetConfig(models.Model):
	title = models.CharField(max_length = 2000)
	# unit_code = models.CharField(max_length = 255)
	# machine_type = models.CharField(max_length = 255)
	# reference_wi = models.CharField(max_length = 255)
	config_string = models.TextField()
	# part = models.CharField(max_length = 255)
	group = models.ForeignKey('Group', on_delete = models.CASCADE)
	version = models.IntegerField()
	is_active = models.BooleanField(default = False)
	comments = models.TextField(null = True, blank = True)

	def __str__(self):
		return self.title

class Record(models.Model):
	serial_no = models.CharField(max_length = 255, unique = True)
	record_string = models.TextField()
	# unit_code = models.CharField(max_length = 255)
	machine_type = models.CharField(max_length = 255)
	part = models.CharField(max_length = 255)
	# group = models.CharField(max_length = 255)
	# reference_wi = models.CharField(max_length = 255)
	sheet_config_id = models.ForeignKey('SheetConfig', on_delete = models.CASCADE)
	result = models.IntegerField(default = 0)
	order_no = models.IntegerField(null = True)
	operator = models.CharField(max_length = 255)
	input_date = models.DateTimeField(auto_now_add = True)
	update_date = models.DateTimeField(auto_now = True)
	# comments = models.TextField(null = True, blank = True)

	def __str__(self):
		return self.serial_no

class SfmAjd(models.Model):
	shift = models.CharField(max_length = 255)
	adj_date = models.DateField()
	adj_reason = models.CharField(max_length = 255)
	adj_nbr = models.IntegerField()

	def __str__(self):
		return self.shift

