# vc-funding

### Server Setup

Create a virtual environment to isolate our package dependencies locally
```
$ cd vc-funding
$ python3 -m venv env
$ source env/bin/activate  (On Windows use `env\Scripts\activate`)
```

Install Django and Django REST framework into the virtual environment
```
$ pip install django
$ pip install djangorestframework
```

Run the server: 
```
$ python3 manage.py runserver
```

Create and apply the migrations: 
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

Create a superuser to access the db:
```
$ python3 manage.py createsuperuser
```

Database is available at the URL: `127.0.0.1:8000/admin`
* unless another port is used; port 8000 is used by default


### Data Ingestion
Run `ingest.py` script to ingest data from `people.csv` and `companies.csv` files into the SQL database.

```
$ python3 ingest.py
```


### API Endpoints

* `/api/avg-funding-by-person/<person_id>`
* `/api/companies-by-person/<person_id>`
* `investors-by-company/<company_linkedin_name>`


### SQL queries
Q1:
```
SELECT AVG(known_total_funding) 
FROM company 
INNER JOIN employment ON company.id = employment.company_id 
WHERE employment.person_id = '9e941331a62543f0a665c202d86d9ae5' AND company.known_total_funding IS NOT NULL
```

Q2:
```
SELECT COUNT(id)
FROM company
WHERE id NOT IN (SELECT c.id FROM company c INNER JOIN employment e ON c.id = e.company_id)
```
alternatively,
```
SELECT COUNT(company.id)
FROM company
LEFT JOIN employment ON company.id = employment.company_id
WHERE employment.id IS NULL
```

Q3:
```
SELECT name, COUNT(employment.id) popularity
FROM company
INNER JOIN employment ON company.id = employment.company_id 
GROUP_BY name
ORDER_BY popularity DESC
LIMIT 10
```

Q4:
```
SELECT c.name, c.headcount, e.person_id
FROM company c
INNER JOIN employment e ON c.id = e.company_id
WHERE e.person_id IN (SELECT person_id FROM employment WHERE lower(last_title) LIKE '%founder%')
ORDER_BY c.headcount DESC
LIMIT 3
```
