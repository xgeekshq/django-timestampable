# Django Timestamps

Timestamps and Soft Delete Patterns in Django Models.

## Add "timestamps" to your INSTALLED_APPS settings

```python
INSTALLED_APPS = [
    # ...
    'timestamps',
]
```

## Usage

a) For models you want timestamps, just inherit Timestample:

```python
from timestamps.models import models, Timestample


class YourModel(Timestample):
    # your fields here ...

```

b) For models you want soft-delete, just inherit SoftDeletes:

```python
from timestamps.models import models, SoftDeletes


class YourModel(SoftDeletes):
    # your fields here ...

```

c) If you want both, you can also inherit from Model for shorter convenience:

```python
from timestamps.models import models, Model


class YourModel(Model):
    # your fields here ...

```


### Soft Deleting

- To get all objects without the deleted ones:

```queryset = YourModel.objects```

- To get only deleted objects:

```queryset = YourModel.objects_deleted```

- To get all the objects, including deleted ones:

```queryset = YourModel.objects_with_deleted```


#### To soft delete an instance

```python
some_model = MyModel.objects.first()
some_model.delete()  # or some_model.delete(hard=False)
```

#### To restore an instance

```python
some_model = MyModel.objects_deleted.first()
some_model.restore()
```

#### To hard delete an instance

```python
some_model = MyModel.objects.first()
some_model.delete(hard=True)
```

#### To bulk soft delete a queryset

```python
qs = MyModel.objects  # you can also apply filters to bulk delete a subset: qs = MyModel.objects.filter(...)
qs.delete()  # or qs.delete(hard=False)
```

#### To bulk hard delete a queryset

```python
qs = MyModel.objects  # ... bulk hard delete a subset: qs = MyModel.objects.filter(...)
qs.delete(hard=True)
```

#### To bulk restore a queryset

```python
qs = MyModel.objects_deleted  # ... bulk restore a subset: qs = MyModel.objects_deleted.filter(...)
qs.restore()  # or qs.delete(hard=False)
```


---


### If you're using DRF
you can use the SoftDeleteModelViewSet along with DefaultRouter present in this package
and you will have access to a complete CRUD on soft deleted objects as well.
This 2 classes allows you to expose:

Consider a Dummy Model that inherits from SoftDelete.

You can have all routes for CRUD operations on this model:


| VERB | URL PATH | DESCRIPTION |
| ---- | -------- | ----------- |
| GET | /dummy/ | gets all the objects, without the deleted ones |
| POST | /dummy/ | creates a new object |
| DELETE | /dummy/[?permanent=\<true,false>] | deletes all objects (or a filtered subject). allows hard-delete. Default: soft-delete |
| GET | /dummy/\<pk\>/ | gets a non-deleted object (by primary key) |
| POST | /dummy/\<pk\>/ | updates an object (by primary key) |
| PATCH | /dummy/\<pk\>/ | partial updates an object (by primary key) |
| DELETE | /dummy/\<pk\>/[?permanent=\<true,false>] | deletes a non-deleted object (by primary key) |
| PATCH | /dummy/restore/ | restore all objects (or a filtered subject) |
| PATCH | /dummy/\<pk\>/restore/ | restores a soft-deleted object (by primary key) |
| GET | /dummy/deleted/ | gets all deleted objects |
| GET | /dummy/deleted/\<pk\>/ | gets a deleted object (by primary key) |
| GET | /dummy/with-deleted/ | get all objects, deleted included |
| GET | /dummy/with-deleted/\<pk\>/ | get an object (by primary key) |
-----------------------------------

The query parameter "permanent" it's case-insensitive and can also be: y, yes, t, on, 1, n, no, f, off and 0.


#### How to implement all of this CRUD operations by default

```python
# dummy/views.py
from timestamps.drf import viewsets 


class MyModelViewSet(SoftDeleteModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

```

````python
# dummy/urls.py
from timestamps.drf import routers
from .views import DummyModelViewSet


router = routers.DefaultRouter()
router.register(r'dummy', DummyModelViewSet)


urlpatterns = router.urls

````

#### Note
If you don't want to expose all the crud operations, be free to register as:

```python
router.register(r'dummy', DummyModelViewSet.as_view({'get': 'list_with_deleted'}))  # e.g.
```

And you can always use the mixins instead and create your APIViews:

````python
from timestamps.drf.mixins import ListDeletedModelMixin
from rest_framework import generic

class MyView(ListDeletedModelMixin, generic.GenericAPIView):
    def list_deleted(self, request, *args, **kwargs):
        # your code goes here...

````


Internally, the ListDeletedModelMixin just calls the method ListModelMixin.list(self, request, *args, **kwargs).
The method of determining if the queryset must get all objects, only the deleted or all with deleted is done using AOP,
which means that the method GenericAPIView.get_queryset() is advised at runtime to map the current action
to the correct queryset the view needs.

If you don't inherit from generic.GenericAPIView, you must be aware that, for this type of scenarios,
you need to override the method get_queryset() to return the objects that matches your needs.