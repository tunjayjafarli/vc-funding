from django.urls import path

from . import views

urlpatterns = [
    path('avg-funding-by-person/<person_id>', views.avg_funding_by_person),

    path('companies-by-person/<person_id>', views.companies_by_person),

    path('investors-by-company/<company_linkedin_name>', views.investors_by_company)
]