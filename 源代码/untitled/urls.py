"""Living_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from dormsys import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dormsys/index', views.index),
    path('dormsys/login', views.login),
    path('dormsys/logout', views.logout),

    # student
    path('dormsys/student_main', views.student_main),
    path('dormsys/change_student_info', views.change_student_info),
    path('dormsys/change_or_add_emergency_info', views.change_or_add_emergency_contact),
    path('dormsys/deal_with_dorm', views.deal_with_dorm),
    path('dormsys/search_dorm_info', views.search_dorm_info),
    path('dormsys/search_announcement', views.search_announcement),
    path('dormsys/enter_dorm', views.enter_dorm),
    path('dormsys/delete_dorm', views.delete_dorm),
    path('dormsys/change_dorm', views.change_dorm),
    path('dormsys/search_empty_dorm1', views.search_empty_dorm1),
    path('dormsys/matter_info',views.matter_info),



    #tutor
    path('dormsys/tutor_main', views.tutor_main),
    path('dormsys/change_tutor_info', views.change_tutor_info),
    path('dormsys/search_student_info1',views.search_student_info_from_tutor),
    path('dormsys/allocate_dorm',views.allocate_dorm),
    path('dormsys/approve_info',views.approve_info),
    path('dormsys/approve_agree/<int:matter_id>',views.approve_agree),
    path('dormsys/approve_disagree/<int:matter_id>',views.approve_disagree),
    path('dormsys/search_empty_dorm2', views.search_empty_dorm2),
    path('dormsys/search_no_dorm_student/', views.search_no_dorm_student),


    #supervisor
    path('dormsys/supervisor_main', views.supervisor_main),
    path('dormsys/change_supervisor_info', views.change_supervisor_info),
    path('dormsys/search_student_info2',views.search_student_info_from_supervisor),
    path('dormsys/make_announcement',views.make_announcement)
]
