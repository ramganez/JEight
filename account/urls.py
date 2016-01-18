from django.conf.urls import include, url
from django.views.generic.base import RedirectView, TemplateView


from account.views import signin, signout


urlpatterns = [
    # Examples:
    # url(r'^$', 'jeight.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(pattern_name='signin'), name='go-to-signin'),
    url(r'^signin/$', signin, name='signin'),
    url(r'^signout/$', signout, name='signout'),
    # url(r'^ske/$', TemplateView.as_view(template_name='account/ske.html'), name='ske'),
    # url(r'^datep/$', TemplateView.as_view(template_name='account/datep.html'), name='datep'),
    # url(r'^history-temp/$', TemplateView.as_view(template_name='account/history_temp.html'), name='history_temp'),
]
