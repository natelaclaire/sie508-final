from django.contrib import admin

# Register your models here.
from .models import PlanType, PlanStatus, Plan, Trip, Todo, BudgetItem

# Define the admin class
class PlanTypeAdmin(admin.ModelAdmin):
    list_display = ('name')

    fields = ['name']


# Register the admin class with the associated model
admin.site.register(PlanType, PlanTypeAdmin)

# Define the admin class
class PlanStatusAdmin(admin.ModelAdmin):
    list_display = ('name')

    fields = ['name']


# Register the admin class with the associated model
admin.site.register(PlanStatus, PlanStatusAdmin)


class PlanInline(admin.TabularInline):
    model = Plan

    extra = 0

class TodoInline(admin.TabularInline):
    model = Todo

    extra = 0

class BudgetItemInline(admin.TabularInline):
    model = BudgetItem

    extra = 0

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('destination', 'goal_date')

    inlines = [PlanInline, TodoInline, BudgetItemInline]
