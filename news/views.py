from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View, generic

from news.forms import TopicSearchForm
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
