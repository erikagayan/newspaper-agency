
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from news.forms import TopicSearchForm, NewspaperSearchForm, RedactorCreationForm, RedactorUpdateForm, NewspaperForm, \
    UserCreateForm
from news.models import Topic, Redactor, Newspaper


@login_required
def index(request):
    """View function for the home page of the site."""

    num_newspapers = Newspaper.objects.count()
    num_redactors = Redactor.objects.count()
    num_topics = Topic.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_newspapers": num_newspapers,
        "num_redactors": num_redactors,
        "num_topics": num_topics,
        "num_visits": num_visits + 1,
    }

    return render(request, "news/index.html", context=context)


class UserCreateView(generic.CreateView):
    model = Redactor
    form_class = UserCreateForm
    template_name = "registration/register_user.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect("news:index")


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "news/topic_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TopicSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        queryset = Topic.objects.all()

        form = TopicSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("news:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("news:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("news:topic-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 5


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related("newspapers__topic")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_url = reverse_lazy("news:redactor-list")


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorUpdateForm
    success_url = reverse_lazy("news:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    template_name = "news/redactor_confirm_delete.html"
    success_url = reverse_lazy("news:redactor-list")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")

        context["search_form"] = NewspaperSearchForm(initial={"title": title})

        return context

    def get_queryset(self):
        queryset = Newspaper.objects.all()

        form = NewspaperSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])

        return queryset


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("news:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("news:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("news:newspaper-list")
