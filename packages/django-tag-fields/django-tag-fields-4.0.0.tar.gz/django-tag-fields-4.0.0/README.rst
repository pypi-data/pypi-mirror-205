django-tag-fields
=================

.. image:: https://img.shields.io/pypi/pyversions/django-tag_fields.svg
   :target: https://pypi.org/project/django-tag-fields/
   :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/djversions/django-taggit.svg
   :target: https://pypi.org/project/django-taggit/
   :alt: Supported Django versions

.. image:: https://github.com/imAsparky/django-tag-fields/workflows/Test/badge.svg
   :target: https://github.com/imAsparky/django-tag-fields/actions
   :alt: GitHub Actions

.. image:: https://codecov.io/gh/imAsparky/django-tag-fields/branch/main/graph/badge.svg?token=6TPEAAOUUF
   :target: https://codecov.io/gh/imAsparky/django-tag-fields

This is a clone of `Jazzband django-taggit <https://github.com/jazzband/django-taggit>`_ project.
By contributing you agree to abide by the `Contributor Code of Conduct
<https://github.com/imAsparky/django-tag-fields/blob/main/CODE_OF_CONDUCT.md>`_.


.. note::

   This project was cloned from ``django-taggit v3.1.0`` and will continue to work in the same
   way as that version.

   Over time I endeavor to extend django-taggit with individual field tagging.


``django-tag-fields`` a simpler approach to tagging with Django.  Add ``"tag_fields"`` to your
``INSTALLED_APPS`` then just add a TaggableManager to your model and go:

.. code:: python

    from django.db import models

    from tag_fields.managers import TaggableManager


    class Food(models.Model):
        # ... fields here

        tags = TaggableManager()


Then you can use the API like so:

.. code:: pycon

    >>> apple = Food.objects.create(name="apple")
    >>> apple.tags.add("red", "green", "delicious")
    >>> apple.tags.all()
    [<Tag: red>, <Tag: green>, <Tag: delicious>]
    >>> apple.tags.remove("green")
    >>> apple.tags.all()
    [<Tag: red>, <Tag: delicious>]
    >>> Food.objects.filter(tags__name__in=["red"])
    [<Food: apple>, <Food: cherry>]

Tags will show up for you automatically in forms and the admin.

``django-tag-fields`` requires Django 3.2 or greater.

For more info check out the `documentation
<https://django-tag-fields.readthedocs.io/>`_.

For questions about usage or development you can create an issue on Github (if your question is about
usage please add the `question` label).
