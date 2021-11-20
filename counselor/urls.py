from django.urls import path

from counselor.views import GetRankSuggestionAPIView

app_name = 'counselor'

urlpatterns = [
    path('get_rank_suggestion', GetRankSuggestionAPIView.as_view())

]
