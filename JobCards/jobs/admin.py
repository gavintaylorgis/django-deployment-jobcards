from django.contrib import admin

# Register your models here.
from .models import Status,AssetType,Asset,Contractor,Priority,Approver,Job,Comments,JobType


admin.site.register(Status)
admin.site.register(AssetType)
admin.site.register(Asset)
admin.site.register(Contractor)
admin.site.register(Priority)
admin.site.register(Approver)
admin.site.register(Job)
admin.site.register(Comments)
admin.site.register(JobType)