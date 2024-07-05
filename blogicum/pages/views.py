from django.shortcuts import render


def about(request):
    return render(request, 'pages/about.html')


def rules(request):
    return render(request, 'pages/rules.html')


def page_not_found(request, exception):
    """Ошибка 404"""
    return render(request, 'pages/404.html', status=404)


def error_500(request, exception):
    """Ошибка 500"""
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    """Ошибка 403"""
    return render(request, 'core/403csrf.html', status=403)
