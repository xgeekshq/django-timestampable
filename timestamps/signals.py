from django.dispatch import Signal


pre_soft_delete = Signal()
post_soft_delete = Signal()

pre_restore = Signal()
post_restore = Signal()
