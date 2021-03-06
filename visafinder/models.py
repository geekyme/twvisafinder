# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField


class VisaCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class VisaEligibility(models.Model):
    eligiblevisa = models.ForeignKey('Visa', on_delete=models.CASCADE)
    country = CountryField(null=True, blank=True)
    all_countries = models.BooleanField(default=False)
    conditional = models.BooleanField(default=False)
    condition = models.TextField(null=True, blank=True)
    min_age = models.PositiveSmallIntegerField(null=True, blank=True)
    max_age = models.PositiveSmallIntegerField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    update_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.eligiblevisa.name + "-" + self.country.name


class Visa(models.Model):
    ENTRY_CHOICES = (
            ('1', 'Single Entry'),
            ('2', 'Double Entry'),
            ('X', 'Multiple Entry'),
    )

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    category = models.ManyToManyField(VisaCategory())
    duration = models.PositiveSmallIntegerField()
    entries = models.CharField(max_length=1, choices=ENTRY_CHOICES, default='1')
    link = models.URLField()
    eligibilities = models.ManyToManyField(VisaEligibility, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    update_date = models.DateField(default=timezone.now)
    extendable = models.BooleanField(default=False)
    requirements = models.TextField()

    def __str__(self):
        return self.name

class GoldCardQualification(models.Model):
    MINISTRY_CHOICES = (
         ('MOST', 'Science and Technology'),
         ('MOEA', 'Economics'),
         ('MOE', 'Education'),
         ('MOC', 'Culture and Art'),
         ('MOS', 'Sport'),
         ('MOF', 'Finance'),
         ('MOJ', 'Law'),
         ('MOA', 'Architecture'),
    )

    ministry = models.CharField(max_length=4, choices=MINISTRY_CHOICES, default='MOST')
    regulation_no = models.CharField(max_length=6)
    link = models.URLField()
    notes = models.TextField(null=True, blank=True)
    weight = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.ministry + "-" + self.regulation_no


class GoldCardQuestion(models.Model):
    tree_id = models.PositiveSmallIntegerField(null=False, blank=False)
    tree_order = models.PositiveSmallIntegerField(null=False, blank=False)
    next_tree_id = models.PositiveSmallIntegerField(null=True, blank=True)
    qualifications = models.ManyToManyField(GoldCardQualification, blank=True)
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text
