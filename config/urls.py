from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from braces.views import LoginRequiredMixin


class TempHomeView(LoginRequiredMixin, TemplateView):
    pass


urlpatterns = [
    url(r'^$', TempHomeView.as_view(template_name='pages/home.html'), name='home'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include(('sentinel.users.urls', 'users'), namespace='users')),
    url(r'^accounts/', include(('allauth.urls', 'allauth'), namespace='allauth')),
    url(r'^avatar/', include(('avatar.urls', 'avatar'), namespace='avatar')),

    # Your stuff: custom urls includes go here
    url(r'^agents/', include(('sentinel.agents.urls', 'agents'), namespace='agents')),
    url(r'^investors/', include(('sentinel.investors.urls', 'investors'), namespace='investors')),
    url(r'^transactions/', include(('sentinel.investors.transactions_urls', 'transactions'), namespace='transactions')),
    url(r'^settings/', include(('sentinel.core.urls', 'settings'), namespace='settings')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
