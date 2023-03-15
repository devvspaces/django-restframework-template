from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from utils.base.routers import CustomDefaultRouter, CustomRouterNoLookup


class BookViewSet(ModelViewSet):

    @action(detail=False)
    def search(self, request):
        pass

    @action(detail=True)
    def read(self, request, pk=None):
        pass


def get_pattern(route):
    return route.pattern.regex.pattern


class TestCustomDefaultRouter:
    def test_custom_default_router(self):
        router = CustomDefaultRouter()
        router.register('books', BookViewSet, basename='books')
        routes = router.urls

        urls = router.get_routes(BookViewSet)

        assert len(routes) == 7

        assert routes[0].name == 'books-list'
        assert get_pattern(routes[0]) == r'^books/$'
        assert urls[0].mapping == {'get': 'list'}

        assert routes[1].name == 'books-search'
        assert get_pattern(routes[1]) == r'^books/search/$'
        assert urls[1].mapping == {'get': 'search'}

        assert routes[2].name == 'books-create'
        assert get_pattern(routes[2]) == r'^books/create/$'
        assert urls[2].mapping == {'post': 'create'}

        assert routes[3].name == 'books-detail'
        assert get_pattern(routes[3]) == r'^books/detail/(?P<pk>[^/.]+)/$'
        assert urls[3].mapping == {'get': 'retrieve'}

        assert routes[4].name == 'books-update'
        assert get_pattern(routes[4]) == r'^books/update/(?P<pk>[^/.]+)/$'
        assert urls[4].mapping == {'put': 'update', 'patch': 'partial_update'}

        assert routes[5].name == 'books-read'
        assert get_pattern(routes[5]) == r'^books/(?P<pk>[^/.]+)/read/$'
        assert urls[5].mapping == {'get': 'read'}

        assert routes[6].name == 'books-delete'
        assert get_pattern(routes[6]) == r'^books/delete/(?P<pk>[^/.]+)/$'
        assert urls[6].mapping == {'delete': 'destroy'}


class TestCustomRouterNoLookup:
    def test_custom_router_no_lookup(self):
        router = CustomRouterNoLookup()
        router.register('books', BookViewSet, basename='books')
        routes = router.urls

        urls = router.get_routes(BookViewSet)

        assert len(routes) == 7

        assert routes[0].name == 'books-list'
        assert get_pattern(routes[0]) == r'^books/$'
        assert urls[0].mapping == {'get': 'list'}

        assert routes[1].name == 'books-search'
        assert get_pattern(routes[1]) == r'^books/search/$'
        assert urls[1].mapping == {'get': 'search'}

        assert routes[2].name == 'books-create'
        assert get_pattern(routes[2]) == r'^books/create/$'
        assert urls[2].mapping == {'post': 'create'}

        assert routes[3].name == 'books-detail'
        assert get_pattern(routes[3]) == r'^books/detail/$'
        assert urls[3].mapping == {'get': 'retrieve'}

        assert routes[4].name == 'books-update'
        assert get_pattern(routes[4]) == r'^books/update/$'
        assert urls[4].mapping == {'put': 'update', 'patch': 'partial_update'}

        assert routes[5].name == 'books-read'
        assert get_pattern(routes[5]) == r'^books/read/$'
        assert urls[5].mapping == {'get': 'read'}

        assert routes[6].name == 'books-delete'
        assert get_pattern(routes[6]) == r'^books/delete/$'
        assert urls[6].mapping == {'delete': 'destroy'}
