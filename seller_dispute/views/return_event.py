from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from ..models import Return, DisputeCase
from django.db import models

def available_returns_api(request):
    # Only returns that do not already have a non-deleted DisputeCase
    available_returns = Return.objects.filter(
        (models.Q(dispute_case__isnull=True) |
         models.Q(dispute_case__deleted_at__isnull=False))
    )
    context = {'returns': available_returns}
    html = render_to_string('seller_dispute/return_event_select.html', context)
    return HttpResponse(html)

def return_details_api(request, pk):
    dispute_case = get_object_or_404(DisputeCase, pk=pk)
    return_event = dispute_case.return_event
    context = {'return_event': return_event}
    return render(request, 'seller_dispute/return_details.html', context) 