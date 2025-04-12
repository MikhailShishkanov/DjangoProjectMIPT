from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cobra_project_app.models import Test
from cobra_project_site import settings


@login_required(login_url=settings.LOGIN_URL)
def home_view(request):
    user_tests = Test.objects.filter(user=request.user).order_by('id')
    return render(request, 'home_page.html', {'tests': user_tests})
