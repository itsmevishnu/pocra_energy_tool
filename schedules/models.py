from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class TimeStamp(models.Model):
    """
    Abstract model inheritance for getting all the fields mentioned below in all the models

    """
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Name(TimeStamp):
    """
    Abstract database for storing the names of the entity in English and Marathi.
    """
    name = models.CharField(max_length=100, unique=True)
    name_mr = models.CharField(max_length=100, null=True)
    
    class Meta:
        abstract = True

# Crops and related meta data tables.
class Crop(Name):
    """
    Model for storing crop information
    """
    water_requirement = models.CharField(max_length=5)

    class Meta:
        """
        Change the table names to crops
        """
        db_table = 'crops'

    def __str__(self):
        return self.name

class IrrigationMethod(Name):
    """
    Model for storing the irrigation methods
    """
    class Meta:
        """
        Change the table names to irrigation method
        """
        db_table = "irrigation_methods"

    def __str__(self): 
        return self.name
    
    
class SoilType(Name):
    """
    Model for storing the soil types
    """
    class Meta:
        """
        Change the table name soil types
        """
        db_table = "soil_types"
    
    def __str__(self):
        return self.name


class CropRelation(models.Model):
    """
    A juncton table that connect different models together.
    It specify the frequency of irrigation(for every x days) required for each crop for 
    different irrigation method and for different soil type.
    The calculation performed by the field observations.
    """
    crop = models.ManyToManyField(Crop)
    irrigation_method = models.ManyToManyField(IrrigationMethod)
    soil_type = models.ManyToManyField(SoilType)
    irrigation_frequency = models.IntegerField() #irrigated every x days

    class Meta:
        """
        Change the table name to crop_relations
        """
        db_table = "crop_relations"

    def __str__(self):
        crop_name = " ".join(str(name) for name in self.crop.all() )
        irrigation_method = " ".join(str(name) for name in self.irrigation_method.all() )
        soil_type = " ".join(str(name) for name in self.soil_type.all() )

        return f"Info of {crop_name} with {irrigation_method} irrigation in {soil_type} soil type"

class IrrigationTimeRate(models.Model):
    """
    Model to store the time required to irrigate unit area of land.
    Soil type and irrigation method considered for calculation.
    The time calculated based on the field observations.
    """
    soil_type = models.ForeignKey(SoilType, on_delete=models.CASCADE)
    irrigation_method = models.ForeignKey(IrrigationMethod, on_delete=models.CASCADE)
    pump_capacity = models.FloatField()
    time_required = models.FloatField()

    class Meta:
        """
        Change the table name to irrigation_time_rates
        """
        db_table = "irrigation_time_rates"

    def __str__(self):
        """
        The object shown as Good (Soil type) with drip (irrigation method) and 5 Hp( pump capaicity) required 5 hrs.
        """
        soil_type = self.soil_type.name
        irrigation_method = self.irrigation_method.name
        return f"{soil_type} soil with {irrigation_method} irrigation and {self.pump_capacity} Hp pump required {self.time_required} hrs"

# Farmers and related models.   
class Farmer(Name):
    """
    Farmer model store the farmer name and total lande
    """
    gat_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    total_area = models.FloatField()

    class Meta:
        """
        Change the table name to farmers
        """
        db_table = "farmers"

    def __str__(self):
        return self.name

class FarmerCropRelation(models.Model):
    """
    The junction table that connect farmers,crops, irrigation methods and soil type
    """
    farmer = models.ManyToManyField(Farmer)
    crop = models.ManyToManyField(Crop)
    irrigation_method = models.ManyToManyField(IrrigationMethod)
    soil_type = models.ManyToManyField(SoilType)
    area = models.FloatField()
    # irrigation_frequency = models.IntegerField() # Irrigated every x days
    # I need to find out the methods for checking the condition such that 
    # the area under each crop should be less than or equal to the total land 
    # entered by the farmer.

    class Meta:
        """
        Table name to farmer_crops
        """
        db_table = "farmer_crops"
    
    def __str__(self):
        """
        The object shows like "name(Farmer) has 5 ha(area) of wheat(crop) culitvation"
        """
        farmer = " ".join(str(name) for name in self.farmer.all())
        crop = " ".join(str(name) for name in self.crop.all())
        return f"{farmer} has {self.area} of {crop} cultivation"
    
    # def clean(self):
    #     super().clean()
    #     total_area = self.farmer.total_area
        # # current_sum = self.entries.aggregate(models.Sum('area'))['area__sum'] or 0

        # print(total_area)
        # exit()
        # if current_sum > total_area:
        #     raise ValidationError(f"The sum of areas exceed total area {total_area}")

class FarmerPumpRelation(TimeStamp):
    """
    Model for storing farmer and pump information.
    """
    SOURCE = [
        ("open_well", "Open well"),
        ("bore_well", "Bore well"),
        ("surface_water", "Surface water"),
        ("other", "Other")
    ]

    source_type = models.CharField(max_length=15, choices=SOURCE)
    dt_id = models.CharField(max_length=50, null=True)
    capacity = models.FloatField()
    direct_to_field = models.BooleanField()
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)

    class Meta:
        """
        Change the table name to farmer_pumps
        """
        db_table = "farmer_pumps"

    def __str__(self):
        """
        The objects shows "Farmer has a pump of 2 hp connected with the source"
        """
        return f"{self.farmer.name} has a pump of {self.capacity} HP connected to {self.get_source_type_display()}"


# Schedule related models.
class Schedule(TimeStamp):
    """
    Model for schedules
    Contains Start_date and number of days and end date.
    End date is calculated from start date and number of days
    """
    start_date = models.DateField()
    number_of_days = models.IntegerField()
    duration_of_supply = models.FloatField(default=8.0)

    class Meta:
        """
        Change the table name to schedules
        """
        db_table = "schedules"

    @property
    def end_date(self):
        """
        Create a field called end_date by adding number of days to the start date.
        """
        return self.start_date + timedelta(days=self.number_of_days)
    
    def __str__(self):
        """
        The object shows like "Schedule 1 from dd/mm/yyyy to dd/mm/yyyy    
        """
        return f"Schedule {self.pk} from {self.start_date} to {self.end_date}"

class DayNightSchedule(models.Model):
    """
    Model for Day night and afternnon classification for schedule to display.
    It shows the time of power supply available.
    """
    SUPPLY_PERIOD = [
        ("day", "Day"),
        ("night", "Night"),
        ("afternoon", "Afternoon")
    ]
    date =  models.DateField()
    supply_period = models.CharField(max_length=15, choices=SUPPLY_PERIOD)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    
    class Meta:
        """
        Change the table name to day_night_schedules
        """
        db_table = 'day_night_schedules'

    def __str__(self):
        """
        The object shows Supply for schedule 1 on dd/mm/yyyy at day time
        """
        return f"Supply for schedule {self.schedule} on {self.date} at {self.supply_period}"

# Final calculations and relationships
class FarmerPowerRequirement(TimeStamp):
    """
    Model for storing different information connecting farmers and schedule
    """
    DURATION = [
        ("full_day", "Full day"),
        ("half_day", "Half day"),
        ("quarter_day", "Quarter of the day")
    ]
    days_for_irrigation = models.FloatField()
    number_of_irrigation = models.IntegerField()
    number_of_slots = models.IntegerField()
    last_irrigation_date = models.DateField(null=True)
    irrigation_start_within = models.IntegerField(null=True)
    period_between_irrigation = models.IntegerField(null=True)
    delta_period_between_irrigation = models.IntegerField(null=True)
    is_night_irrigation_acceptable = models.BooleanField()
    slot_duration = models.CharField(max_length=15, choices=DURATION)
    is_transfer_from_source = models.BooleanField()
    transfer_slot_duriation = models.CharField(max_length=15, choices=DURATION, null=True)

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    farmer_pump = models.ForeignKey(FarmerPumpRelation, on_delete=models.CASCADE, related_name='pump_for_irrigation')
    transfer_source_pump = models.ForeignKey(FarmerPumpRelation, on_delete=models.CASCADE, related_name='pump_for_transfer', null=True)

    class Meta:
        """
        Chagne the table name to farmer_power_requirements
        """
        db_table = "farmer_power_requirements"

    def __str__(self):
        """
        The objects shows Requirement for crop for irrigating using 1 HP pump
        """
        return f"Requirement for {self.crop.name} for irrigating using {self.farmer_pump.capacity} HP pump"
