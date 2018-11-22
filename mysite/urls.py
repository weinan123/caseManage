"""project_weinan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from main import views  as main

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', main.index,name='index'),
    url(r'^index/$', main.index,name='index'),
    url(r'^login/$', main.login),
    url(r'^logout/$', main.logout,),
    url(r'^register/$', main.register),
    url(r'^yyBroke/([\w\W]*)$', main.yyBroke,),
    url(r'^([\w\W]*)/([\w\W]*)/caseModel/$', main.yyCaseModel),
    url(r'^caseModel_delete/$', main.caseModel_delete, ),
    url(r'^yyBroke_delete/$', main.yyBroke_delete),
    url(r'^uploadFiles/$', main.uploadFiles, ),
    url(r'^yyBroke_search/([\w\W]*)$', main.yyBroke_search),
    url(r'^yyBrokeCase_delete/$', main.yyBrokeCase_delete, ),
    url(r'^yyBrokeCase_insert/$', main.yyBrokeCase_insert),
    url(r'^yyBrokeCase_save/$', main.yyBrokeCase_save, ),
    url(r'^execteLog/$', main.execteLog, ),

]
