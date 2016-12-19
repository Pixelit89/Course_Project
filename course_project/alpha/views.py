from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from personal_page.models import Account
from .models import Chat


class ConversationsView(LoginRequiredMixin, generic.TemplateView):
    login_url = '/login/'
    redirect_field_name = ''
    template_name = 'alpha/conversations.html'

    def get_context_data(self, **kwargs):
        context = super(ConversationsView, self).get_context_data(**kwargs)
        user = Account.objects.get(id=self.request.session['id'])
        context['friends'] = user.friends.all()
        context['avatar'] = user.avatar
        context['chats'] = []
        try:
            chats = Chat.objects.filter(Q(account_id=user.id) | Q(companion_id=user.id))
            for chat in chats:
                if chat.account_id == user.id and chat.companion_id not in context['chats']:
                    context['chats'].append(chat.companion_id)
                elif chat.companion_id == user.id and chat.account_id not in context['chats']:
                    context['chats'].append(chat.account_id)
        except Chat.DoesNotExist:
            context['chats'] = ''
        return context


def messages(request, account_id, companion_id):
    c = Chat.objects.filter(Q(account_id=account_id, companion_id=companion_id) |
                            Q(account_id=companion_id, companion_id=account_id)).order_by('created')
    user = Account.objects.get(id=request.session['id'])
    context = {
        'home': 'active',
        'chat': c,
        'avatar': user.avatar,
        'companion_id': companion_id,
        'account_id': companion_id
    }
    return render(request, "alpha/home.html", context)


def Post(request, account_id, companion_id):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(account_id=account_id, companion_id=companion_id, message=msg)
        if msg != '':
            c.save()
        return JsonResponse({ 'msg': msg, 'user': c.account.username })
    else:
        return HttpResponse('Request must be POST.')


def messages_box(request, account_id, companion_id):
    c = Chat.objects.filter(Q(account_id=account_id, companion_id=companion_id) |
                            Q(account_id=companion_id, companion_id=account_id)).order_by('created')
    return render(request, 'alpha/messages.html', {'chat': c})