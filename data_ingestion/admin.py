from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Company)
admin.site.register(CompanyLinkedinAccount)
admin.site.register(Investor)
admin.site.register(Employment)