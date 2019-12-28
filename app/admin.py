# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from app.models import QuoteVoucher, Itenary, Hotel, Vehicle


class ItenaryAdmin(admin.TabularInline):
    model = Itenary


class HotelAdmin(admin.TabularInline):
    model = Hotel


class VehicleAdmin(admin.TabularInline):
    model = Vehicle


class VoucherAdmin(admin.ModelAdmin):
    inlines = (ItenaryAdmin, HotelAdmin, VehicleAdmin)


admin.site.register(QuoteVoucher, VoucherAdmin)
