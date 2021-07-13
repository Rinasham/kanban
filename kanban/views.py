from django.db import models
from django.shortcuts import render,redirect,resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView,UpdateView,CreateView,ListView,DeleteView
from django.urls import reverse_lazy

from .forms import UserForm,ListForm,CardForm
from .mixins import OnlyYouMixin
from .models import List,Card


def index(request):
    return render(request, "kanban/index.html")


class HomeView(LoginRequiredMixin,ListView):
    model=List
    template_name = "kanban/home.html"
    
    def get_queryset(self):
        return List.objects.filter(user=self.request.user)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            login(request, user_instance)
            return redirect("kanban:home")
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }
    return render(request, 'kanban/signup.html', context)


class UserDetailView(OnlyYouMixin, DetailView):
    model = User
    template_name = "kanban/users/detail.html"


class UserUpdateView(OnlyYouMixin,UpdateView):
    model = User
    template_name = "kanban/users/update.html"
    form_class = UserForm

    def get_success_url(self):
        return resolve_url('kanban:users_detail', pk=self.kwargs['pk'])


class ListCreateView(LoginRequiredMixin, CreateView):
    model = List
    template_name = "kanban/lists/create.html"
    form_class = ListForm
    success_url = reverse_lazy("kanban:lists_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ListListView(LoginRequiredMixin,ListView):
    model = List
    template_name = "kanban/lists/list.html"
    
    def get_queryset(self):
        return List.objects.filter(user=self.request.user)


class ListDetailView(LoginRequiredMixin,DetailView):
    model=List
    template_name="kanban/lists/detail.html"


class ListUpdateView(LoginRequiredMixin,UpdateView):
    model=List
    template_name="kanban/lists/update.html"
    form_class=ListForm
    success_url = reverse_lazy("kanban:home")

class ListDeleteView(LoginRequiredMixin,DeleteView):
    model=List
    template_name="kanban/lists/delete.html"
    success_url=reverse_lazy("kanban:home")


class CardCreateView(LoginRequiredMixin,CreateView):
    model=Card
    template_name="kanban/cards/create.html"
    form_class=CardForm
    success_url=reverse_lazy("kanban:home")
    
    def get_form_kwargs(self):
        kwargs = super(CardCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)


class CardListView(LoginRequiredMixin,ListView):
    model=Card
    template_name="kanban/cards/list.html"
    
    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)


class CardDetailView(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "kanban/cards/detail.html"


class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card
    template_name = "kanban/cards/update.html"
    form_class = CardForm
    success_url = reverse_lazy("kanban:home")
    
    def get_form_kwargs(self):
        kwargs = super(CardUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = "kanban/cards/delete.html"
    success_url = reverse_lazy("kanban:home")
