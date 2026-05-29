from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from datetime import date, datetime, timedelta
from calendar import monthcalendar, month_name
import calendar as cal_module

from .models import Event
from .forms import EventForm


def get_calendar_data(year, month):
    """캘린더 데이터 생성"""
    # 월의 첫 날과 마지막 날
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)

    # 월간 일정 조회
    events = Event.objects.filter(
        is_deleted=False,
        start_date__lte=last_day,
        start_date__gte=first_day,
    ).select_related('created_by')

    # 날짜별 일정 매핑 (캘린더 셀의 day 숫자와 키 일치)
    events_by_date = {}
    for event in events:
        day_key = event.start_date.day
        events_by_date.setdefault(day_key, []).append(event)

    # 캘린더 뷰 데이터
    cal = monthcalendar(year, month)

    return {
        'year': year,
        'month': month,
        'month_name': month_name[month],
        'calendar': cal,
        'events_by_date': events_by_date,
        'today': datetime.now().date(),
        'first_weekday': first_day.weekday(),
    }


def list_view(request):
    """캘린더 목록 - 누구나 조회 가능"""
    # 현재 연도, 월 (쿼리 파라미터에서 가져옴)
    today = datetime.now().date()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # 이전/다음 달 계산
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    cal_data = get_calendar_data(year, month)

    context = {
        **cal_data,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    }
    return render(request, 'calendar_app/list.html', context)


def detail_view(request, pk):
    """일정 상세 - 누구나 조회 가능"""
    event = get_object_or_404(Event, pk=pk, is_deleted=False)

    # 구글 캘린더 추가 URL
    from urllib.parse import quote
    title = quote(event.title)
    details = quote(event.description or '')
    location = quote(event.location or '')

    start_str = event.start_date.isoformat()
    end_str = (event.end_date or event.start_date).isoformat()

    google_calendar_url = (
        f"https://calendar.google.com/calendar/render?"
        f"action=TEMPLATE&text={title}&dates={start_str.replace('-', '')}"
        f"/{end_str.replace('-', '')}&details={details}&location={location}"
    )

    context = {
        'event': event,
        'google_calendar_url': google_calendar_url,
    }
    return render(request, 'calendar_app/detail.html', context)


@login_required
def create_view(request):
    """일정 생성 - 관리자만 가능"""
    if not request.user.is_staff:
        raise PermissionDenied

    # 특정 날짜로 새 일정을 만들려는 경우
    initial_date = request.GET.get('date')

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, '일정이 등록되었습니다.')
            return redirect('calendar:detail', pk=event.pk)
    else:
        initial = {}
        if initial_date:
            initial['start_date'] = initial_date
        form = EventForm(initial=initial)

    context = {
        'form': form,
        'initial_date': initial_date,
    }
    return render(request, 'calendar_app/form.html', context)


@login_required
def edit_view(request, pk):
    """일정 수정 - 관리자만 가능"""
    event = get_object_or_404(Event, pk=pk, is_deleted=False)

    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, '일정이 수정되었습니다.')
            return redirect('calendar:detail', pk=event.pk)
    else:
        form = EventForm(instance=event)

    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'calendar_app/form.html', context)


@login_required
def delete_view(request, pk):
    """일정 삭제 - 관리자만 가능"""
    event = get_object_or_404(Event, pk=pk, is_deleted=False)

    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        event.soft_delete()
        messages.success(request, '일정이 삭제되었습니다.')
        return redirect('calendar:list')

    context = {'event': event}
    return render(request, 'calendar_app/confirm_delete.html', context)
