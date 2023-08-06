from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from pkg_resources import parse_version
from wagtail import __version__ as WAGTAIL_VERSION

from wagtail.admin import urls as wagtailadmin_urls

if parse_version(WAGTAIL_VERSION) < parse_version('3.0'):
    from wagtail.core import urls as wagtail_urls
else:
    from wagtail import urls as wagtail_urls

from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = []

urlpatterns += [
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
