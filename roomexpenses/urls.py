from django.conf.urls import include, url
from django.views.generic.base import TemplateView

urlpatterns = [
    # Examples:
    # url(r'^$', 'jeight.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', TemplateView.as_view(template_name='roomexpenses/expenses.html'), name='home'),

]
