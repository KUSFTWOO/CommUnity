from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from .models import Poll, PollOption, Vote
from .forms import PollForm


def list_view(request):
    """투표 목록 - 진행중/완료된 투표 구분"""
    all_polls = Poll.objects.prefetch_related('options').all()

    active_polls = [p for p in all_polls if not p.is_expired]
    closed_polls = [p for p in all_polls if p.is_expired]

    context = {
        'active_polls': active_polls,
        'closed_polls': closed_polls,
        'user_votes': {}
    }

    if request.user.is_authenticated:
        user_votes = Vote.objects.filter(user=request.user).values('poll_id', 'option_id')
        context['user_votes'] = {vote['poll_id']: vote['option_id'] for vote in user_votes}

    return render(request, 'votes/list.html', context)


def detail_view(request, pk):
    """투표 상세 - 투표 참여 및 결과 표시"""
    poll = get_object_or_404(Poll.objects.prefetch_related('options'), pk=pk)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        vote_exists = Vote.objects.filter(poll=poll, user=request.user).exists()
        if vote_exists:
            return redirect('votes:detail', pk=poll.pk)

        option_id = request.POST.get('option_id')
        try:
            option = PollOption.objects.get(id=option_id, poll=poll)
        except PollOption.DoesNotExist:
            return redirect('votes:detail', pk=poll.pk)

        Vote.objects.create(
            poll=poll,
            option=option,
            user=request.user
        )
        option.votes_count += 1
        option.save(update_fields=['votes_count'])

        return redirect('votes:detail', pk=poll.pk)

    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(poll=poll, user=request.user)
        except Vote.DoesNotExist:
            pass

    context = {
        'poll': poll,
        'user_vote': user_vote,
        'is_expired': poll.is_expired,
        'total_votes': poll.total_votes,
    }

    return render(request, 'votes/detail.html', context)


@login_required
def create_view(request):
    """투표 생성 - 관리자만"""
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.created_by = request.user
            poll.save()

            options_text = form.cleaned_data.get('options', '')
            options_list = [opt.strip() for opt in options_text.split('\n') if opt.strip()]

            for option_text in options_list:
                PollOption.objects.create(
                    poll=poll,
                    text=option_text,
                    votes_count=0
                )

            return redirect('votes:detail', pk=poll.pk)
    else:
        form = PollForm()

    context = {'form': form}
    return render(request, 'votes/form.html', context)


@login_required
def edit_view(request, pk):
    """투표 수정 - 관리자만"""
    if not request.user.is_staff:
        raise PermissionDenied

    poll = get_object_or_404(Poll, pk=pk)

    if request.method == 'POST':
        form = PollForm(request.POST, instance=poll)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.save()

            PollOption.objects.filter(poll=poll).delete()

            options_text = form.cleaned_data.get('options', '')
            options_list = [opt.strip() for opt in options_text.split('\n') if opt.strip()]

            for option_text in options_list:
                PollOption.objects.create(
                    poll=poll,
                    text=option_text,
                    votes_count=0
                )

            return redirect('votes:detail', pk=poll.pk)
    else:
        options_text = '\n'.join([opt.text for opt in poll.options.all()])
        form = PollForm(instance=poll)
        form.fields['options'].initial = options_text

    context = {'form': form, 'poll': poll}
    return render(request, 'votes/form.html', context)


@login_required
def delete_view(request, pk):
    """투표 삭제 - 관리자만"""
    if not request.user.is_staff:
        raise PermissionDenied

    poll = get_object_or_404(Poll, pk=pk)

    if request.method == 'POST':
        poll.delete()
        return redirect('votes:list')

    context = {'poll': poll}
    return render(request, 'votes/confirm_delete.html', context)
