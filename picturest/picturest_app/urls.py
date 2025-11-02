from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main, name='index'),
    path('signup/', views.signup, name='signup'),
    path('home-page/', views.home_page, name='homepage'),
    path('logout/', views.logout_view, name='logout'),
    path('image-edit/<int:id>/', views.image_edit, name='image_edit'),
    path('image-delete/<int:id>/', views.image_delete, name='image_delete'),
    path('user-profile/<str:username>/', views.user_profile, name='user_profile'),
    path('get-img-data/', views.get_img_data, name='get_img_data'),
    path('user-profile/<str:username>/edit/', views.edit_user_profile, name='edit_profile'),
    path('download-image/<int:id>/', views.download_image, name='download_image'),
    path('bookmark-image/', views.bookmarkImage, name='bookmark_image'),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)