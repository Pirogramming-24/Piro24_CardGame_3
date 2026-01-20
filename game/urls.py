
from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path("", views.game_main, name="game_main"),
    path("create/", views.create_game, name="create_game"),
    path("list/", views.list_game, name="list_game"),
    path("detail/<int:pk>/", views.game_detail, name="game_detail"),
    path("counter/<int:pk>/", views.counter_attack, name="counter_attack"),
    path("counter/<int:pk>/submit/", views.submit_counter_attack, name="submit_counter"),
    path("cancel/<int:pk>/", views.game_cancel, name="game_cancel"),
    path("ranking/", views.ranking, name="ranking"),
]
