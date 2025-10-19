from django.shortcuts import render, redirect
from . import models
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, 'login_register.html')


def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = models.User.objects.register_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="register")
        return redirect('/')
    users = models.get_user_using_email(request.POST['email'])
    if len(users) > 0:
        messages.error(request, "email is already used", extra_tags="login")
    password = request.POST['pass']
    hash_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = models.add_user(request.POST, hash_pass)
    request.session['user_id'] = user.id
    return redirect('/dashboard')

def login(request):
    if request.method == "GET":
        return redirect('/')
    errors = models.User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="login")
        return redirect('/')
    user = models.get_user_using_email(request.POST['email'])
    if len(user) == 0:
        messages.error(request, "email or password does not exist", extra_tags="login")
    password = request.POST['pass']
    chack = bcrypt.checkpw(password.encode() ,user[0].password.encode())
    if chack == False:
        messages.error(request, "email or password does not exist", extra_tags="login")
    request.session['user_id'] = user[0].id
    return redirect('/dashboard')

def dashboard(request):
    user = models.get_user(request.session['user_id'])
    games = models.get_games()
    context = {
        'games': games,
        'geners': models.get_geners(),
        'user': user
    }
    return render(request, 'all_games.html', context)

def add_game(request):
    if request.method == "GET":
        return redirect('/dashboard')
    errors = models.Game.objects.game_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="game")
        return redirect('/dashboard')
    user = models.get_user(request.session['user_id'])
    models.add_game(request.POST, user)
    return redirect('/dashboard')

def game_details(request, id):
    user = models.get_user(request.session['user_id'])
    game = models.get_game(id)
    favorits = models.get_favorites(game.id)
    context = {
        'game': game,
        'user': user,
        'favorites': favorits
    }
    return render(request, 'game_details.html', context)

def logout(request):
    if request.method == "GET":
        return redirect('/dashboard')
    del request.session['user_id']
    return redirect('/')

def flush(request):
    request.session.flush()
    return redirect('/')

def edit_data(request, id):
    game = models.get_game(id)
    user = models.get_user(request.session['user_id'])
    context = {
        'game': game,
        'user': user
    }
    return render(request, 'edit_data.html', context)

def change_data(request):
    if request.method == "GET":
        return redirect('/dashboard')
    errors = models.Game.objects.game_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="game")
        return redirect('/dashboard')
    game = models.get_game(request.POST['game_id'])
    models.update_game_name(game.id, request.POST['name'])
    models.update_game_gener(game.id, request.POST['new_type'])
    models.update_game_date(game.id, request.POST['date'])
    models.update_game_desc(game.id, request.POST['desc'])
    return redirect(f'/edit/game/{game.id}')

def delete(request, id):
    game = models.get_game(id)
    models.delete_game(game)
    return redirect('/dashboard')