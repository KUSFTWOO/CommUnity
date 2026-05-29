from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from collections import Counter
from .models import Survey, Question, Response, Answer
from .forms import SurveyForm


def list_view(request):
    """설문 목록 - 진행중/완료된 설문 구분"""
    all_surveys = Survey.objects.prefetch_related('questions').all()

    active_surveys = [s for s in all_surveys if not s.is_expired]
    closed_surveys = [s for s in all_surveys if s.is_expired]

    # 사용자의 응답 정보 추가
    if request.user.is_authenticated:
        user_responses = Response.objects.filter(survey__in=all_surveys, respondent=request.user).values_list('survey_id', 'pk')
        user_response_map = {survey_id: response_pk for survey_id, response_pk in user_responses}

        for survey in active_surveys + closed_surveys:
            if survey.pk in user_response_map:
                survey.user_response_pk = user_response_map[survey.pk]
            else:
                survey.user_response_pk = None

    context = {
        'active_surveys': active_surveys,
        'closed_surveys': closed_surveys,
    }

    return render(request, 'surveys/list.html', context)


def respond_view(request, pk):
    """설문 응답"""
    survey = get_object_or_404(Survey.objects.prefetch_related('questions'), pk=pk)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        response_exists = Response.objects.filter(survey=survey, respondent=request.user).exists()
        if response_exists:
            return redirect('surveys:results', pk=survey.pk)

        # Response 생성
        response = Response.objects.create(
            survey=survey,
            respondent=request.user if not survey.is_anonymous else None
        )

        # 각 질문에 대한 Answer 저장
        for question in survey.questions.all():
            if question.question_type == 'MULTIPLE':
                answer_text = '|'.join(request.POST.getlist(f'question_{question.id}'))
            else:
                answer_text = request.POST.get(f'question_{question.id}', '')

            Answer.objects.create(
                response=response,
                question=question,
                answer_text=answer_text
            )

        return redirect('surveys:response_detail', survey_pk=survey.pk, response_pk=response.pk)

    questions = survey.questions.all()
    user_response = None
    if request.user.is_authenticated:
        user_response = Response.objects.filter(survey=survey, respondent=request.user).first()

    context = {
        'survey': survey,
        'questions': questions,
        'is_expired': survey.is_expired,
        'user_response': user_response,
    }

    return render(request, 'surveys/respond.html', context)


@login_required
def create_view(request):
    """설문 생성 - 관리자만"""
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.created_by = request.user
            survey.save()

            # 질문들 저장
            question_count = int(request.POST.get('question_count', 0))
            for i in range(question_count):
                text = request.POST.get(f'question_{i}_text')
                question_type = request.POST.get(f'question_{i}_type')
                required = request.POST.get(f'question_{i}_required') == 'on'
                options = request.POST.get(f'question_{i}_options', '')

                if text and question_type:
                    Question.objects.create(
                        survey=survey,
                        text=text,
                        question_type=question_type,
                        required=required,
                        options=options,
                        order=i
                    )

            return redirect('surveys:results', pk=survey.pk)
    else:
        form = SurveyForm()

    context = {'form': form}
    return render(request, 'surveys/form.html', context)


@login_required
def results_view(request, pk):
    """설문 결과 - 관리자만"""
    if not request.user.is_staff:
        raise PermissionDenied

    survey = get_object_or_404(Survey.objects.prefetch_related('questions', 'responses'), pk=pk)
    questions = survey.questions.all()

    # 결과 분석
    question_results = []
    for question in questions:
        answers = Answer.objects.filter(question=question).values_list('answer_text', flat=True)

        if question.question_type == 'CHOICE':
            counter = Counter(answers)
            total = sum(counter.values())
            options_data = []
            for option in question.parsed_options:
                count = counter.get(option, 0)
                percentage = (count / total * 100) if total > 0 else 0
                options_data.append({
                    'option': option,
                    'count': count,
                    'percentage': round(percentage, 1)
                })
            question_results.append({
                'question': question,
                'type': 'CHOICE',
                'data': options_data,
                'total': total
            })

        elif question.question_type == 'MULTIPLE':
            all_selected = []
            for answer in answers:
                if answer:
                    all_selected.extend(answer.split('|'))
            counter = Counter(all_selected)
            total = len(answers)
            options_data = []
            for option in question.parsed_options:
                count = counter.get(option, 0)
                percentage = (count / total * 100) if total > 0 else 0
                options_data.append({
                    'option': option,
                    'count': count,
                    'percentage': round(percentage, 1)
                })
            question_results.append({
                'question': question,
                'type': 'MULTIPLE',
                'data': options_data,
                'total': total
            })

        elif question.question_type == 'SCALE':
            numeric_answers = []
            for answer in answers:
                try:
                    numeric_answers.append(int(answer))
                except (ValueError, TypeError):
                    pass
            avg_score = sum(numeric_answers) / len(numeric_answers) if numeric_answers else 0
            question_results.append({
                'question': question,
                'type': 'SCALE',
                'average': round(avg_score, 2),
                'total': len(numeric_answers)
            })

        elif question.question_type in ['TEXT', 'TEXTAREA']:
            question_results.append({
                'question': question,
                'type': 'TEXT' if question.question_type == 'TEXT' else 'TEXTAREA',
                'answers': list(answers),
                'total': len(answers)
            })

    context = {
        'survey': survey,
        'question_results': question_results,
        'total_responses': survey.total_responses,
    }

    return render(request, 'surveys/results.html', context)


@login_required
def delete_view(request, pk):
    """설문 삭제 - 관리자만"""
    if not request.user.is_staff:
        raise PermissionDenied

    survey = get_object_or_404(Survey, pk=pk)

    if request.method == 'POST':
        survey.delete()
        return redirect('surveys:list')

    context = {'survey': survey}
    return render(request, 'surveys/confirm_delete.html', context)


@login_required
def response_view(request, survey_pk, response_pk):
    """개인별 응답 상세 조회"""
    survey = get_object_or_404(Survey, pk=survey_pk)
    response = get_object_or_404(Response, pk=response_pk, survey=survey)

    # 권한 체크: 자신의 응답이거나 관리자
    if response.respondent != request.user and not request.user.is_staff:
        raise PermissionDenied

    # 응답 상세 정보 구성
    questions_with_answers = []
    for question in survey.questions.all():
        answer = response.answers.filter(question=question).first()
        answer_text = answer.answer_text if answer else ''

        answer_data = {
            'question': question,
            'answer_text': answer_text,
        }

        # 선택 항목이 있으면 파싱
        if question.question_type in ['CHOICE', 'MULTIPLE']:
            if question.question_type == 'MULTIPLE':
                selected_options = answer_text.split('|') if answer_text else []
            else:
                selected_options = [answer_text] if answer_text else []
            answer_data['selected_options'] = selected_options

        questions_with_answers.append(answer_data)

    context = {
        'survey': survey,
        'response': response,
        'questions_with_answers': questions_with_answers,
        'is_own_response': response.respondent == request.user,
    }

    return render(request, 'surveys/response_detail.html', context)
