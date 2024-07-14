from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

# Импортируем функцию, позволяющую серверу разработки отдавать файлы.
from django.conf.urls.static import static


app_name = 'blogicum'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls'), name='blog'),
    path('pages/', include('pages.urls'), name='pages'),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('login'),
        ),
        name='registration',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Если проект запущен в режиме разработки...
if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

handler403 = 'pages.views.csrf_failure'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.error_500'
