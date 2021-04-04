from django.test import TransactionTestCase
from .models import FooTimestamps as Foo


@Foo.fake_me
class TimestampableTestCase(TransactionTestCase):
    def test_created_at_is_set_on_create(self):
        f = Foo()
        self.assertIsNone(f.created_at)

        f.save()
        self.assertIsNotNone(f.created_at)

    def test_updated_at_is_set_on_create(self):
        f = Foo()
        self.assertIsNone(f.updated_at)

        f.save()
        self.assertIsNotNone(f.updated_at)

    def test_updated_at_is_set_on_update(self):
        f = Foo()
        f.save()

        updated_at = f.updated_at
        
        f.save()
        self.assertNotEquals(updated_at, f.updated_at)

    def test_created_at_is_not_set_on_update(self):
        f = Foo()
        f.save()

        created_at = f.created_at
        
        f.save()
        self.assertEquals(created_at, f.created_at)
