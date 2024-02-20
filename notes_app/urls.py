from django.urls import path
from .views import *

urlpatterns = [
    path('signup', sign_up, name='sign_up'),
    path('login',login, name='login'),
    path('notes/create',create_note,name='create_note'),
    path('notes/<int:id>',get_or_update_note,name='get_or_update_note'),
    path('notes/share',share_note,name='share_note'),
    path('notes/version-history/<int:id>', get_note_version_history, name='get_note_version_history'),
]
