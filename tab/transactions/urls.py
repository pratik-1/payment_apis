"""
URLs for the transactions app.
"""


from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("transactions", views.TransactionView)
router.register("accounts", views.AccountsView)

app_name = "transactions"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<uuid:account_id>/balance",
        views.TransactionSummayView.as_view(),
        name="transaction-summary",
    ),
    # path('<int:pk>', views.DetailView.as_view(), name='detail'),
]
