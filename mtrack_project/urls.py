from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from rapidsms_httprouter.urls import urlpatterns as router_urls
from rapidsms_xforms.urls import urlpatterns as xform_urls
from cvs.urls import urlpatterns as cvs_urls
from healthmodels.urls import urlpatterns as healthmodels_urls
from contact.urls import urlpatterns as contact_urls
from mtrack.urls import urlpatterns as mtrack_urls
from mcdtrac.urls import urlpatterns as mcdtrac_urls
from ussd.urls import urlpatterns as ussd_urls
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^my-project/', include('my_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
#    url(r'^users/', include('smartmin.users.urls')),
    (r'^admin/', include(admin.site.urls)),
    # RapidSMS core URLs
    (r'^account/', include('rapidsms.urls.login_logout')),
    url(r'^$', direct_to_template, {'template':'mtrack/dashboard.html'}, name='rapidsms-dashboard'),
    url('^accounts/login', 'rapidsms.views.login'),
    url('^accounts/logout', 'rapidsms.views.logout'),
    # RapidSMS contrib app URLs
    (r'^ajax/', include('rapidsms.contrib.ajax.urls')),
    (r'^export/', include('rapidsms.contrib.export.urls')),
    (r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    (r'^locations/', include('rapidsms.contrib.locations.urls')),
    (r'^messaging/', include('rapidsms.contrib.messaging.urls')),
    (r'^registration/', include('auth.urls')),
    (r'^scheduler/', include('rapidsms.contrib.scheduler.urls')),
    (r'^polls/', include('poll.urls')),
    (r'^logistics/', include('logistics.urls')),
    (r'^reports/', include('email_reports.urls')),
) + mtrack_urls + router_urls + cvs_urls + healthmodels_urls + contact_urls + ussd_urls + mcdtrac_urls +xform_urls

if settings.DEBUG:
    urlpatterns += patterns('',
        # helper URLs file that automatically serves the 'static' folder in
        # INSTALLED_APPS via the Django static media server (NOT for use in
        # production)
        (r'^', include('rapidsms.urls.static_media')),
    )

from rapidsms_httprouter.router import get_router
get_router(start_workers=True)

