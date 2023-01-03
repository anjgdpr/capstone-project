from django.urls import path 
from django.conf import settings
from . import views 
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


App_name = 'books'
urlpatterns = [
    path('', views.index, name='index'), 
    path('lib_index', views.lib_index, name='lib_index'), 
    path('login', views.loginview, name='loginview'),
    path('signup', views.signup, name='signup'),
    path('register', views.register, name='register'),
    path('contact', views.contact, name='contact'),
    path('processlogin', views.processlogin, name='processlogin'),
    path('logout', views.processlogout, name='processlogout'),
    path('browse', views.browse, name='browse'),
    path('s_browse', views.s_browse, name='s_browse'),
    path('locked', views.l_browse, name='l_browse'),
    path('add', views.add, name='add'),
    path('search', views.search, name='search'),
    path('s_search', views.s_search, name='s_search'),
    path('searchfav', views.searchfav, name='searchfav'),
    path('filterview',views.filterview, name='filterview'),
    path('libfilterview',views.libfilterview, name='libfilterview'),
    path('filterfav',views.filterfav, name='filterfav'),
    path('processadd',views.processadd, name='processadd'),
    path('<int:book_id>/detail/', views.detail, name='detail'),
    path('<int:book_id>/s_detail/', views.s_detail, name='s_detail'),
    path('<int:book_id>/edit/', views.edit, name='edit'),
    path('<int:book_id>/processedit/', views.processedit, name='processedit'),
    path('fav/<int:id>/', views.favorite_add, name='favorite_add'),
    path('favorites', views.favorite_list, name='favorite_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()

    