from django.conf.urls import patterns, include, url
from liwu.settings import MEDIA_ROOT
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^items', 'liwu.kgapp.views.showItems'),
    url(r'^p', 'liwu.kgapp.views.processLiwuItem'),
    url(r'^import2beEdit', 'liwu.kgapp.views.import2beEdit'),
    url(r'^showToBeEdited', 'liwu.kgapp.views.showToBeEdited'),
    url(r'^uploadSelectedLiwu', 'liwu.kgapp.views.uploadSelectedLiwu'),
    url(r'^uploadImgXheditor/$', 'liwu.kgapp.views.uploadImgXheditor'),
    url(r'^save2hasEditedDB','liwu.kgapp.views.save2hasEditedDB'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve', {'document_root': '/disk1/liwuDjango/liwu/liwu/media/'}),
    url(r'^showCandidateDetail', 'liwu.kgapp.views.showLiwuDetail')
)
