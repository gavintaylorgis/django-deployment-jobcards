from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

User = get_user_model()
# Create your models here.
GROUP_CHOICES = [ [g.name, g.name] for g in Group.objects.exclude(name='contractor').exclude(name='requisitioner').exclude(name='approver') ]
#print(GROUP_CHOICES)

class Status(models.Model):
    status_name = models.CharField(max_length=200,default='Hold')
    status_descrip = models.TextField()
    status_sort_order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.status_name

    class Meta():
        ordering = ['status_sort_order']


class AssetType(models.Model):
    asset_type_name = models.CharField(max_length=120)
    asset_type_descrip = models.TextField()

    def __str__(self):
        return self.asset_type_name


class Asset(models.Model):
    asset_name = models.CharField(max_length=200)
    asset_descrip = models.CharField(max_length=200)
    asset_active = models.BooleanField(default=True,null=False)
    asset_type = models.ForeignKey(AssetType,default=0,on_delete=models.CASCADE)

    def __str__(self):
        return self.asset_name

class Contractor(models.Model):
    contractor_name = models.CharField(max_length=200)

    def __str__(self):
        return self.contractor_name

class Priority(models.Model):
    priority_name = models.CharField(max_length=200)
    priority_sort_order = models.IntegerField(default=0)

    def __str__(self):
        return self.priority_name

    class Meta():
        ordering = ['priority_sort_order']

class Approver(models.Model):
    approver_name = models.CharField(max_length=200)

    def __str__(self):
        return self.approver_name

class JobType(models.Model):
    jobtype_name = models.CharField(max_length=120)
    jobtype_descrip = models.TextField()
    
    def __str__(self):
        return self.jobtype_name

class Job(models.Model):

    requisitioner = models.ForeignKey(User,related_name='jobs',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    asset = models.ForeignKey(Asset,related_name='jobs',on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority,related_name='jobs',on_delete=models.CASCADE)
    request_completed_by_date = models.DateTimeField(auto_now=False)
    job_descrip = models.TextField('Job Description')
    conctractor = models.ForeignKey(Contractor,related_name='jobs',on_delete=models.CASCADE,default=Contractor.objects.get(contractor_name="None").pk)
    status = models.ForeignKey(Status,related_name='jobs',on_delete=models.CASCADE,default=Status.objects.get(status_name='Requested').pk)
    approver = models.ForeignKey(Approver,related_name='jobs',on_delete=models.CASCADE,default=1)
    job_type = models.ForeignKey(JobType,related_name='jobs',on_delete=models.CASCADE,null=True)
    jobcard_number = models.CharField('Invoice Number',max_length=150,default='')
    job_closed = models.BooleanField(default=False)
    contractor_group = models.CharField(max_length=200, choices=GROUP_CHOICES,default=4)
    ack_cost_code = models.CharField('ACK/EDC Code',max_length=20, default='', null=True)

    
    def __str__(self):
        return self.job_descrip 
    
    def save(self,*args,**kwargs):
        
        super().save(*args,**kwargs)
    
    def approve(self):
        #stat = get_object_or_404(Status,status_name="Approved")
        stat = Status.objects.get(status_name="Approved")
        self.status = stat
        self.save()
    def rework(self):
            #stat = get_object_or_404(Status,status_name="Approved")
        stat = Status.objects.get(status_name="Rework")
        self.status = stat
        self.save()
    
    def reject(self):
            #stat = get_object_or_404(Status,status_name="Approved")
        stat = Status.objects.get(status_name="Rejected")
        self.status = stat
        self.save()
    
    def accepted(self):
            #stat = get_object_or_404(Status,status_name="Approved")
        stat = Status.objects.get(status_name="Accepted")
        self.status = stat
        self.save()

    def declined(self):
            #stat = get_object_or_404(Status,status_name="Approved")
        stat = Status.objects.get(status_name="Declined")
        self.status = stat
        self.save()
    
    def requestcloseout(self):
            #stat = get_object_or_404(Status,status_name="Approved")
        stat = Status.objects.get(status_name="Request Closeout")
        self.status = stat
        self.save()

    def closeout(self):
            #stat = get_object_or_404(Status,status_name="Approved")
        stat = Status.objects.get(status_name="Closed")
        self.status = stat
        self.job_closed = True
        self.save()
    
    def re_request(self):
        stat = Status.objects.get(status_name="Requested")
        self.status = status
        self.save()


    def get_absolute_url(self):
        return reverse('jobs:selected_job_details',kwargs={'pk':self.pk}) 
    class Meta:
        ordering = ['-pk']
        #unique_together = ['requisitioner','message'] 

class Comments(models.Model):
    job = models.ForeignKey(Job,related_name='comments',on_delete=models.CASCADE)
    commentor = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)
    comment_details = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta():
        ordering = ['-created_at']

