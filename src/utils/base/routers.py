from rest_framework.routers import DefaultRouter, DynamicRoute, Route


class CustomDefaultRouter(DefaultRouter):
    """
    A custom router for API endpoints,
    which uses trailing slashes.
    """
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/create{trailing_slash}$',
            mapping={'post': 'create'},
            name='{basename}-create',
            detail=False,
            initkwargs={'suffix': 'Create'}
        ),
        Route(
            url=r'^{prefix}/detail/{lookup}{trailing_slash}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        Route(
            url=r'^{prefix}/update/{lookup}{trailing_slash}$',
            mapping={
                'put': 'update',
                'patch': 'partial_update',
            },
            name='{basename}-update',
            detail=True,
            initkwargs={'suffix': 'Update'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/delete/{lookup}{trailing_slash}$',
            mapping={'delete': 'destroy'},
            name='{basename}-delete',
            detail=True,
            initkwargs={'suffix': 'Delete'}
        ),
    ]


class CustomRouterNoLookup(DefaultRouter):
    """
    A router for API endpoints without lookup names
    in detail urls
    """
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/create{trailing_slash}$',
            mapping={'post': 'create'},
            name='{basename}-create',
            detail=False,
            initkwargs={'suffix': 'Create'}
        ),
        Route(
            url=r'^{prefix}/detail{trailing_slash}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        Route(
            url=r'^{prefix}/update{trailing_slash}$',
            mapping={
                'post': 'update',
                'patch': 'partial_update',
            },
            name='{basename}-update',
            detail=True,
            initkwargs={'suffix': 'Update'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/delete{trailing_slash}$',
            mapping={'delete': 'destroy'},
            name='{basename}-delete',
            detail=True,
            initkwargs={'suffix': 'Delete'}
        ),
    ]

