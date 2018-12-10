"""passbook Invitation administration"""
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, DeleteView, ListView

from passbook.admin.mixins import AdminRequiredMixin
from passbook.core.forms.invitations import InvitationForm
from passbook.core.models import Invitation


class InvitationListView(AdminRequiredMixin, ListView):
    """Show list of all invitations"""

    model = Invitation
    template_name = 'administration/invitation/list.html'


class InvitationCreateView(SuccessMessageMixin, AdminRequiredMixin, CreateView):
    """Create new Invitation"""

    template_name = 'generic/create.html'
    success_url = reverse_lazy('passbook_admin:invitations')
    success_message = _('Successfully created Invitation')
    form_class = InvitationForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)

class InvitationDeleteView(SuccessMessageMixin, AdminRequiredMixin, DeleteView):
    """Delete invitation"""

    model = Invitation
    template_name = 'generic/delete.html'
    success_url = reverse_lazy('passbook_admin:invitations')
    success_message = _('Successfully updated Invitation')