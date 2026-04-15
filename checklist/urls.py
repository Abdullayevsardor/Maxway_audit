from django.urls import path
from . import views
from .views import (
    CategoryListView,
    BranchListCreateView,
    ScoreCreateUpdateView,
    audit_details_page,
    custom_logout,
    worker_login,
    audit_form,
)

urlpatterns = [
    # ===== WORKER =====
    path('auditt/', views.audit_form_view, name='home'),
    path('audit/', views.audit_form_view, name='audit_form'),
    path('input/', views.audit_input_view, name='audit_input'),
    path('success/', views.audit_success_view, name='audit_success'),

    # ===== RESULTS / PAGES =====
    # path('results/', views.audit_results_view, name='audit_results'),
    path('page/', audit_details_page, name='audit_page'),
    path(
        'pages/filial/<str:filial_nomi>/',
        views.audit_filial_detail,
        name='audit_filial_detail'
    ),

    # ===== API =====
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('branches/', BranchListCreateView.as_view(), name='branches'),
    path('score/', ScoreCreateUpdateView.as_view(), name='score'),

    # ===== EXPORT (ALL AUDITS) =====
    path('export/excel/', views.export_excel, name='audit_export_excel'),
    path('export/pdf/', views.export_pdf, name='audit_export_pdf'),

    # ===== EXPORT (SINGLE AUDIT) =====
    path(
        'audit/<int:audit_id>/export_excel/',
        views.export_audit_detail_excel,
        name='export_audit_detail_excel'
    ),
    path(
        'audit/<int:audit_id>/export_pdf/',
        views.export_audit_detail_pdf,
        name='export_audit_detail_pdf'
    ),

    # ===== DELETE =====
    path(
        'audit/delete/<int:id>/',
        views.audit_delete,
        name='audit_delete'
    ),
    # ===== LOGOUT =====
    path('logout/', custom_logout, name='logout'),
    path('setup-admin-777/', views.create_admin_once),
    
    #==== AUTHENTICATION =====
    path('', worker_login, name='login'),

    #=====  lowescore =====
    path("audits/low-scores/", views.low_scores_view, name="low_scores"),


]



