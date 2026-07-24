"""college_finder_app URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('universities/', include('universities.urls')),
    path('compare/', include('college_comparison.urls')),
    path('bookmarks/', include('bookmarks.urls')),
    path('blogs/', include('blogs.urls')),
    path('faqs/', include('faqs.urls')),
    path('', include('users.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
]

# --- Static files (dev only — WhiteNoise handles this in production) -------
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# --- Media files -----------------------------------------------------------
# In DEBUG mode: Django's dev server serves media via the helper below.
# In production: controlled by SERVE_MEDIA_IN_PRODUCTION in settings.
#   True  → Django serves /media/ (fine for low-traffic hobby sites).
#   False → Configure your reverse-proxy / CDN to serve MEDIA_ROOT instead.
if settings.DEBUG or getattr(settings, 'SERVE_MEDIA_IN_PRODUCTION', False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
