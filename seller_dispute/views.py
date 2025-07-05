# Views have been split into the views/ package for better organization.
# See seller_dispute/views/ for all view logic.

from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .models import DisputeCase, Return, DisputeCaseUpdate
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .forms import DisputeCaseForm, DisputeCaseStatusUpdateForm
import datetime

User = get_user_model()

# HTMX-enabled page for dispute cases
class DisputeCaseListView(View):
    def get(self, request):
        # Get the parameters from the request
        sort_by = request.GET.get('sort', 'created_at')
        order = request.GET.get('order', 'desc')
        page_number = request.GET.get('page', 1)
        status_filter = request.GET.get('status', '')


        if order == 'desc':
            sort_by = f'-{sort_by}'
        dispute_cases = DisputeCase.objects.all()
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

def available_returns_api(request):
    # Only returns that do not already have a DisputeCase
    available_returns = Return.objects.filter(dispute_case__isnull=True)
    context = {'returns': available_returns}
    html = render_to_string('seller_dispute/return_event_select.html', context)
    return HttpResponse(html)

def dispute_case_create_form(request):
    if request.method == 'POST':
        form = DisputeCaseForm(request.POST)
        if form.is_valid():
            dispute_case = form.save()
            # Create a DisputeCaseUpdate entry with status 'open' (CREATED)
            DisputeCaseUpdate.objects.create(
                dispute_case=dispute_case,
                status='open',
                comment='Case created.'
            )
            # After creation, close modal and refresh list (could return a partial or redirect)
            return HttpResponse('<script>window.location.reload();</script>')
    else:
        form = DisputeCaseForm()
    return render(request, 'seller_dispute/dispute_case_form_modal.html', {'form': form})

def dispute_case_timeline_api(request, pk):
    dispute_case = get_object_or_404(DisputeCase, pk=pk)
    updates = dispute_case.updates.order_by('updated_at')
    context = {
        'dispute_case': dispute_case,
        'updates': updates,
    }
    return render(request, 'seller_dispute/dispute_case_timeline.html', context)

def order_details_api(request, pk):
    dispute_case = get_object_or_404(DisputeCase, pk=pk)
    order = dispute_case.return_event.order
    context = {'order': order}
    return render(request, 'seller_dispute/order_details.html', context)

def return_details_api(request, pk):
    dispute_case = get_object_or_404(DisputeCase, pk=pk)
    return_event = dispute_case.return_event
    context = {'return_event': return_event}
    return render(request, 'seller_dispute/return_details.html', context)

def dispute_case_detail_modal(request, pk):
    dispute_case = get_object_or_404(DisputeCase, pk=pk)
    context = {
        'dispute_case': dispute_case,
    }
    return render(request, 'seller_dispute/dispute_case_detail_modal.html', context)

def dispute_case_edit_modal(request, pk):
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

def dispute_case_table_partial(request):
    sort_by = request.GET.get('sort', 'created_at')
    order = request.GET.get('order', 'desc')
    page_number = request.GET.get('page', 1)
    page_size = int(request.GET.get('page_size', 10))
    status_filter = request.GET.get('status', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    date_error = ''
    today = datetime.date.today()
    # Validate dates
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
    dispute_cases = DisputeCase.objects.all()
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