# coding:utf-8
from django.urls import path
from rest_framework_bulk.routes import BulkRouter

from . import api

app_name = 'accounts'

router = BulkRouter()

router.register(r'accounts', api.AccountViewSet, 'account')
router.register(r'account-secrets', api.AccountSecretsViewSet, 'account-secret')
router.register(r'account-templates', api.AccountTemplateViewSet, 'account-template')
router.register(r'account-template-secrets', api.AccountTemplateSecretsViewSet, 'account-template-secret')
router.register(r'account-backup-plans', api.AccountBackupPlanViewSet, 'account-backup')
router.register(r'account-backup-plan-executions', api.AccountBackupPlanExecutionViewSet, 'account-backup-execution')
router.register(r'change-secret-automations', api.ChangeSecretAutomationViewSet, 'change-secret-automation')
router.register(r'change-secret-executions', api.ChangSecretExecutionViewSet, 'change-secret-execution')
router.register(r'change-secret-records', api.ChangeSecretRecordViewSet, 'change-secret-record')
router.register(r'gather-account-automations', api.GatherAccountsAutomationViewSet, 'gather-account-automation')
router.register(r'gather-account-executions', api.GatherAccountsExecutionViewSet, 'gather-account-execution')
router.register(r'push-account-automations', api.PushAccountAutomationViewSet, 'push-account-automation')

urlpatterns = [
    path('accounts/tasks/', api.AccountTaskCreateAPI.as_view(), name='account-task-create'),
    path('account-secrets/<uuid:pk>/histories/', api.AccountHistoriesSecretAPI.as_view(),
         name='account-secret-history'),
    path('change-secret/<uuid:pk>/asset/remove/', api.ChangSecretRemoveAssetApi.as_view(), name='change-secret-remove-asset'),
    path('change-secret/<uuid:pk>/asset/add/', api.ChangSecretAddAssetApi.as_view(), name='change-secret-add-asset'),
    path('change-secret/<uuid:pk>/nodes/', api.ChangSecretNodeAddRemoveApi.as_view(), name='change-secret-add-or-remove-node'),
    path('change-secret/<uuid:pk>/assets/', api.ChangSecretAssetsListApi.as_view(), name='change-secret-assets'),
]

urlpatterns += router.urls
