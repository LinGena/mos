from django.db import models


class Activities(models.Model):
    name = models.CharField(unique=True, max_length=255)
    create_user = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'activities'
        verbose_name_plural = 'activities'


class Facilities(models.Model):
    name = models.CharField(unique=True, max_length=255)
    create_user = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'facilities'
        verbose_name_plural = 'facilities'


class Worklog(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    facility_id = models.IntegerField(blank=True, null=True)
    activity_id = models.IntegerField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    hours_worked = models.FloatField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    earned_hours = models.FloatField(blank=True, null=True)
    pgl = models.FloatField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'worklog'


class Pgl(models.Model):
    facility_id = models.IntegerField()
    activity_id = models.IntegerField()
    pgl = models.FloatField()

    class Meta:
        managed = False
        db_table = 'pgl'
        verbose_name_plural = 'pgl'
