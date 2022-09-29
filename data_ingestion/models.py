from tabnanny import verbose
import uuid
from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    headcount = models.PositiveIntegerField(blank=True, null=True)
    founding_date = models.DateField(blank=True, null=True)
    most_recent_raise = models.PositiveIntegerField(blank=True, null=True)
    most_recent_valuation = models.PositiveIntegerField(blank=True, null=True)
    known_total_funding = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = "Companies"

class CompanyLinkedinAccount(models.Model):
    linkedin_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, related_name='linkedin_names', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.linkedin_name)

class Employment(models.Model):
    person_id = models.UUIDField(default=uuid.uuid4)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    last_title = models.CharField(max_length=255, blank=True)
    group_start_date = models.DateField(blank=True, null=True)
    group_end_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return str(self.person_id) + " - " + str(self.last_title) + " at " + str(self.company.name)

    class Meta:
        ordering = ('person_id', )

class Investor(models.Model):
    name = models.CharField(max_length=255, primary_key=True, unique=True)
    companies_funded = models.ManyToManyField(Company, related_name='investors', db_table='investments')

    def __str__(self):
        return str(self.name)