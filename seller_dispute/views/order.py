from django.shortcuts import get_object_or_404, render
from ..models import DisputeCase

def order_details_api(request, pk):
    dispute_case = get_object_or_404(DisputeCase, pk=pk)
    order = dispute_case.return_event.order
    context = {'order': order}
    return render(request, 'seller_dispute/order_details.html', context) 