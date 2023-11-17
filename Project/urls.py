"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path

from django.conf import settings
from django.conf.urls.static import static

# from Management.views import signin
from Management import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index , name='index' ),

    # LOGIN
    path('signin/', views.signin , name='signin' ),
    path('signup/', views.signup , name='signup' ),
    path('signout/', views.signout , name='signout' ),

    # CUSTOMERS 
    path('user_data/', views.list_user_data , name='user_data'),
    path('user_data/<int:id>/data/', views.detail_user_data , name='detail_user_data'),
    path('user_data/<int:id>/update/', views.update_password , name='update_password'),
    path('user_data/create_coupon_points/', views.create_coupon_points , name='create_coupon_points'),
    path('user_data/<int:id>/delete_coupon/', views.delete_coupon , name='delete_coupon'),

    path('vehicle/', views.list_vehicles , name='vehicle'),
    path('vehicle/<int:id>/state/', views.state_vehicle , name='state_vehicle'),
    path('vehicle/<int:id>/delete/', views.delete_vehicle , name='delete_vehicle'),
    path('register_vehicle/', views.register_vehicle , name='register_vehicle'),

    path('appointment/', views.list_appointment , name='appointment'),
    path('appointment/<int:id>/cancel/', views.cancel_appointment , name='cancel_appointment'),
    path('register_date/', views.register_date ,name='register_date'),

    # path('points/', views.points, name='points'),

    # WORK USERS list_mechanic
    path('register_recepcionist/', views.register_recepcionist ,name='register_recepcionist'),

    path('list_mechanic/', views.list_mechanic ,name='list_mechanic'),
    path('list_mechanic/<int:id>/update/', views.update_mechanic ,name='update_mechanic'),
    path('list_mechanic/<int:id>/delete/', views.delete_mechanic ,name='delete_mechanic'),
    path('register_mechanic/', views.register_mechanic ,name='register_mechanic'),
    # path('list_mechanic/register_mechanic', views.register_mechanic ,name='register_mechanic'),

    path('list_jobs_pending/', views.list_jobs_pending ,name='list_jobs_pending'),
    path('list_jobs_pending/<int:id>/ot/', views.generate_ot ,name='generate_ot'),
    path('list_jobs_pending/<int:id>/delete/<str:job_type>/', views.delete_job ,name='delete_job_pending'),
    path('list_jobs_diary/', views.list_jobs_diary ,name='list_jobs_diary'),
    path('list_jobs_inprogress/', views.list_jobs_inprogress ,name='list_jobs_inprogress'),
    path('list_jobs_inprogress/<int:id>/checklist/', views.job_checklist ,name='checklist'),
    path('list_jobs_inprogress/<int:id>/update/', views.update_job ,name='update_job'),
    path('list_jobs_inprogress/<int:id>/<str:job_type>/delete/', views.delete_job ,name='delete_job_inprogress'),
    path('list_jobs_inprogress/<int:id>/completed/', views.completed_job ,name='completed_job'),
    path('list_jobs_completed/', views.list_jobs_completed ,name='list_jobs_completed'),
    path('list_jobs_completed/<int:id>/<str:job_type>/delete/', views.delete_job ,name='delete_job_completed'),
    path('list_service/<int:id_service>/<int:id>/delete/', views.delete_service ,name='delete_service'),

    # path('search/<str:patent>/', views.search_patent, name='search_patent')

    # re_path('search_patent/(?P<patent>[^/]+)?/', views.search_patent, name='search_patent')
    # re_path('search_patent/(?P<patent>.*)/', views.search_patent, name='search_patent')
    # re_path('search_patent/(?P<patent>[.*]+)?/', views.search_patent, name='search_patent')
    re_path('search_patent/(?P<patent>[\w\d]+)?/', views.search_patent, name='search_patent')



    # (?P<patent>.+)/$
    #  /(?P<patent>[^/]+)?/
    # path('list_jobs/', views.list_jobs ,name='list_jobs'),
    # path('list_jobs/<int:id>/checklist/', views.job_checklist ,name='checklist'),
    # path('list_jobs/<int:id>/ot/', views.generate_ot ,name='generate_ot'),
    # path('list_jobs/<int:id>/update/', views.update_job ,name='update_job'),
    # path('list_jobs/<int:id>/delete/', views.delete_job ,name='delete_job'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
