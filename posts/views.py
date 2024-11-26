from http.client import responses

from django.core.serializers import serialize
from django.template.defaulttags import querystring
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.decorators import api_view, APIView, permission_classes
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import CurrentUserPostsSerializer

class PostViewset(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class = PostSerializer

class PostListCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)

    def get(self,request:Request,*args,**kwargs):
        return self.list(request, *args, **kwargs)

    def post(self,request:Request,*args,**kwargs):
        return self.create(request, *args, **kwargs)

class PostRetrieveUpdatedDeleteView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request:Request):
    user=request.user
    serializer=CurrentUserPostsSerializer(instance=user, context={"request":request})

    return Response(data=serializer.data, status=status.HTTP_200_OK)

class ListPostsForAuthor(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        username=self.kwargs.get("username")
        return Post.objects.filter(author__username=username)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)