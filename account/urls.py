from django.conf.urls import include, url
from django.views.generic.base import RedirectView

from account.views import signin


urlpatterns = [
    # Examples:
    # url(r'^$', 'jeight.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(pattern_name='signin'), name='go-to-signin'),
    url(r'^signin/$', signin, name='signin'),
]
