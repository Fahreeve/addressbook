from django.conf.urls import url

from book.views import NoteListView, NoteFormView, NoteTemplateView, NoteDeleteView, CSVView, NoteCreateView

urlpatterns = [
    url(r'^list/$', NoteListView.as_view(), name='note_list'),
    url(r'^export/$', CSVView.as_view(), name='note_export'),
    url(r'^note/create/$', NoteCreateView.as_view(), name='note_create'),
    url(r'^note/(?P<pk>\d+)/$', NoteTemplateView.as_view(), name='note'),
    url(r'^note/(?P<pk>\d+)/edit/$', NoteFormView.as_view(), name='note_edit'),
    url(r'^note/(?P<pk>\d+)/delete/$', NoteDeleteView.as_view(), name='note_delete'),
]
