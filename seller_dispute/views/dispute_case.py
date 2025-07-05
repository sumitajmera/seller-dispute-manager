from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views import View
from django.http import HttpResponse
from django.template.loader import render_to_string
from ..forms import DisputeCaseForm, DisputeCaseStatusUpdateForm
from ..models import DisputeCase, DisputeCaseUpdate, Return
import datetime
from django.utils import timezone

class DisputeCaseViewSet(viewsets.ModelViewSet):
    queryset = DisputeCase.objects.all()
    serializer_class = None  # Set in urls.py or serializers.py

    @action(detail=False, methods=['get'], url_path='list-page')
    def list_page(self, request):
        sort_by = request.GET.get('sort', 'created_at')
        order = request.GET.get('order', 'desc')
        page_number = request.GET.get('page', 1)
        status_filter = request.GET.get('status', '')
        if order == 'desc':
            sort_by = f'-{sort_by}'
        dispute_cases = DisputeCase.objects.filter(deleted_at__isnull=True)
        if status_filter:
            dispute_cases = dispute_cases.filter(status=status_filter)
        dispute_cases = dispute_cases.order_by(sort_by)
        paginator = Paginator(dispute_cases, 10)
        page_obj = paginator.get_page(page_number)
        page_size_options = [5, 10, 20, 50, 100]
        status_choices = DisputeCase.STATUS_CHOICES
        context = {
            'page_obj': page_obj,
            'sort': request.GET.get('sort', 'created_at'),
            'order': order,
            'page_size_options': page_size_options,
            'status_choices': status_choices,
            'status_filter': status_filter,
        }
        return render(request, 'seller_dispute/dispute_case_list.html', context)

    @action(detail=False, methods=['get'], url_path='table-partial')
    def table_partial(self, request):
        sort_by = request.GET.get('sort', 'created_at')
        order = request.GET.get('order', 'desc')
        page_number = request.GET.get('page', 1)
        page_size = int(request.GET.get('page_size', 10))
        status_filter = request.GET.get('status', '')
        from_date = request.GET.get('from_date', '')
        to_date = request.GET.get('to_date', '')
        date_error = ''
        today = datetime.date.today()
        if from_date:
            try:
                from_date_obj = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
                if from_date_obj > today:
                    date_error = 'From date cannot be in the future.'
            except ValueError:
                date_error = 'Invalid from date.'
        if to_date and from_date and not date_error:
            try:
                to_date_obj = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
                from_date_obj = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
                if to_date_obj < from_date_obj:
                    date_error = 'To date cannot be before From date.'
            except ValueError:
                date_error = 'Invalid to date.'
        if order == 'desc':
            sort_by = f'-{sort_by}'
        dispute_cases = DisputeCase.objects.filter(deleted_at__isnull=True)
        if not date_error:
            if status_filter:
                dispute_cases = dispute_cases.filter(status=status_filter)
            if from_date:
                dispute_cases = dispute_cases.filter(created_at__date__gte=from_date)
            if to_date:
                dispute_cases = dispute_cases.filter(created_at__date__lte=to_date)
        dispute_cases = dispute_cases.order_by(sort_by)
        paginator = Paginator(dispute_cases, page_size)
        page_obj = paginator.get_page(page_number)
        page_size_options = [5, 10, 20, 50, 100]
        status_choices = DisputeCase.STATUS_CHOICES
        context = {
            'page_obj': page_obj,
            'sort': request.GET.get('sort', 'created_at'),
            'order': order,
            'page_size': page_size,
            'page_size_options': page_size_options,
            'status_choices': status_choices,
            'status_filter': status_filter,
            'from_date': from_date,
            'to_date': to_date,
            'date_error': date_error,
        }
        return render(request, 'seller_dispute/dispute_case_table_partial.html', context)

    @action(detail=False, methods=['get', 'post'], url_path='create-form')
    def create_form(self, request):
        if request.method == 'POST':
            form = DisputeCaseForm(request.POST)
            if form.is_valid():
                dispute_case = form.save()
                DisputeCaseUpdate.objects.create(
                    dispute_case=dispute_case,
                    status='open',
                    comment='Case created.'
                )
                return HttpResponse('<script>window.location.reload();</script>')
        else:
            form = DisputeCaseForm()
        return render(request, 'seller_dispute/dispute_case_form_modal.html', {'form': form})

    @action(detail=True, methods=['get'], url_path='timeline')
    def timeline(self, request, pk=None):
        dispute_case = get_object_or_404(DisputeCase, pk=pk)
        updates = dispute_case.updates.order_by('updated_at')
        context = {
            'dispute_case': dispute_case,
            'updates': updates,
        }
        return render(request, 'seller_dispute/dispute_case_timeline.html', context)

    @action(detail=True, methods=['get'], url_path='detail-modal')
    def detail_modal(self, request, pk=None):
        dispute_case = get_object_or_404(DisputeCase, pk=pk)
        context = {
            'dispute_case': dispute_case,
        }
        return render(request, 'seller_dispute/dispute_case_detail_modal.html', context)

    @action(detail=True, methods=['get', 'post'], url_path='edit-modal')
    def edit_modal(self, request, pk=None):
        dispute_case = get_object_or_404(DisputeCase, pk=pk)
        if request.method == 'POST':
            form = DisputeCaseStatusUpdateForm(request.POST)
            if form.is_valid():
                status = form.cleaned_data['status']
                comment = form.cleaned_data['comment']
                dispute_case.status = status
                dispute_case.save()
                DisputeCaseUpdate.objects.create(
                    dispute_case=dispute_case,
                    status=status,
                    comment=comment or f"Status set to {status.title()}"
                )
                return HttpResponse('<script>window.location.reload();</script>')
        else:
            form = DisputeCaseStatusUpdateForm(initial={'status': dispute_case.status})
        context = {'dispute_case': dispute_case, 'form': form}
        return render(request, 'seller_dispute/dispute_case_edit_modal.html', context)

    @action(detail=True, methods=['get'], url_path='confirm-delete-modal')
    def confirm_delete_modal(self, request, pk=None):
        dispute_case = get_object_or_404(DisputeCase, pk=pk)
        context = {'dispute_case': dispute_case}
        return render(request, 'seller_dispute/dispute_case_confirm_delete_modal.html', context)

    def destroy(self, request, pk=None):
        dispute_case = get_object_or_404(DisputeCase, pk=pk)
        if dispute_case.deleted_at is None:
            dispute_case.deleted_at = timezone.now()
            dispute_case.save()
            return Response({'status': 'deleted'}, status=204)
        return Response({'error': 'Already deleted'}, status=400) 