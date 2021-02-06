from django import forms
from bootstrap_datepicker_plus import DatePickerInput,DateTimePickerInput
from jobs.models import Job,Comments

class JobForm(forms.ModelForm):
    

    class Meta():
        model = Job
        fields = ['asset','priority','request_completed_by_date','job_descrip','contractor_group','conctractor','status','approver','job_type','jobcard_number','job_closed']
        widgets= {
        'request_completed_by_date': DateTimePickerInput(),

        }

class CommentForm(forms.ModelForm):
    
    class Meta():
        model = Comments
        fields = ['comment_details',]
        
        widgets = {
            'text' : forms.Textarea()
        }

class JobCodeForm(forms.ModelForm):
    class Meta():
        model = Job
        fields = ['jobcard_number']

