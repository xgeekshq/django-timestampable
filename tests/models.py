import uuid
from timestamps.models import models,  Model


class Foo(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)


class Bar(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    foo = models.ForeignKey(Foo, on_delete=models.CASCADE)
