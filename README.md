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
* `/api/investors-by-company/<company_linkedin_name>`


### SQL queries
Q1:
```
SELECT AVG(company.known_total_funding) 
FROM company 
INNER JOIN employment ON company.id = employment.company_id 
WHERE employment.person_id = "92a528778d5d41a6950f1b9c6574be7a" AND company.known_total_funding IS NOT NULL
```
Output: `[(108000000.0,)]`

Q2:
```
SELECT COUNT(c.id)
FROM company c
WHERE c.id NOT IN (SELECT c.id FROM company c INNER JOIN employment e ON c.id = e.company_id)
```
alternatively,
```
SELECT COUNT(company.id)
FROM company
LEFT JOIN employment ON company.id = employment.company_id
WHERE employment.id IS NULL
```
Output: `[(9421,)]`


Q3:
```
SELECT company.name
FROM company
INNER JOIN employment ON company.id = employment.company_id 
GROUP BY company.name
ORDER BY COUNT(employment.id) DESC
LIMIT 10
```
Output:
```
[('Microsoft',), ('Amazon',), ('Intel Corporation',), ('Google',), ('Apple',), ('Hewlett Packard Enterprise',), ('Facebook',), ('Texas Instruments',), ('Hewlett-Packard',), ('Meta',)]
```

Q4:
```
SELECT c.name, c.headcount, e.person_id
FROM company c
INNER JOIN employment e ON c.id = e.company_id
WHERE c.id IN (SELECT e.company_id FROM employment e WHERE lower(e.last_title) LIKE '%founder%')
ORDER BY c.headcount DESC
LIMIT 3
```
Output:
```
[('Dafiti', 2907, 'bb0d848943604a94bd3dc079f75afc96'), ('eBay for Business', 1336, 'a292842c475e4b4f9671fb09536c472e'), ('UWorld', 439, 'c6f69f63c7d5419faf34d0cccf544e18')]
```

Q5:
Average duration in years of employment
```
SELECT ROUND(AVG(duration), 2) 
FROM (
    SELECT e.person_id, (JULIANDAY(e.group_end_date) - JULIANDAY(e.group_start_date)) / 365) as duration 
    FROM  employment e 
    WHERE e.person_id IN (
        SELECT e.person_id
        FROM employment e
        GROUP BY e.person_id
        HAVING COUNT(e.id) > 1
    )
)
```
Output: `[(2.51,)]`

Number of employees who had more than one job
```
SELECT COUNT(*) 
FROM (
    SELECT e.person_id
    FROM employment e 
    GROUP BY e.person_id 
    HAVING COUNT(e.id) > 1
)
```
Output: `[(904,)]`

