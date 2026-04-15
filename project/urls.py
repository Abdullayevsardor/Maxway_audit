 
from django.contrib import admin
from django.urls import path, include, re_path # re_path qo'shildi
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve # serve funksiyasi qo'shildi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("checklist.urls")),
]
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
# # Productionda (DEBUG=False) rasmlar ko'rinishi uchun bu qism kerak
# if not settings.DEBUG:
#     urlpatterns += [
#         re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
#         re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
#     ]
# else:
#     # Development rejimida (DEBUG=True)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
