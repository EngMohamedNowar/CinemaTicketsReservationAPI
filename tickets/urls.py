from django.urls import path ,include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests',views.Viewsets_guest)
router.register('movie',views.Viewsets_movie)
router.register('reservation',views.Viewsets_reservation)


urlpatterns = [
    path('cbv/',views.CBV_list.as_view()),
    path('cbv/<int:pk>',views.CBV_PK.as_view()),
    path('mixins/',views.Mixins_list.as_view()),
    path('mixins/<int:pk>',views.Mixins_pk.as_view()),
    path('generics/',views.Generics_list.as_view()),
    path('generics/<int:pk>',views.Generics_pk.as_view()),
    path('viewsets/', include(router.urls)),
    path('findmovies/',views.find_movie),
    path('create_reservation/',views.create_reservation),
]