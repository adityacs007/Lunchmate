from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
from django.contrib.auth.models import User
from friendship.models import Friend, Follow
import logging
from django.views.generic.base import TemplateView
from friendship.exceptions import AlreadyExistsError

try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User


class HomeView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        return { 'all_users': User.objects.all()}
        
def home(request):
    if not request.user.is_anonymous():
        friends= Friend.objects.friends(User.objects.get(username=request.user))
    else:
        friends=[]
    context = {'request': request, 'user': request.user,
               'is_anon': request.user.is_anonymous(),
               'friends': friends,
                'all_users': User.objects.all()}   
    logging.info(context['user'])
    
    return render_to_response('homepage.html',context,context_instance=RequestContext(request))

def add_friend(request, to_username):
    """ Create a FriendshipRequest """
    if request.user:
        friends= Friend.objects.friends(User.objects.get(username=request.user))
    else:
        friends=[]
    ctx = {'to_username': to_username, 'friends': friends,
           'all_users': User.objects.all(),'request': request, 'user': request.user}

    if request.method == 'GET':
        to_user = user_model.objects.get(username=to_username)
        from_user = request.user
        try:
            #logging.info('try before add:'+to_username)
            Friend.objects.add_friend(from_user, to_user)
            #logging.info('try after add:'+to_username)
        except AlreadyExistsError as e:
            ctx['errors'] = ["%s" % e]
            #logging.info('catch:'+to_username)

    return render(request, 'homepage.html', ctx)


def my_view(request):
    # List of this user's friends
    all_friends = Friend.objects.friends(request.user)

    # List all unread friendship requests
    requests = Friend.objects.unread_requests(user=request.user)

    # List all rejected friendship requests
    rejects = Friend.objects.rejected_requests(user=request.user)

    # Count of all rejected friendship requests
    #reject_count = Friend.objects.rejected_request_count(user=request.user)

    # List all unrejected friendship requests
    unrejects = Friend.objects.unrejected_requests(user=request.user)

    # Count of all unrejected friendship requests
    unreject_count = Friend.objects.unrejected_request_count(user=request.user)

    # List all sent friendship requests
    sent = Friend.objects.sent_requests(user=request.user)

    # List of this user's followers
    all_followers = Follow.objects.followers(request.user)

    # List of who this user is following
    following = Follow.objects.following(request.user)

    ### Managing friendship relationships

    # Create a friendship request
    other_user = User.objects.get(pk=1)
    new_relationship = Friend.objects.add_friend(request.user, other_user)

    
    # Can optionally save a message when creating friend requests
    message_relationship = Friend.objects.add_friend(
        from_user=request.user,
        to_user=other_user,
        message='Hi, I would like to be your friend',
    )

    # And immediately accept it, normally you would give this option to the user
    new_relationship.accept()

    # Now the users are friends
    Friend.objects.are_friends(request.user, other_user) == True

    # Remove the friendship
    Friend.objects.remove_friend(other_user, request.user)

    # Create request.user follows other_user relationship
    following_created = Follow.objects.add_follower(request.user, other_user)
    
    context = {'request': request, 'user': request.user}
    return render_to_response('homepage.html',context)

def index(request):
   context = {'request': request, 'user': request.user}
   return render_to_response('index.html',context)