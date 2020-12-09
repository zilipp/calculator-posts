from django.urls import path
from chat.views import home, login, signup, signout

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('signup/', signup),
    path('logout/', signout),
]
