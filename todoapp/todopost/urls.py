from django.urls import path
from . import views


urlpatterns = [
    path('',views.home_view,name='home'),
    path('post/<int:post_id>/',views.detail_view,name='post-detail'),
    path('post/create/',views.create_post,name='post-create'),
    path('post/<int:post_id>/share/',views.post_share,name='post-share'),
    path('post/delete/',views.delete_post,name='post-delete'),
    path('post/<int:post_id>/update/',views.update_post,name='post-update'),
    path('comment/delete/',views.delete_comment,name='comment-delete'),
    path('comment/<int:comment_id>/update/',views.comment_update,name='comment-update'),
]