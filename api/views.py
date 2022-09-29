from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.db.models import Avg

from data_ingestion.models import *

@api_view(['GET'])
def avg_funding_by_person(request, person_id):
    '''
    Returns the average total funding of all the companies that the person with the given ID has worked at.
    '''
    try:
        response_data = Employment.objects.filter(person_id=person_id).aggregate(avg_funding=Avg('company__known_total_funding'))
        return Response(response_data)
    except:
        return Response({"error": "No results found matching the person ID"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def companies_by_person(request, person_id):
    '''
    Returns a list of all the companies that the person with the given ID has worked at.
    '''
    try:
        employment_records = Employment.objects.filter(person_id=person_id)
        companies = [e.company.name for e in employment_records]
        return Response(companies)
    except:
        return Response({"error": "No results found matching the person ID"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def investors_by_company(request, company_linkedin_name):
    '''
    Returns a list of the investors for a company given any of its linkedin names.
    '''
    linkedin_accounts = CompanyLinkedinAccount.objects.filter(linkedin_name=company_linkedin_name)
    if linkedin_accounts:
        response_data = {}
        for li in linkedin_accounts:
            investors = [investor.name for investor in li.company.investors.all()]
            if investors:
                response_data[li.company.name] = investors
        return Response(response_data)
    else:
        return Response({"error": "No results found matching the linkedin name"}, status=status.HTTP_400_BAD_REQUEST)