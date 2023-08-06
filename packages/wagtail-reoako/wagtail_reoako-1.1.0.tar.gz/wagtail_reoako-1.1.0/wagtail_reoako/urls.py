from django.conf.urls import url

from wagtail_reoako.views import modal_view, search_view

urlpatterns = [
    # these should be prefixed with admin route when consumed
    # i.e. url(r'^admin/', include('wagtail_reoako.urls')),
    url(r'^reoako-modal/?$', modal_view, name='reoako_modal'),
    url(r'^reoako-modal/search/?$', search_view, name='reoako_modal_search')
]
