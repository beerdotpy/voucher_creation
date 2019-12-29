# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.mail import EmailMessage
import pdfkit
import os
from django.template.loader import get_template
from datetime import date
import time
from threading import Thread


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
    confirmed = models.BooleanField()
    confirmation_number = models.CharField(max_length=200)
    name_of_guest = models.CharField(max_length=200)
    phone_number = models.IntegerField()

    def save(self, *args, **kwargs):
        Worker(self).start()
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
    address = models.TextField(blank=True)
    contact_person = models.TextField(max_length=200, blank=True)
    phone_number = models.IntegerField(blank=True)
    contact_person_position = models.CharField(max_length=200, blank=True)
    place = models.CharField(max_length=100)
    meal_plan = models.CharField(max_length=100)
    room_type = models.CharField(max_length=200)
    occupancy_type = models.CharField(max_length=200)
    no_of_rooms = models.IntegerField()
    no_of_nights = models.IntegerField()

    def __unicode__(self):
        return self.name


class Vehicle(models.Model):
    voucher = models.ForeignKey(QuoteVoucher)
    category = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    no_of_vehicle = models.IntegerField()
    number_plate = models.CharField(max_length=20)
    no_of_days = models.IntegerField()
    ac_available = models.BooleanField()
    contact_person = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=12)
    service_provider = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class SpecialService(models.Model):
    voucher = models.ForeignKey(QuoteVoucher)
    date = models.DateField()
    service = models.CharField(max_length=200)
    description = models.TextField()


class Worker(Thread):
    def __init__(self, voucher):
        super(Worker, self).__init__()
        self.voucher = voucher

    def run(self):
        time.sleep(20)
        print "Sending Mail....."
        self = self.voucher
        output_path = os.getcwd() + '/templates/output/test.pdf'
        if not self.confirmed:
            data = {'current_date': date.today(),
                    'image_path': os.getcwd() + '/templates/images/logo.png',
                    'no_of_pax': self.no_of_pax,
                    'arrival': self.arrival,
                    'departure': self.pickup_place,
                    'rooms': self.no_of_rooms,
                    'duration': self.package_type,
                    'itinerary': self.itenary_set.all().values(),
                    'hotels': self.hotel_set.all().values(),
                    'vehicle': self.vehicle_set.all().values(),
                    'amount': self.price,
                    'inclusion': self.package_inclusion.split("\n"),
                    'exclusion': self.package_exclusion.split("\n"),
                    'reservation_policy': self.reservation_policy.split("\n"),
                    'cancellation_policy': self.cancellation_policy.split("\n"),
                    'terms': self.terms_conditions.split("\n"),
                    'special_service': self.specialservice_set.all().values()}
            template = get_template('quoteVoucher.html')
            html = template.render(data)
            pdfkit.from_string(html, output_path)
            msg = EmailMessage('Quote Voucher', 'Please find the quotation attached', 'sarthakmeh03@gmail.com',
                               [self.email_id])
            msg.content_subtype = "html"
            msg.attach_file(output_path)
            msg.send()
        else:
            msg = EmailMessage('Hotel and Driver Voucher', 'Please find the voucher attached', 'sarthakmeh03@gmail.com',
                               [self.email_id])
            for i in self.hotel_set.all().values():
                data = {'current_date': date.today(),
                        'image_path': os.getcwd() + '/templates/images/logo.png',
                        'hotel_name': i['name'],
                        'address': i['address'],
                        'guest_name': self.name_of_guest,
                        'check_in': i['check_in'],
                        'check_out': i['check_out'],
                        'no_of_pax': self.no_of_pax,
                        'meal_plan': i['meal_plan'],
                        'room_type': i['room_type'],
                        'no_of_nights': i['no_of_nights'],
                        'occupancy_type': i['occupancy_type'],
                        'no_of_rooms': i['no_of_rooms'],
                        'contact_name': i['contact_person'],
                        'mobile_no': i['phone_number'],
                        'contact_position': i['contact_person_position'],
                        'place': i['place'],
                        'confirmation_no': self.confirmation_number
                        }
                template = get_template('hotelVoucher.html')
                html = template.render(data)
                pdfkit.from_string(html, output_path)
                msg.content_subtype = "html"
                msg.attach_file(output_path)
            driver_data = {'current_date': date.today(),
                           'confirmation_no': self.confirmation_number,
                           'guest_name': self.name_of_guest,
                           'image_path': os.getcwd() + '/templates/images/logo.png',
                           'arrival': self.arrival,
                           'departure': self.pickup_place,
                           'duration': self.package_type,
                           'itinerary': self.itenary_set.all().values,
                           'hotels': self.hotel_set.all().values,
                           'vehicle': self.vehicle_set.all().values,
                           'special_service': self.specialservice_set.all().values}
            template = get_template('driverVoucher.html')
            html = template.render(driver_data)
            pdfkit.from_string(html, output_path)
            msg.content_subtype = "html"
            msg.attach_file(output_path)
            msg.send()
