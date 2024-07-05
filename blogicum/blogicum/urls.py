from django.contrib import admin
from django.urls import path, include
from django.conf import settings


app_name = 'blogicum'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls'), name='blog'),
    path('pages/', include('pages.urls'), name='pages'),
]

# Если проект запущен в режиме разработки...
if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

handler404 = 'pages.views.page_not_found'
