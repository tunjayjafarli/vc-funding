import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

import csv
import json
from datetime import datetime
from data_ingestion.models import *

# # # Ingest the companies.csv file
with open('source_files/companies.csv', mode='r') as csv_file:
    
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        
        # Parse and create company object in the db
        name = row['NAME']
        founding_date = datetime.strptime(row['FOUNDING_DATE'], '%Y-%m-%d').date() if row['FOUNDING_DATE'] else None
        company_data = {
            'description': row['DESCRIPTION'],
            'headcount': int(row['HEADCOUNT']) if row['HEADCOUNT'] else None,
            'most_recent_raise': int(row['MOST_RECENT_RAISE']) if row['MOST_RECENT_RAISE'] else None,
            'most_recent_valuation': int(row['MOST_RECENT_VALUATION']) if row['MOST_RECENT_VALUATION'] else None,
            'known_total_funding': int(row['KNOWN_TOTAL_FUNDING']) if row['KNOWN_TOTAL_FUNDING'] else None,
        }
        company_obj, created = Company.objects.update_or_create(name=name, founding_date=founding_date, defaults=company_data)
        
        if created:
            print("Created company:", company_obj.name)
        else:
            print("Updated company:", company_obj.name)

        # Parse and create linkedin names in the db
        if row["COMPANY_LINKEDIN_NAMES"]:
            for linkedin_name in json.loads(row["COMPANY_LINKEDIN_NAMES"]):
                CompanyLinkedinAccount.objects.update_or_create(linkedin_name=linkedin_name, company=company_obj)
        
        # Parse and create investors in the db
        if row['INVESTORS']:
            for investor in json.loads(row['INVESTORS']):
                investor_obj = Investor.objects.get_or_create(name=investor)[0]
                company_obj.investors.add(investor_obj)

# Ingest the peoples.csv file
with open('source_files/people.csv', mode='r') as csv_file:
    
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:

        company_name = row['COMPANY_NAME']
        linkedin_name = row['COMPANY_LI_NAME']

        try:
            company_obj = Company.objects.get_or_create(name=company_name)[0]
        except Company.MultipleObjectsReturned:
            company_obj = Company.objects.filter(name=company_name)[0]

        linkedin_account_obj = None
        
        if linkedin_name and linkedin_name != "n/a":
            linkedin_accounts = CompanyLinkedinAccount.objects.filter(linkedin_name=linkedin_name, company__name=company_name)
            if len(linkedin_accounts) > 0:
                linkedin_account_obj = linkedin_accounts[0]
            else:
                linkedin_account_obj = CompanyLinkedinAccount.objects.create(linkedin_name=linkedin_name, company=company_obj)

        # Parse and create employment object in the db
        employment_data = {
            'person_id': row['PERSON_ID'],
            'company': linkedin_account_obj.company if linkedin_account_obj else company_obj,
            'last_title': row['LAST_TITLE'],
            'group_start_date': datetime.strptime(row['GROUP_START_DATE'], '%Y-%m-%d').date() if row['GROUP_START_DATE'] else None,
            'group_end_date': datetime.strptime(row['GROUP_END_DATE'], '%Y-%m-%d').date() if row['GROUP_END_DATE'] else None
        }

        employment_obj, created = Employment.objects.update_or_create(**employment_data)

        if created:
            print("Employment record created:", employment_obj.person_id, employment_obj.last_title, employment_obj.company)
        else:
            print("Employment record updated:", employment_obj.person_id, employment_obj.last_title, employment_obj.company)
