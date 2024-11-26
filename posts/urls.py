from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from posts.views import PostViewset

# router = DefaultRouter()
# router.register("", PostViewset, basename="posts")

urlpatterns = [
    # path('homepage/', views.homepage, name='posts_homepage'),
    # path("", include(router.urls)),
    path("", views.PostListCreateView.as_view(), name="post_list"),
    path("<int:pk>/", views.PostRetrieveUpdatedDeleteView.as_view(), name="post_detail"),
    path("current_user/", views.get_posts_for_current_user, name="current_user"),
    path("posts_for_current/", views.ListPostsForAuthor.as_view(), name="post_for_current_user"),
]