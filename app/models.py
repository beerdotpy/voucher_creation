# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.mail import EmailMessage
import pdfkit
import os
from django.template.loader import get_template
from datetime import date


class QuoteVoucher(models.Model):
    email_id = models.CharField(max_length=200)
    no_of_pax = models.CharField(max_length=200)
    package_type = models.CharField(max_length=200)
    arrival = models.DateField()
    pickup_place = models.CharField(max_length=200)
    no_of_rooms = models.CharField(max_length=200)
    price = models.IntegerField()
    package_inclusion = models.TextField()
    package_exclusion = models.TextField()
    reservation_policy = models.TextField()
    cancellation_policy = models.TextField()
    terms_conditions = models.TextField()

    def save(self, *args, **kwargs):
        output_path = os.getcwd() + '/templates/output/test.pdf'
        data = {'current_date': date.today(),
                'image_path': os.getcwd() + '/templates/images/logo.png',
                'no_of_pax': self.no_of_pax,
                'arrival': self.arrival,
                'departure': self.pickup_place,
                'rooms': self.no_of_rooms,
                'duration': self.package_type,
                'itinerary': self.itenary_set.all().values,
                'hotels': self.hotel_set.all().values,
                'vehicle': self.vehicle_set.all().values,
                'amount': self.price,
                'inclusion': self.package_inclusion.split("\n"),
                'exclusion': self.package_exclusion.split("\n"),
                'reservation_policy': self.reservation_policy.split("\n"),
                'cancellation_policy': self.cancellation_policy.split("\n"),
                'terms': self.terms_conditions.split("\n"),
                'special_service': self.specialservice_set.all().values}
        template = get_template('quoteVoucher.html')
        html = template.render(data)
        pdfkit.from_string(html, output_path)
        msg = EmailMessage('Quote Voucher', 'Please find the quotation attached', 'sarthakmeh03@gmail.com',
                           [self.email_id])
        msg.content_subtype = "html"
        msg.attach_file(output_path)
        msg.send()
        return super(QuoteVoucher, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.package_type


class Itenary(models.Model):
    voucher = models.ForeignKey(QuoteVoucher)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __unicode__(self):
        return self.title


class Hotel(models.Model):
    voucher = models.ForeignKey(QuoteVoucher)
    name = models.CharField(max_length=255)
    check_in = models.DateField()
    check_out = models.DateField()
    place = models.CharField(max_length=100)
    meal_plan = models.CharField(max_length=100)
    room_type = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Vehicle(models.Model):
    voucher = models.ForeignKey(QuoteVoucher)
    category = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    no_of_vehicle = models.IntegerField()

    def __unicode__(self):
        return self.name


class SpecialService(models.Model):
    voucher = models.ForeignKey(QuoteVoucher)
    date = models.DateField()
    service = models.CharField(max_length=200)
    description = models.TextField()
