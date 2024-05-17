"""webV1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from app import views

urlpatterns = [
    path('', views.index,name='home'), 
    path('admin/', admin.site.urls),
    
    path('database/mTSA', views.browse_mtsa,name='database_mTSA'),
    path('database/aeTSA', views.browse_aetsa,name='database_aeTSA'),
    path('search/mTSA/', views.search_database_mTSA,name='search_database_mTSA'),
    path('search/aeTSA/', views.search_database_aeTSA,name='search_database_aeTSA'),
    path('about', views.about,name='about'),

    # path('database/mTSA/detail/<str:tnh>',views.detail_page_mtsa, name = 'detail_page_mtsa_url'),
    path('database/mTSA/RNA/detail/<int:id>',views.detail_page_mtsa, name = 'detail_page_mtsa'),
    path('database/mTSA/DNA/detail/<int:id>',views.detail_page_mtsa_dna, name = 'detail_page_mtsa_dna'),
    path('database/aeTSA/detail/<int:id>',views.detail_page_aetsa, name = 'detail_page_aetsa'),

    path('database/mTSA/<str:source>/detail/relational_transcript/<int:id>',views.relational_transcript, name = 'relational_transcript'),


    path('download/', views.download,name='download'), 
    path('download_mTSA/', views.download_mTSA,name='download_mTSA'),
    path('download/user_filter_peptides', views.download_user_filter_peptides,name='download_user_filter_peptides'), 
    
    
    path('upload', views.upload,name='upload'),
    path('upload_result', views.upload_result,name='upload_result'),
    path('view_result/<str:job_uuid>', views.view_result,name='view_result'),
    path('view_result/download_result/<str:job_uuid>', views.download_prioritizing_result,name='download_prioritizing_result'),
    
    path('user_info_job', views.user_info_job,name='user_info_job'),
    path('summary', views.summary,name='summary'),


# =======test=========
    path('test', views.test,name='test'),
    path('test1', views.test1,name='test1'), 
    path('get_data/', views.get_data, name='get_data'),
    path('send_email',views.send_email,name = 'send_email') ,
    path('search/',views.listall,name='reference_guided'),
    path('<str:mode>',views.sort),



]
