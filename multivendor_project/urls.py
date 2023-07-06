from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(('App_login.urls'), namespace='App_login')),
    path('', include(('App_shop.urls'), namespace='App_shop')),
    path('shop/', include(('App_order.urls'), namespace='App_order')),
    path('payment/', include(('App_payment.urls'), namespace='App_payment'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
