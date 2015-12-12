from django.conf.urls import include, url
from account.views import signin


urlpatterns = [
    # Examples:
    # url(r'^$', 'jeight.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', signin, name='signin'),

]
