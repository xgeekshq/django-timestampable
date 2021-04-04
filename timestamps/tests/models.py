from django_fake_model import models as f
from ..models import SoftDeletes, Timestampable


class FooTimestamps(f.FakeModel, Timestampable):
    pass


class FooSoftDeletes(f.FakeModel, SoftDeletes):
    pass
