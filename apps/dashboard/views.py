from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, ListView


class ProfileView(LoginRequiredMixin, UpdateView):
    fields = (
        'first_name',
        'last_name',
    )
    template_name = 'dashboard/profile.html'
    success_url = reverse_lazy('dashboard:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Your information updated successfully.'))
        return super().form_valid(form)


class BookmarkListView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/bookmark_list.html'

    def get_queryset(self):
        return self.request.user.bookmarks.prefetch_related('genres')


class DeviceListView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/device_list.html'

    def get_queryset(self):
        return self.request.user.logged_in_devices.all()
