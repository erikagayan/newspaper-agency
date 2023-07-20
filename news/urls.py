from django.urls import path

from .views import (
    index,
    TopicListView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "topics/",
        TopicListView.as_view(),
        name="topic_list",
    )
]

app_name = "news"
