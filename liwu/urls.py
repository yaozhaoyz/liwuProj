from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^items', 'liwu.kgapp.views.showItems'),
    url(r'^p', 'liwu.kgapp.views.processLiwuItem'),
    url(r'^import', 'liwu.kgapp.views.importData2ItemDB'),
    url(r'^showCandidate', 'liwu.kgapp.views.showCandidate'),
    url(r'^showCandidateDetail', 'liwu.kgapp.views.showLiwuDetail')
)
