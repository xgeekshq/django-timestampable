from rest_framework import routers


class DefaultRouter(routers.DefaultRouter):
    def __init__(self, *args, **kwargs):
        super(DefaultRouter, self).__init__(*args, **kwargs)

    routers.DefaultRouter.routes[0].mapping.setdefault('delete', 'bulk_destroy')

    # list deleted
    routers.DefaultRouter.routes.insert(0, routers.Route(
        url=r'^{prefix}/deleted{trailing_slash}$',
        mapping={
            'get': 'list_deleted',
        },
        name='{basename}-list-deleted',
        detail=False,
        initkwargs={'suffix': 'Deleted'}
    ))

    # list with deleted
    routers.DefaultRouter.routes.insert(1, routers.Route(
        url=r'^{prefix}/with-deleted{trailing_slash}$',
        mapping={
            'get': 'list_with_deleted',
        },
        name='{basename}-list-with-deleted',
        detail=False,
        initkwargs={'suffix': 'With Deleted'}
    ))

    # bulk restore
    routers.DefaultRouter.routes.insert(2, routers.Route(
        url=r'^{prefix}/restore{trailing_slash}$',
        mapping={
            'patch': 'bulk_restore',
        },
        name='{basename}-list-restore',
        detail=False,
        initkwargs={'suffix': 'Restore'}
    ))

    # retrieve deleted
    routers.DefaultRouter.routes.insert(5, routers.Route(
        url=r'^{prefix}/deleted/{lookup}{trailing_slash}$',
        name='{basename}-deleted',
        mapping={
            'get': 'retrieve_deleted',
        },
        detail=True,
        initkwargs={'suffix': 'Deleted'}
    ))

    # retrieve with deleted
    routers.DefaultRouter.routes.insert(6, routers.Route(
        url=r'^{prefix}/with-deleted/{lookup}{trailing_slash}$',
        name='{basename}-with-deleted',
        mapping={
            'get': 'retrieve_with_deleted',
        },
        detail=True,
        initkwargs={'suffix': 'With Deleted'}
    ))

    # restore
    routers.DefaultRouter.routes.insert(7, routers.Route(
        url=r'^{prefix}/{lookup}/restore{trailing_slash}$',
        name='{basename}-restore',
        mapping={
            'patch': 'restore',
        },
        detail=True,
        initkwargs={'suffix': 'Restore'}
    ))
