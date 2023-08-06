=========
DRF-CMS
=========

DRF-CMS is a Django app to manage non-relational websites content in a restful way.
Elements are key-value and linked to a page, letting the client decide how to compose them.


Quick start
-----------

1. Add "cms" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'drf_cms',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('cms/', include('drf_cms.urls')),

3. Run ``python manage.py migrate`` to create the cms models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create cms pages and content (you'll need the Admin app enabled).
