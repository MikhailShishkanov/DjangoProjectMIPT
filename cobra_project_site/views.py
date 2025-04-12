from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from cobra_project_app.forms import TestForm
from cobra_project_app.models import Test, Question, Answer
from cobra_project_site import settings


@login_required(login_url=settings.LOGIN_URL)
def home_view(request):
    user_tests = Test.objects.filter(user=request.user).order_by('id')
    return render(request, 'home_page.html', {'tests': user_tests})


@login_required(login_url=settings.LOGIN_URL)
def test_compiling(request):
    if request.method == 'POST':
        # Обработка формы теста
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            # Создаем тест
            test = test_form.save(commit=False)
            test.user = request.user
            test.save()

            # Обрабатываем вопросы и ответы
            question_index = 0
            while f'question_{question_index}_name' in request.POST:
                question_name = request.POST.get(f'question_{question_index}_name')
                question = Question.objects.create(
                    test=test,
                    name=question_name
                )

                # Обрабатываем ответы для вопроса
                answer_index = 0
                while f'question_{question_index}_answer_{answer_index}_name' in request.POST:
                    answer_name = request.POST.get(f'question_{question_index}_answer_{answer_index}_name')
                    correctness = request.POST.get(
                        f'question_{question_index}_answer_{answer_index}_correctness') == 'on'

                    Answer.objects.create(
                        question=question,
                        name=answer_name,
                        correctness=correctness
                    )
                    answer_index += 1

                question_index += 1

            return redirect('home')

    else:
        test_form = TestForm()

    return render(request, 'test_compiling.html', {
        'test_form': test_form,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')