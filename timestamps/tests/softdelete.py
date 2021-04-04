from django.test import TransactionTestCase
from .models import FooSoftDeletes as Foo


@Foo.fake_me
class SoftDeletesTestCase(TransactionTestCase):
    def test_soft_delete(self):
        foo = Foo()

        foo.save()
        self.assertIsNone(foo.deleted_at)

        foo.delete()
        self.assertIsNotNone(foo.deleted_at)

        # querying table again to check if object still exists
        self.assertEqual(1, Foo.objects_with_deleted.count())

    def test_restore(self):
        foo = Foo()
        foo.save()

        foo.delete()
        self.assertIsNotNone(foo.deleted_at)

        self.assertEqual(0, Foo.objects.count())

        foo.restore()
        self.assertEqual(1, Foo.objects.count())

    def test_querysets_count(self):
        foo1 = Foo()
        foo1.save()

        self.assertEquals(1, Foo.objects.count())
        self.assertEquals(0, Foo.objects_deleted.count())
        self.assertEquals(1, Foo.objects_with_deleted.count())

        foo1.delete(hard=False)
        self.assertEquals(0, Foo.objects.count())
        self.assertEquals(1, Foo.objects_deleted.count())
        self.assertEquals(1, Foo.objects_with_deleted.count())

        foo1.restore()

        foo2 = Foo()
        foo2.save()

        self.assertEquals(2, Foo.objects.count())
        self.assertEquals(0, Foo.objects_deleted.count())
        self.assertEquals(2, Foo.objects_with_deleted.count())

        foo2.delete(hard=False)
        self.assertEquals(1, Foo.objects.count())
        self.assertEquals(1, Foo.objects_deleted.count())
        self.assertEquals(2, Foo.objects_with_deleted.count())

        foo2.delete(hard=True)
        self.assertEquals(1, Foo.objects.count())
        self.assertEquals(0, Foo.objects_deleted.count())
        self.assertEquals(1, Foo.objects_with_deleted.count())

    def test_bulk_soft_delete(self):
        Foo().save()
        Foo().save()

        self.assertEquals(2, Foo.objects.count())

        Foo.objects.delete()
        self.assertEquals(0, Foo.objects.count())
        self.assertEquals(2, Foo.objects_deleted.count())

    def test_bulk_hard_delete(self):
        Foo().save()
        Foo().save()

        self.assertEquals(2, Foo.objects.count())

        Foo.objects.delete(hard=True)
        self.assertEquals(0, Foo.objects_with_deleted.count())

    def test_bulk_restore(self):
        Foo().save()
        Foo().save()

        self.assertEquals(2, Foo.objects.count())

        Foo.objects.delete()
        self.assertEquals(0, Foo.objects.count())

        Foo.objects_deleted.restore()
        self.assertEquals(2, Foo.objects.count())
