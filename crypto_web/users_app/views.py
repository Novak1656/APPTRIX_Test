from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.decorators.http import require_http_methods
from .forms import RegistrationForm
from main_app.models import Cryptocurrency
from .models import Favorites


class RegistrationView(FormView):
    """
        Registration page
    """
    template_name = 'users_app/user_registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('main_page')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect('main_page')
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super(RegistrationView, self).form_valid(form)


@require_http_methods(['POST'])
def login_view(request):
    """
        Endpoint for user login
    """
    resp_data = request.POST
    model = get_user_model()
    user = model.objects.filter(username=resp_data.get('username'))
    if not user:
        messages.error(request, 'Username invalid', extra_tags='login_error')
        return redirect(request.META['HTTP_REFERER'])
    if not check_password(resp_data.get('password'), user.password):
        messages.error(request, 'Password invalid')
        return redirect(request.META['HTTP_REFERER'], extra_tags='login_error')
    login(request, user)
    return redirect('main_page')


def logout_view(request):
    """
        Endpoint for user login
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('main_page')


@login_required
@require_http_methods(['POST'])
@transaction.atomic
def add_in_favorite(request):
    """
         Endpoint for add cryptocurrency in favorite
    """
    crypt_pk = request.POST.get('crypt_pk')
    crypt_obj = get_object_or_404(Cryptocurrency, pk=crypt_pk)
    Favorites.objects.create(user=request.user, crypto=crypt_obj)
    return redirect(request.META['HTTP_REFERER'])


@login_required
@require_http_methods(['POST'])
@transaction.atomic
def delete_from_favorite(request):
    """
        Endpoint for delete cryptocurrency from favorite
    """
    crypt_pk = request.POST.get('crypt_pk')
    crypt_obj = get_object_or_404(Favorites, user=request.user, crypto_id=crypt_pk)
    crypt_obj.delete()
    return redirect(request.META['HTTP_REFERER'])


class UserFavoritesView(LoginRequiredMixin, TemplateView):
    """
        Favorites page
    """
    template_name = 'main_app/crypto_list.html'
    extra_context = {'page_title': 'My Favorites'}
    login_url = reverse_lazy('user_login')

    def get_context_data(self, **kwargs):
        context = super(UserFavoritesView, self).get_context_data(**kwargs)
        queryset = Cryptocurrency.objects.filter(pk__in=self.request.user.favorites.values_list('crypto_id', flat=True))
        context['crypto_info'] = queryset
        context['user_favorites'] = [crypt.id for crypt in queryset]
        return context
