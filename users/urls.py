from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('users', views.UserView, basename='users')
router.register('expense-claim', views.ExpenseClaimView, basename='expenseclaim')
router.register('expense-category', views.ExpenseCategoryView, basename='expensecategory')
router.register('all-claim-request', views.ClaimRequestView, basename='claimrequest')

urlpatterns = router.urls