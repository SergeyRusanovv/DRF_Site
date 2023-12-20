from rest_framework import routers


class MyCustomRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'^{prefix}$',  # шаблон маршрута
            mapping={'get': 'list'},  # связывает тип запроса и метод
            name='{basename}-list',  # название маршрута
            detail=False,  # список или отдельная запись
            initkwargs={'suffix': 'List'}  # доп аргументы для kwargs
        ),
        routers.Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        routers.DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        )
    ]
