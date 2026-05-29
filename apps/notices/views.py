from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Notice
from .forms import NoticeForm


def list_view(request):
    """공지사항 목록 - 누구나 조회 가능"""
    notices = Notice.objects.filter(is_deleted=False)

    # 페이지네이션 (10개씩)
    paginator = Paginator(notices, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'notices': page_obj.object_list,
    }
    return render(request, 'notices/list.html', context)


def detail_view(request, pk):
    """공지사항 상세 - 누구나 조회 가능"""
    notice = get_object_or_404(Notice, pk=pk, is_deleted=False)
    context = {'notice': notice}
    return render(request, 'notices/detail.html', context)


@login_required
def create_view(request):
    """공지사항 작성 - 관리자만 가능"""
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.save()
            messages.success(request, '공지사항이 등록되었습니다.')
            return redirect('notices:detail', pk=notice.pk)
    else:
        form = NoticeForm()

    context = {'form': form}
    return render(request, 'notices/form.html', context)


@login_required
def edit_view(request, pk):
    """공지사항 수정 - 관리자만 가능"""
    notice = get_object_or_404(Notice, pk=pk, is_deleted=False)

    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            notice = form.save()
            messages.success(request, '공지사항이 수정되었습니다.')
            return redirect('notices:detail', pk=notice.pk)
    else:
        form = NoticeForm(instance=notice)

    context = {'form': form, 'notice': notice}
    return render(request, 'notices/form.html', context)


@login_required
def delete_view(request, pk):
    """공지사항 삭제 - 관리자만 가능"""
    notice = get_object_or_404(Notice, pk=pk, is_deleted=False)

    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        notice.soft_delete()
        messages.success(request, '공지사항이 삭제되었습니다.')
        return redirect('notices:list')

    context = {'notice': notice}
    return render(request, 'notices/confirm_delete.html', context)
