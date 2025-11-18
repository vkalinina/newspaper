from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Redactor, Article, Topic
from .forms import (
    RedactorCreationForm,
    RedactorExperienceUpdateForm,
    ArticleForm,
    RedactorSearchForm,
    ArticleSearchForm,
    TopicSearchForm
)


@login_required
def index(request):
    """View function for the home page of the site."""

    num_redactors = Redactor.objects.count()
    num_articles= Article.objects.count()
    num_topics = Topic.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_redactors": num_redactors,
        "num_articles": num_articles,
        "num_topics": num_topics,
        "num_visits": num_visits + 1,
    }

    return render(request, "catalog/index.html", context=context)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "catalog/topic_list.html"
    paginate_by = 5

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(TopicListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TopicSearchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("catalog:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("catalog:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("catalog:topic-list")


class ArticleListView(LoginRequiredMixin, generic.ListView):
    model = Article
    paginate_by = 5

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        model = self.request.GET.get("model", "")
        context["search_form"] = ArticleSearchForm(
            initial={"model": model}
        )
        return context

    def get_queryset(self):
        queryset = Article.objects.select_related("topic")
        model = self.request.GET.get("model")
        if model:
            return queryset.filter(model__icontains=model)
        return queryset


class ArticleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Article


class ArticleCreateView(LoginRequiredMixin, generic.CreateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("catalog:article-list")


class ArticleUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("catalog:article-list")


class ArticleDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Article
    success_url = reverse_lazy("catalog:article-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 5

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.GET.get("username")
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset.order_by("username")


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related("articles__redactors")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_url = reverse_lazy("catalog:redactor-list")


class RedactorExperienceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorExperienceUpdateForm
    success_url = reverse_lazy("catalog:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("catalog:redactor-list")


@login_required
def toggle_assign_to_articles(request, pk):
    redactor = Redactor.objects.get(id=request.user.id)
    if (
        Article.objects.get(id=pk) in redactor.articles.all()
    ):  # probably could check if car exists
        redactor.articles.remove(pk)
    else:
        redactor.articles.add(pk)
    return HttpResponseRedirect(reverse_lazy("catalog:article-detail", args=[pk]))

