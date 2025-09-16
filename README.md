# Django Timestamps

Timestamps and Soft Delete Patterns in Django Models.

## ✅ Summary

- Add timestamps and soft delete to any model with a single line of code.
- Manage deleted objects effortlessly with built-in managers and custom querysets.
- Seamlessly integrate into existing models without breaking changes or refactoring your app/project
  - ⭐ no need to modify the default objects manager or queryset ⭐
- Hook into lifecycle events with signals.
- Get full CRUD support in DRF, including restore endpoints.
- Configure safety features such as bulk hard delete and bulk responses.

## 🚀 Installation

### Without DRF

````bash
$ pip install django-timestampable
````

### With DRF support

To install django-timestampable with [Django Rest Framework](https://www.django-rest-framework.org/) included:

````bash
$ pip install "django-timestampable[drf]"
````

*You can use the first option if you have Django Rest Framework already installed.*

&nbsp;

## ⚙️ Configuration

Add `timestamps` to your `INSTALLED_APPS` in your Django settings:

```python
INSTALLED_APPS = [
    # ...
    'timestamps',
]
```

### Or, if you installed with [Django Rest Framework](https://www.django-rest-framework.org/):

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'timestamps',
]
```

## 🛠 Usage

a) For Timestamps

```python
from timestamps.models import models, Timestampable

class YourModel(Timestampable):
    # your fields here ...

```

b) For Soft Deletes

```python
from timestamps.models import models, SoftDeletes

class YourModel(SoftDeletes):
    # your fields here ...

```

c) Combine both Timestamps and Soft Deletes

```python
# to this:
from timestamps.models import models, Model  # shortcut including both

class YourModel(Model):
    # your fields here ...

```

**Note**: Always import Model from timestamps.models explicitly. models.Model from Django is untouched.

## 🧹 Soft Deleting

### Query managers

When you use SoftDeletes or Model, you have 3 query managers available:

- Active objects only (without soft deleted objects):

```queryset = YourModel.objects```

- Deleted objects only:

```queryset = YourModel.objects_deleted```

- All objects (active + deleted):

```queryset = YourModel.objects_with_deleted```

### Operations

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

## 📡 Signals

Four signals are available:

- pre_soft_delete
- post_soft_delete
- pre_restore
- post_restore

To use them, just import the signals and register listeners for them. Eg:

### Pre Soft Delete

```python3
from timestamps.signals import pre_soft_delete
from django.dispatch import receiver

@receiver(pre_soft_delete)
def on_pre_soft_delete(sender, instance, **kwargs):
    print(f"Model {sender} with id {instance.pk} will be deleted!")
```

### Post Soft Delete

```python3
from timestamps.signals import post_soft_delete
from django.dispatch import receiver

@receiver(post_soft_delete)
def on_post_soft_delete(sender, instance, **kwargs):
    print(f"Model {sender} with id {instance.pk} was deleted at {instance.deleted_at}!")
```

### Pre Restore

```python3
from timestamps.signals import pre_restore
from django.dispatch import receiver

@receiver(pre_restore)
def on_pre_restore(sender, instance, **kwargs):
    print(f"Model {sender} with id {instance.pk} deleted at {instance.deleted_at} will be restored!")
```

### Post Restore

```python3
from timestamps.signals import post_restore
from django.dispatch import receiver

@receiver(post_restore)
def on_post_restore(sender, instance, **kwargs):
    print(f"Model {sender} with id {instance.pk} restored!")
```

## 🌐 Using with DRF

You can use the SoftDeleteModelViewSet along with DefaultRouter present in this package
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

&nbsp;

The query parameter "permanent" it's case-sensitive and can also be one of the values:

```python
truthful_options = [
    't', 'T',
    'y', 'Y', 'yes', 'Yes', 'YES',
    'true', 'True', 'TRUE',
    'on', 'On', 'ON',
    '1', 1,
    True
]
```

```python
falsely_options = [
    'f', 'F',
    'n', 'N', 'no', 'No', 'NO',
    'false', 'False', 'FALSE',
    'off', 'Off', 'OFF',
    '0', 0,
    'null',
    False
]
```

### How to expose all CRUD operations

```python
# dummy/views.py
from timestamps.drf import viewsets  # instead of: from rest_framework import viewsets
from .models import Dummy
from .serializers import DummySerializer


class DummyModelViewSet(viewsets.ModelViewSet):
    queryset = Dummy.objects.all()
    serializer_class = DummySerializer

```

````python
# dummy/urls.py
from timestamps.drf import routers  # instead of: from rest_framework import routers
from .views import DummyModelViewSet


router = routers.DefaultRouter()
router.register(r'dummy', DummyModelViewSet)


urlpatterns = router.urls

````

## ⚠️ Notes & Settings

### Note A - About Bulk Hard Delete

For security reasons, by default, if you pass to the query parameter "?permanent=true" on a bulk destroy, 
the view will not let you hard-delete, raising a PermissionDenied.
If you want to enable it on your project, just add to the project settings:

```python
TIMESTAMPS__BULK_HARD_DELETE = True
```

It's here to prevent users of "forgetting" that the routes also expose bulk hard-delete by default.
In production, you can set this flag to True and manage hard-deleting using DRF permissions.

*Hard-deleting one object at time is allowed by default.*

&nbsp;

### Note B - About Bulk Response

Bulk actions of restoring and deleting returns no content (status code 204) by default.
If you want to return a response with the number of deleted/restored objects, just add this setting:

```python
TIMESTAMPS__BULK_RESPONSE_CONTENT = True
```

Example of returned response: ```{"count": 3 }```

&nbsp;

### Note C - Selective Routes

If you don't want to expose all the crud operations, be free to register as:

```python
router.register(r'dummy', DummyModelViewSet.as_view({'get': 'list_with_deleted'}))  # e.g.
```

Or use DRF mixins instead:

````python
from rest_framework import generic
from timestamps.drf.mixins import ListDeletedModelMixin
from .models import Dummy
from .serializers import DummySerializer

class MyView(ListDeletedModelMixin, generic.GenericAPIView):
    queryset = Dummy.objects.all()
    serializer_class = DummySerializer
    
    def list_deleted(self, request, *args, **kwargs):
        # optional. your code goes here...

````

Internally, the ListDeletedModelMixin just calls the method ListModelMixin.list(self, request, *args, **kwargs).
The method of determining if the queryset must get all objects, only the deleted or all with deleted is done using AOP,
which means that the method GenericAPIView.get_queryset() is advised at runtime to map the current action
to the correct queryset the view needs.

If you don't inherit from generic.GenericAPIView, you must be aware that, for this type of scenarios,
you need to override the method get_queryset() to return the objects that matches your needs.

&nbsp;

---

&nbsp;

Thanks for using `django-timestampable`! 🎉
