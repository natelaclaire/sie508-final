from django.db import models

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.conf import settings
from datetime import date
import uuid  # Required for unique book instances
from datetime import date

from django.conf import settings  # Required to assign User as a borrower


class PlanType(models.Model):
    """Model representing a plan type (e.g. Flight, Hotel, Activity, etc.)."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a plan type (e.g. Flight, Hotel, Activity, etc.)"
    )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular plan type instance."""
        return reverse('plantype-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='plantype_name_case_insensitive_unique',
                violation_error_message = "Plan Type already exists (case insensitive match)"
            ),
        ]

class PlanStatus(models.Model):
    """Model representing a Plan Status (e.g. Idea, Booked, Canceled, etc.)"""
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the plan's status (e.g. Idea, Booked, Canceled, etc.)")

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('planstatus-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='planstatus_name_case_insensitive_unique',
                violation_error_message = "Plan Status already exists (case insensitive match)"
            ),
        ]

class Trip(models.Model):
    """Model representing a trip."""
    destination = models.CharField(max_length=200)
    goal_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(
        max_length=1000, help_text="Enter any notes about the trip", null=True, blank=True)

    class Meta:
        ordering = ['destination']

    def get_absolute_url(self):
        """Returns the url to access a particular trip record."""
        return reverse('trip-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.destination

class Plan(models.Model):
    """Model representing a plan."""
    description = models.CharField(max_length=200)
    notes = models.TextField(
        max_length=1000, help_text="Enter any notes about the plan", null=True, blank=True)
    status = models.ForeignKey(
        PlanStatus, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(
        PlanType, on_delete=models.SET_NULL, null=True)
    scheduled_start_date_time = models.DateTimeField(null=True, blank=True)
    scheduled_end_date_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['scheduled_start_date_time', 'description']

    def get_absolute_url(self):
        """Returns the url to access a particular plan record."""
        return reverse('plan-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.description

class Todo(models.Model):
    """Model representing a todo."""
    description = models.CharField(max_length=200)
    notes = models.TextField(
        max_length=1000, help_text="Enter any notes about the todo", null=True, blank=True)
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE)
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, null=True)
    due_date = models.DateField(null=True, blank=True)
    date_completed = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['due_date', 'description']

    def get_absolute_url(self):
        """Returns the url to access a particular todo record."""
        return reverse('todo-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.description

class BudgetItem(models.Model):
    """Model representing a budget item."""
    description = models.CharField(max_length=200)
    notes = models.TextField(
        max_length=1000, help_text="Enter any notes about the budget item", null=True)
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE)
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, null=True)
    due_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    ITEM_TYPES = (
        ('es', 'Estimated'),
        ('ac', 'Actual'),
        ('ex', 'Expended'),
    )

    type = models.CharField(
        max_length=2,
        choices=ITEM_TYPES,
        blank=True,
        default='es',
        help_text='Budget Item Type')

    class Meta:
        ordering = ['due_date', 'description']

    def get_absolute_url(self):
        """Returns the url to access a particular budget item record."""
        return reverse('budgetitem-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.description

