# Districts - Africa

Districts - Africa is a Django app for managing regions, districts, counties, sub-counties, parishes, and their corresponding locations within the African continent.

Detailed documentation is in the "docs" directory.

## Quick start

1. Install the Districts package using `pip` by running the following command:

2. Add "districts" to your `INSTALLED_APPS` setting like this:

INSTALLED_APPS = [
...,
"districts",
]

3. Include the districts URLconf in your project urls.py like this:

path("districts/", include("districts.urls")),

4. Run `python manage.py migrate` to create the districts models.

5. Run `python manage.py load_districts_data` to load the Districts data to your model.

6. Start the development server and visit `http://127.0.0.1:8000/districts/` to view the districts and the URLs.

7. For instance, visit `http://127.0.0.1:8000/districts/region/` to access the regions within a country.
