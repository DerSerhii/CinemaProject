from django.views import generic


class ChatView(generic.TemplateView):
    template_name = 'sockets/chat.html'


class FilmChatView(generic.TemplateView):
    template_name = 'sockets/film-chat.html'
