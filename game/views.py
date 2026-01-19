from django.shortcuts import render, get_object_or_404, redirect
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Game
from .utils import calculate_game_result, is_valid_card_number
from django.core.paginator import Paginator

User = get_user_model()

@login_required
def game_main(request):
    return render(request, "game/main.html")



# 3. start 버튼을 누르면 나타나는 페이지 (= 공격하기)
@login_required
def create_game(request):
    if request.method == "POST":
        defender_id = request.POST.get("defender_id")
        attacker_card = request.POST.get("attacker_card")

        defender = User.objects.get(id=defender_id)

        Game.objects.create(
            attacker=request.user,
            defender=defender,
            attacker_card=attacker_card,
            win_rule=random.choice(["HIGH", "LOW"]),
            status=Game.Status.REQUESTED
        )

        return redirect("game:list_game")

    cards = random.sample(range(1, 11), 5)
    users = User.objects.exclude(id=request.user.id)

    return render(request, "game/create_game.html", {
        "cards": cards,
        "users": users,
    })


# 4. 게임 전적 페이지 (= 게임 진행 list)
@login_required
def list_game(request):
    filter_type = request.GET.get("filter", "all")

    games_qs = (
        Game.objects.filter(attacker=request.user)
        | Game.objects.filter(defender=request.user)
    )

    if filter_type == "ongoing":
        games_qs = games_qs.exclude(status=Game.Status.FINISHED)
    elif filter_type == "finished":
        games_qs = games_qs.filter(status=Game.Status.FINISHED)

    games_qs = games_qs.order_by("-id") #역순정렬

    # 페이지네이션
    paginator = Paginator(games_qs, 8)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    for game in page_obj:
        game.display_status = game.display_status_for(request.user)
        game.can_counter = game.can_counter(request.user)
        game.can_cancel = game.can_cancel(request.user)
        game.user_result = game.result_for(request.user) #html이랑 연결하기 위한 임시 꼬리표

    return render(request, "game/list_game.html", {
        "page_obj": page_obj,
        "filter": filter_type,
    })

# 취소
@login_required
def game_cancel(request, pk):
    game = get_object_or_404(Game, pk=pk, attacker=request.user)

    if game.status != Game.Status.REQUESTED:
        return redirect("game:list_game")

    game.delete()
    return redirect("game:list_game")





# 5. 게임 상세 페이지
@login_required
def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)

    user = request.user

    if user not in [game.attacker, game.defender]:
        return redirect("game:list_game")

    context = {
        "game": game,
        "is_attacker": user == game.attacker,
        "is_defender": user == game.defender,
        "display_status": game.display_status_for(user),
        "can_counter": game.can_counter(user),
        "can_cancel": game.can_cancel(user),
    }

    context["my_card"] = game.attacker_card if user == game.attacker else game.defender_card
    context["opponent_card"] = game.defender_card if user == game.attacker else game.attacker_card

    if game.status == Game.Status.FINISHED:
        context.update({
            "result": game.result_for(user), 
            "my_score": game.score_for(user),
            "opponent_score": game.score_for(
                game.defender if user == game.attacker else game.attacker
            ),
        })

    return render(request, "game/game_detail.html", context)



# 6. 반격하기 페이지 (= 반격하기 버튼 눌렀을 때) // 여기부터 해주면 됩니다!
@login_required
def counter_attack(request, pk):
    game = get_object_or_404(Game, pk=pk, defender=request.user)

    if game.status == Game.Status.FINISHED:
        return redirect('game:game_detail', pk=game.id)

    cards = random.sample(range(1, 11), 5)

    return render(request, "game/counter_attack.html", {
        "game": game,
        "cards": cards,
    })


# 7. 반격 제출
@login_required
@require_POST
def submit_counter_attack(request, pk):
    game = get_object_or_404(Game, pk=pk)

    if game.defender != request.user:
        return redirect('game:list_game')

    if game.status == Game.Status.FINISHED:
        return redirect('game:game_detail', pk=game.id)

    selected_card = request.POST.get('card')

    if not is_valid_card_number(selected_card):
        return redirect('game:counter_attack', pk=game.id)

    selected_card = int(selected_card)

    game.defender_card = selected_card
    game.status = Game.Status.FINISHED

    calculate_game_result(game)

    game.save()

    return redirect('game:game_detail', pk=game.id)


# 8. 랭킹 페이지
@login_required
def ranking(request):
    from account.models import Profile
    
    profiles = Profile.objects.all().order_by('-score')
    
    my_rank = "Unranked" # rank계산 추가
    if hasattr(request.user, 'profile'):
        my_profile = request.user.profile
        
        for index, profile in enumerate(profiles):
            if profile == my_profile:
                my_rank = index + 1
                break
    
    return render(request, "game/ranking.html", {
        "profiles": profiles,
        "my_rank": my_rank,
    })
