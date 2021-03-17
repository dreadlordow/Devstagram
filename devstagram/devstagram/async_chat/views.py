from django.shortcuts import render


def chatroom(request, user_one, user_two):
    return render(request, 'async/chatroom.html')
