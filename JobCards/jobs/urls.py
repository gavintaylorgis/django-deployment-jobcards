from django.urls import path
from . import views

app_name = 'jobs'


urlpatterns = [
    path('', views.JobsList.as_view(), name="all"),
    path('inactive/', views.ClosedJobsList.as_view(),name='inactive'),
    path("new/", views.CreateJob.as_view(), name="create"),
    path("by/<username>/",views.UserJob.as_view(),name="for_user"),
    path("<int:pk>/update/",views.UpdateJob.as_view(),name="update"),
    path("delete/<int:pk>/",views.DeleteJob.as_view(),name="delete"),
    path('job/<int:pk>/approve/',views.job_approve,name='job_approve'),
    path('job/<int:pk>/rework/',views.job_rework,name='job_rework'),
    path('job/<int:pk>/reject/',views.job_reject,name='job_reject'),
    path('job/<int:pk>/accept/',views.job_accept,name='job_accept'),
    path('job/<int:pk>/decline/',views.job_decline,name='job_decline'),
    path('job/<int:pk>/requestcloseout/',views.job_req_closeout,name='job_requestcloseout'),
    path('job/<int:pk>/closeout/',views.job_closeout,name='job_closeout'),
    path('job/<int:pk>/jobcode/',views.add_jobcode,name='job_addjobcode'),
    path('job/<int:pk>',views.job_get_selected_job_details, name='selected_job_details'),
    path('job/<int:pk>/comment/',views.add_comment_to_job,name='add_comment_to_job'),
 
    

]