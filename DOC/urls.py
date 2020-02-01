from django.contrib import admin
from django.urls import path
from .views import home,doc,genrate, deleteSession, genrateBonafide, genrateLeaving, doc_log 

urlpatterns = [
    path('home/',home,name='home'),
    path('doc/',doc,name='doc'),
    path('genrate/',genrate,name='genrate'),
    path('doc_log/',doc_log,name='doc_log'),
    path('deleteSession',deleteSession,name='deleteSession'),
    path('genrateBonafide',genrateBonafide,name='genrateBonafide'),
    path('genrateLeaving',genrateLeaving,name='genrateLeaving'),
]