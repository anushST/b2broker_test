from django.urls import include, path
from rest_framework import routers

from .views import TransactionViewSet, WalletViewSet

router = routers.DefaultRouter()
router.register('wallets', WalletViewSet)

transaction_list = TransactionViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
transaction_detail = TransactionViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path(
        'wallets/<int:wallet_id>/transactions/',
        transaction_list,
        name='transactions',
    ),
    path(
        'wallets/<int:wallet_id>/transactions/<int:pk>/',
        transaction_detail,
        name='transaction-detail',
    ),
    path('', include(router.urls)),
]
