from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.dispute_case import DisputeCaseViewSet
from .views.return_event import available_returns_api, return_details_api
from .views.order import order_details_api

router = DefaultRouter()
router.register(r'dispute-cases', DisputeCaseViewSet, basename='dispute-cases')

urlpatterns = [
    path('', DisputeCaseViewSet.as_view({'get': 'list_page'}), name='dispute_case_list'),
    # DisputeCaseViewSet custom actions (HTMX, modals, etc)
    path('dispute-case-list/', DisputeCaseViewSet.as_view({'get': 'list_page'}), name='dispute_case_list_page'),
    path('dispute-case-table-partial/', DisputeCaseViewSet.as_view({'get': 'table_partial'}), name='dispute_case_table_partial'),
    path('dispute-case-create-form/', DisputeCaseViewSet.as_view({'get': 'create_form', 'post': 'create_form'}), name='dispute_case_create_form'),
    path('dispute-case-detail/<int:pk>/', DisputeCaseViewSet.as_view({'get': 'detail_modal'}), name='dispute_case_detail_modal'),
    path('dispute-case-timeline/<int:pk>/', DisputeCaseViewSet.as_view({'get': 'timeline'}), name='dispute_case_timeline_api'),
    path('dispute-case-edit/<int:pk>/', DisputeCaseViewSet.as_view({'get': 'edit_modal', 'post': 'edit_modal'}), name='dispute_case_edit_modal'),
    path('dispute-case-confirm-delete/<int:pk>/', DisputeCaseViewSet.as_view({'get': 'confirm_delete_modal'}), name='dispute_case_confirm_delete_modal'),

    # Return and Order related
    path('api/available-returns/', available_returns_api, name='available_returns_api'),
    path('order-details/<int:pk>/', order_details_api, name='order_details_api'),
    path('return-details/<int:pk>/', return_details_api, name='return_details_api'),
]
urlpatterns += router.urls
