from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index), # login and registration
    path("dashboard/",views.dashboard), # table of proects
    path('createproject/',views.createproject), # the create project page
    path('project/<int:id>/details',views.details), 
    path('editproject/<int:id>',views.editproject), # the edit page
    path('register/',views.register), # function call 
    path('login/',views.login), # function call
    path('addproject/',views.addproject), # to add the project
    path('deleteproject/<int:projectid>/',views.deleteproject),
    path('join/<int:projectid>/<int:userid>',views.join),
    path('leave/<int:projectid>/<int:userid>/',views.leave),
    path('logout/',views.logout) 
]