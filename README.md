# Devstagram

Devstagram - Django project for Python Web Framework Exam Project in Softuni

Developed on Django version 3.1.7
Using PostgreSQL as DB and Django Channels for Real-time features

# Description
Devstagram is a social media app designed to connect you with your friends, and make new ones.

The application has 3 parts -> 1) Public, 2) Private, 3)Admin

In the Public part not authenticated users, can browse the Posts feed and search for users.
The Private part of the application is only for authenticated users. There users can see each other's posts, like and comment them, and see which users liked a certain post.
Also authenticated users can send each other friend requests and become friends.
When 2 users are friends they can send each other real-time messages, and posts.

The application is divided in three main modules -> 1) registration, 2) mainsite, 3) async_chat
#
The registration module handles all of the authentication functionality - Creating an account, and logging into an accont
#
The mainsite module contains all of the main functionality of the application like handling the uploading of pictures, liking and commenting of pictures, and searching for users.
This module also handles the sending of notifications when a user receives a like on his picture
#
The async_chat module handles all of the real time messaging features.

# Author
Georgi Pavlov
Project for educational purposes
