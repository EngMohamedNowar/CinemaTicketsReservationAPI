from django.urls import path
from . import views

urlpatterns = [
    path('cbv/',views.CBV_list.as_view()),
    path('cbv/<int:pk>',views.CBV_PK.as_view()),
    path('mixins/',views.Mixins_list.as_view()),
    path('mixins/<int:pk>',views.Mixins_pk.as_view()),
    path('generics/',views.Generics_list.as_view()),
    path('generics/<int:pk>',views.Generics_pk.as_view()),

]