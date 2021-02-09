from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django.http import Http404
from django.views import generic
from django.views.generic.edit import UpdateView 
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from . import views
from jobs.models import Job,Comments,Status
from jobs.forms import JobForm,CommentForm,JobCodeForm

from django.contrib.auth import get_user_model
from bootstrap_datepicker_plus import DatePickerInput,DateTimePickerInput

from django.core.mail import send_mail

User = get_user_model()
# Create your views here.


class JobsList(generic.ListView):
    model = models.Job
    #select_related = ('user','group')

class ClosedJobsList(generic.ListView):
    model = models.Job
    template_name = 'jobs/job_list_closed.html'
    #select_related = ('user','group')

class JobDetailView(generic.DetailView):
    model = models.Job
    fields = ['asset','priority','request_completed_by_date','job_descrip','contractor_group','conctractor','status','approver','job_type','jobcard_number','job_closed','ack_cost_code']
    template_name = 'jobs/job_detail.html'


class UserJob(generic.ListView):
    model = models.Job
    template_name = 'jobs/user_job_list.html'

    def get_queryset(self):
        try:
            self.jobs_requisitioner = User.objects.prefetch_related('jobs').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.job_user.jobs.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['job_user'] = self.job_user
        return context



class JobDetail(generic.DetailView):
    model = models.Job
    #select_related = ('user','job')

    def get_queryset(self):
        queryset = super().get_queryset()
        #return queryset.filter(requisitioner__username__iexact=self.kwargs.get('username'))
        print(self.request.job.pk)
        return queryset.filter(job_pk = self.request.job.pk)


class CreateJob(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields = ('asset','priority','request_completed_by_date','job_descrip','contractor_group','approver','job_type','ack_cost_code')
    model = models.Job

    def get_form(self):
         form = super().get_form()
         form.fields['request_completed_by_date'].widget = DateTimePickerInput(format='%Y-%m-%d %H:%M')
         return form

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.requisitioner = self.request.user
        self.object.status = Status.objects.get(status_name="Requested")
        self.object.save()
        return super().form_valid(form)

class DeleteJob(LoginRequiredMixin,generic.DeleteView):
    model = models.Job
    #select_related = ('user','job')
    success_url = reverse_lazy('jobs:all')


class UpdateJob(LoginRequiredMixin,generic.UpdateView):
    model = models.Job
    fields = ['asset','priority','request_completed_by_date','job_descrip','contractor_group','status','approver','job_type','ack_cost_code']
    template_name_suffix = '_update_form'
    success_url =reverse_lazy('jobs:all')

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.status = Status.objects.get(status_name="Requested")
        self.object.save
        return super().form_valid(form)

@login_required
def job_approve(request,pk):
    job = get_object_or_404(Job,pk=pk)
    job.approve()
    comment_instance_details = 'Comment status changed to APPROVED' 
    comment_instance = Comments.objects.create(job=job,commentor=request.user,comment_details=comment_instance_details)
    email_subject = 'Do Not Reply ! Jobcard #{} Updated'.format(pk)
    email_message = 'Job number #{} has been APPROVED by {}. Go to http://127.0.0.1:8000/jobs/job/{} to see any comments'.format(pk,request.user.username,pk)
    print(email_message)
    send_mail(
        email_subject,
        email_message,
        'gavin.taylor.gis@gmail.com',
        [job.requisitioner.email],
        fail_silently=True,
    )
    print('email sent')
    return redirect('/jobs/')

@login_required
def job_rework(request,pk):
    job = get_object_or_404(Job,pk=pk)
    job.rework()
    comment_instance_details = 'Comment status changed to REWORK' 
    comment_instance = Comments.objects.create(job=job,commentor=request.user,comment_details=comment_instance_details)
    email_subject = 'Do Not Reply ! Jobcard #{} Updated'.format(pk)
    email_message = 'Job number #{} has been REWORK by {}. Go to http://127.0.0.1:8000/jobs/job/{} to see any comments'.format(pk,request.user.username,pk)
    print(email_message)
    send_mail(
        email_subject,
        email_message,
        'gavin.taylor.gis@gmail.com',
        [job.requisitioner.email],
        fail_silently=True,
    )
    return redirect('jobs:add_comment_to_job',pk=pk)

@login_required
def job_reject(request,pk):
    job = get_object_or_404(Job,pk=pk)
    job.reject()
    comment_instance_details = 'Comment status changed to REJECTED' 
    comment_instance = Comments.objects.create(job=job,commentor=request.user,comment_details=comment_instance_details)
    email_subject = 'Do Not Reply ! Jobcard #{} Updated'.format(pk)
    email_message = 'Job number #{} has been REJECTED by {}. Go to http://127.0.0.1:8000/jobs/job/{} to see any comments'.format(pk,request.user.username,pk)
    print(email_message)
    send_mail(
        email_subject,
        email_message,
        'gavin.taylor.gis@gmail.com',
        [job.requisitioner.email],
        fail_silently=True,
    )
    return redirect('jobs:add_comment_to_job',pk=pk)

@login_required
def job_accept(request,pk):
    job = get_object_or_404(Job,pk=pk)
    job.accepted()
    comment_instance_details = 'Comment status changed to ACCEPTED' 
    comment_instance = Comments.objects.create(job=job,commentor=request.user,comment_details=comment_instance_details)
    email_subject = 'Do Not Reply ! Jobcard #{} Updated'.format(pk)
    email_message = 'Job number #{} has been ACCEPTED by {}. Go to http://127.0.0.1:8000/jobs/job/{} to see any comments'.format(pk,request.user.username,pk)
    send_mail(
        email_subject,
        email_message,
        'gavin.taylor.gis@gmail.com',
        [job.requisitioner.email],
        fail_silently=True,
    )
    return redirect('/jobs/')

@login_required
def job_decline(request,pk):
    job = get_object_or_404(Job,pk=pk)
    job.declined()
    comment_instance_details = 'Comment status changed to DECLINED' 
    comment_instance = Comments.objects.create(job=job,commentor=request.user,comment_details=comment_instance_details)
    email_subject = 'Do Not Reply ! Jobcard #{} Updated'.format(pk)
    email_message = 'Job number #{} has been DECLINED by {}. Go to http://127.0.0.1:8000/jobs/job/{} to see any comments'.format(pk,request.user.username,pk)
    print(email_message)
    send_mail(
        email_subject,
        email_message,
        'gavin.taylor.gis@gmail.com',
        [job.requisitioner.email],
        fail_silently=True,
    )
    return redirect('jobs:add_comment_to_job',pk=pk)

@login_required
def job_req_closeout(request,pk):
    job = get_object_or_404(Job,pk=pk)
    job.requestcloseout()
    comment_instance_details = 'Comment status changed to REQUEST CLOSEOUT' 
    comment_instance = Comments.objects.create(job=job,commentor=request.user,comment_details=comment_instance_details)
    email_subject = 'Do Not Reply ! Jobcard #{} Updated'.format(pk)
    email_message = 'Closeout on Job number #{} has been been requsted by {}. Go to http://127.0.0.1:8000/jobs/job/{} to see any comments'.format(pk,request.user.username,pk)
    print(email_message)
    send_mail(
        email_subject,
        email_message,
        'gavin.taylor.gis@gmail.com',
        [job.requisitioner.email],
        fail_silently=True,
    )
    return redirect('/jobs/')

@login_required
def job_closeout(request,pk):
    job = get_object_or_404(Job,pk=pk)
    job.closeout()
    comment_instance_details = 'Comment status changed to CLOSED' 
    comment_instance = Comments.objects.create(job=job,commentor=request.user,comment_details=comment_instance_details)
    return redirect('/jobs/')

@login_required
def job_get_selected_job_details(request,pk):
    sel_job = get_object_or_404(Job,pk=pk)
    context={
        'sel_job' : sel_job,
    }
    return render(request,'jobs/job_selected_details.html', context)
    
@login_required
def add_comment_to_job(request,pk):

    job = get_object_or_404(Job,pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.job = job
            comment.commentor = request.user
            comment.save()
            email_subject = 'Do Not Reply !  Jobcard #{} Updated'.format(pk)
            email_message = 'New comment added to job #{} by {}. Go to http://127.0.0.1:8000/jobs/job/{} to see any additional comments. \r\n \r\n {}'.format(pk,request.user.username,pk,comment.comment_details)
            send_mail(
                email_subject,
                email_message,
                'gavin.taylor.gis@gmail.com',
                [job.requisitioner.email],
                fail_silently=True,
                )
            return redirect('jobs:selected_job_details',pk=job.pk)

    else:
        form = CommentForm()
    return render(request,'jobs/comment_form.html',{'form':form})



@login_required
def add_jobcode(request,pk):
    job = get_object_or_404(Job,pk=pk)

    if request.method == 'POST':
        form = JobCodeForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            job.jobcard_number = submission.jobcard_number
            job.save()
            return redirect('jobs:selected_job_details',pk=job.pk)
    else:
        form = JobCodeForm()
    return render(request,'jobs/jobcode_form.html',{'form':form})