from django.test import TransactionTestCase
from timestamps import signals

from tests.models import FooSoftDeletes as Foo


@Foo.fake_me
class TestSoftDeleteSignal(TransactionTestCase):
    def test_pre_soft_delete(self):
        self.signaled = False

        foo = Foo()
        foo.save()

        def handler(sender, instance, **kwargs):
            self.signaled = True

            self.assertEqual(sender, Foo)
            self.assertIs(instance, foo)
            self.assertIsNone(instance.deleted_at)

        signals.pre_soft_delete.connect(handler)
        
        foo.soft_delete()
        self.assertTrue(self.signaled)

        signals.pre_soft_delete.disconnect(handler)

    def test_post_soft_delete(self):
        self.signaled = False

        foo = Foo()
        foo.save()

        def handler(sender, instance, **kwargs):
            self.signaled = True

            self.assertEqual(sender, Foo)
            self.assertIs(instance, foo)
            self.assertIsNotNone(instance.deleted_at)

        signals.post_soft_delete.connect(handler)
        
        foo.soft_delete()
        self.assertTrue(self.signaled)

        signals.post_soft_delete.disconnect(handler)


    def test_pre_restore(self):
        self.signaled = False

        foo = Foo()
        foo.save()
        foo.soft_delete()

        def handler(sender, instance, **kwargs):
            self.signaled = True

            self.assertEqual(sender, Foo)
            self.assertIs(instance, foo)
            self.assertIsNotNone(instance.deleted_at)

        signals.pre_restore.connect(handler)
        
        foo.restore()
        self.assertTrue(self.signaled)

        signals.pre_restore.disconnect(handler)

    def test_post_restore(self):
        self.signaled = False

        foo = Foo()
        foo.save()
        foo.soft_delete()

        def handler(sender, instance, **kwargs):
            self.signaled = True

            self.assertEqual(sender, Foo)
            self.assertIs(instance, foo)
            self.assertIsNone(instance.deleted_at)

        signals.post_restore.connect(handler)
        
        foo.restore()
        self.assertTrue(self.signaled)

        signals.post_restore.disconnect(handler)
