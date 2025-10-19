from django.db import models
import re
from django.utils import timezone

class UserManager(models.Manager):
    def register_validation(self, post):
        errors = {}

        email_pattern = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if post['fname'] == '':
            errors['fname'] = "First Name should not be blank"
        elif len(post['fname']) < 4:
            errors['fname'] = "First Name should not be at least 4 chars"
        
        if post['lname'] == '':
            errors['lname'] = "Last Name should not be blank"
        elif len(post['lname']) < 4:
            errors['lname'] = "Last Name should not be at least 4 chars"
        
        if post['email'] == '':
            errors['email'] = "email should not be blank"
        elif not email_pattern.match(post['email']):
            errors['email'] = "email not match"
        
        if post['pass'] == '':
            errors['pass'] = "Password should not be blank"
        elif len(post['pass']) < 8:
            errors['pass'] = "Password should not be at least 8 chars"
        
        if post['cpass'] == '':
            errors['cpass'] = "Confirme Password should not be blank"
        elif post['cpass'] != post['pass']:
            
            errors['pass'] = "password and confirm password not match"
        if post['avatar'] == '':
            errors['avatar'] = "Avatar should not be blank"
        
        if post['date'] == "":
            errors['date'] = "date should not be blank"
        
        return errors
    
    def login_validator(self, post):
        errors = {}
        email_pattern = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if post['email'] == '':
            errors['email'] = "email should not be blank"
        elif not email_pattern.match(post['email']):
            errors['email'] = "email not match"
        if post['pass'] == '':
            errors['pass'] = "Password should not be blank"
        elif len(post['pass']) < 8:
            errors['pass'] = "Password should not be at least 8 chars"
        return errors

class GameManager(models.Manager):
    def game_validator(self, post):
        errors = {}
        date = timezone.now().date()
        date_patern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
        if post['name'] == '':
            errors['name'] = "game name should be not blank"
        elif len(post['name']) < 2:
            errors['name'] = "game name should at least 2 chars"
        
        if(post['date'] == ''):
            errors['date'] = "date should not blank"
            
        
        if post['desc'] == '':
            errors['desc'] = "Description should be not blank"
        return errors
class User(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    date = models.DateTimeField()
    avatar = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Game(models.Model):
    name = models.CharField(max_length=40)
    Genre = models.CharField(max_length=40)
    date = models.DateTimeField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="games", on_delete=models.CASCADE)
    objects = GameManager()
    rate = models.IntegerField()
    favorites = models.ManyToManyField(User, related_name="favorite_games")



def add_user(post, hash_pass):
    return User.objects.create(fname = post['fname'], lname = post['lname'], email = post['email'], password = hash_pass, date = post['date'])

def get_user_using_email(email):
    return User.objects.filter(email = email)
def get_user(id):
    return User.objects.get(id = id)

def add_game(post, user):
    return Game.objects.create(name = post['name'],date = post['date'], Genre = post['new_type'], desc = post['desc'], user = user, rate = 0)
def get_games():
    return Game.objects.all()

def get_geners():
    games = get_games()
    return games.values_list('Genre', flat=True)

def get_game(id):
    return Game.objects.get(id = id)

def get_favorites(game_id):
    game = get_game(game_id)
    return game.favorites.all()

def update_game_name(id, name):
    game = get_game(id)
    game.name = name
    game.save()

def update_game_gener(id, gener):
    game = get_game(id)
    game.Genre = gener
    game.save()

def update_game_date(id, date):
    game = get_game(id)
    game.date = date
    game.save()

def update_game_desc(id, desc):
    game = get_game(id)
    game.desc = desc
    game.save()

def delete_game(game):
    game.favorites.clear()
    game.delete()