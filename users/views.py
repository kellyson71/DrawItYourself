from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message, MessageImage, UserFollow
from django.utils import timezone
from django.db.models import Q
from drawings.models import Post  # Adicionar esta importação

@login_required
def send_message(request, username):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        try:
            sender = User.objects.get(id=request.user.id)
            receiver = User.objects.get(username=username)
            
            if content or image:
                message = Message.objects.create(
                    sender=sender,
                    receiver=receiver,
                    content=content,
                    created_at=timezone.now()
                )
                
                if image:
                    MessageImage.objects.create(
                        message=message,
                        image=image
                    )
                    
                return JsonResponse({'status': 'success'})
                
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Usuário não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def inbox(request):
    messages = Message.objects.filter(
        receiver=request.user
    ).select_related('sender').order_by('-created_at')

    for message in messages:
        message.has_image = MessageImage.objects.filter(message=message).exists()

    context = {
        'messages': messages
    }
    return render(request, 'users/inbox.html', context)

@login_required
def chat_detail(request, username):
    other_user = get_object_or_404(User, username=username)
    
    # Marca todas as mensagens como lidas
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)
    
    # Busca todas as mensagens entre os usuários
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=other_user) |
         Q(sender=other_user, receiver=request.user))
    ).select_related('sender').order_by('created_at')

    for message in messages:
        message.has_image = MessageImage.objects.filter(message=message).exists()

    # Buscar chats recentes (últimas pessoas com quem conversou)
    recent_chats = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).values('sender', 'receiver').distinct().order_by('-created_at')[:5]
    
    recent_users = set()
    for chat in recent_chats:
        if chat['sender'] != request.user.id:
            recent_users.add(chat['sender'])
        if chat['receiver'] != request.user.id:
            recent_users.add(chat['receiver'])
    
    recent_users = User.objects.filter(id__in=recent_users)
    
    context = {
        'chat_user': other_user,
        'messages': messages,
        'recent_users': recent_users
    }
    return render(request, 'users/chat_detail.html', context)

@login_required
def toggle_follow(request, username):
    try:
        user_to_follow = User.objects.get(username=username)
        if request.user == user_to_follow:
            return JsonResponse({'status': 'error', 'message': 'Você não pode seguir a si mesmo'})
            
        follow, created = UserFollow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        
        if not created:
            follow.delete()
            is_following = False
        else:
            is_following = True
            
        return JsonResponse({
            'status': 'success',
            'is_following': is_following
        })
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Usuário não encontrado'})

@login_required
def following_artists(request):
    following = UserFollow.objects.filter(follower=request.user).select_related('following')
    artists = [follow.following for follow in following]
    
    for artist in artists:
        artist.posts_count = Post.objects.filter(author=artist).count()
        artist.followers_count = UserFollow.objects.filter(following=artist).count()
    
    context = {
        'artists': artists
    }
    return render(request, 'following_artists.html', context)
