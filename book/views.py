import csv

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from book.forms import NoteForm
from book.models import Note


class NoteListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'
    paginate_by = 20
    template_name = 'notes.html'
    queryset = Note.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = NoteForm()
        return context


class NoteTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'
    template_name = 'note.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['object'] = get_object_or_404(Note, pk=kwargs['pk'])
        return context


class NoteFormView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'
    template_name = 'note_edit.html'
    form_class = NoteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pk = self.kwargs.get('pk', None)
        kwargs['instance'] = get_object_or_404(Note, pk=pk, user=self.request.user)
        return kwargs

    def form_valid(self, form):
        note = form.save(commit=False)
        note.user = self.request.user
        note.save()
        messages.success(self.request, _('Запись успешно обновлена'))
        return HttpResponseRedirect(reverse_lazy('note', kwargs={'pk': note.pk}))


class NoteCreateView(LoginRequiredMixin, CreateView):
    form_class = NoteForm
    success_url = reverse_lazy('note_list')
    template_name = 'note_edit.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, _('Запись успешно создана'))
        # return HttpResponseRedirect(reverse_lazy('note_list'))
        return HttpResponse(status=201)


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'
    model = Note
    success_url = reverse_lazy('note_list')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, _('Запись успешно удалена'))
        return response


class CSVView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'

        writer = csv.writer(response)
        fields = ['name', 'surname', 'patronymic', 'address', 'phone_number', 'email', 'comment']
        writer.writerow([Note._meta.get_field(f).verbose_name.title() for f in fields])

        for obj in Note.objects.filter(user=request.user):
            writer.writerow([getattr(obj, f) for f in fields])
        return response
