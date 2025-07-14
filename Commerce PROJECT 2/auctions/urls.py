from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("display", views.display, name="display"),
    path("listing/<int:id>", views.listing, name="listing"),    
    path('removewatchlist/<int:id>', views.removewatchlist, name="removewatchlist"), 
    path('addwatchlist/<int:id>', views.addwatchlist, name="addwatchlist"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('comment/<int:id>', views.comment, name="comment"),
    path('bid/<int:id>', views.bid, name="bid"),
    path('closing/<int:id>', views.closing, name="closing"),
]

