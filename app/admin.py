# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from app.models import QuoteVoucher, Itenary, Hotel, Vehicle, SpecialService


class ItenaryAdmin(admin.TabularInline):
    model = Itenary


class HotelAdmin(admin.TabularInline):
    model = Hotel


class VehicleAdmin(admin.TabularInline):
    model = Vehicle


class ServiceAdmin(admin.TabularInline):
    model = SpecialService


class VoucherAdmin(admin.ModelAdmin):
    inlines = (ItenaryAdmin, HotelAdmin, VehicleAdmin, ServiceAdmin)


admin.site.register(QuoteVoucher, VoucherAdmin)
