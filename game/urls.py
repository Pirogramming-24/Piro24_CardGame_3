
from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path("create/", views.create_game, name="create_game"),
    path("list/", views.list_game, name="list_game"),
    path("detail/<int:pk>/", views.game_detail, name="game_detail"),
    path("counter/<int:pk>/", views.counter_attack, name="counter_attack"),
    path("cancel/<int:pk>/", views.game_cancel, name="game_cancel"),
]
