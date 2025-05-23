from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
from django.contrib.auth import login
from .models import Profile
from .forms import ProfileForm


class AdListView(ListView):
    model = Ad
    paginate_by = 10
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    def get_queryset(self):
        qs = super().get_queryset().select_related('user').order_by('-created_at')
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category:
            qs = qs.filter(category__iexact=category)
        if condition:
            qs = qs.filter(condition__iexact=condition)
        return qs

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'

class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AdOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().user == self.request.user

class AdUpdateView(LoginRequiredMixin, AdOwnerMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')

class AdDeleteView(LoginRequiredMixin, AdOwnerMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ads:ad_list')

# Exchange Proposals
class ExchangeProposalListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = 'ads/exchangeproposal_list.html'
    context_object_name = 'proposals'
    def get_queryset(self):
        qs = super().get_queryset().select_related('ad_sender', 'ad_receiver')
        return qs.filter(Q(ad_sender__user=self.request.user) | Q(ad_receiver__user=self.request.user))

class ExchangeProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'ads/exchangeproposal_form.html'
    success_url = reverse_lazy('ads:proposal_list')
    def form_valid(self, form):
        if form.instance.ad_sender.user != self.request.user:
            form.add_error('ad_sender', 'Вы должны быть автором объявления-отправителя.')
            return self.form_invalid(form)

        # запрет на обмен своими же объявлениями между собой
        if form.instance.ad_receiver.user == self.request.user:
            form.add_error(None, 'Нельзя обмениваться двумя своими объявлениями.')
            return self.form_invalid(form)

        return super().form_valid(form)

class ExchangeProposalUpdateView(LoginRequiredMixin, UpdateView):
    model = ExchangeProposal
    fields = ['status']
    template_name = 'ads/exchangeproposal_update_form.html'
    success_url = reverse_lazy('ads:proposal_list')
    def get_queryset(self):
        return super().get_queryset().filter(ad_receiver__user=self.request.user)


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        response = super().form_valid(form)  # сохраняем User
        login(self.request, self.object)  # auto-login
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "registration/profile.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "registration/profile_edit.html"

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy("profile")
