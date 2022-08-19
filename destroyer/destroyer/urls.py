"""destroyer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

#apps
import destroyer_app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', destroyer_app.views.home, name="home" ),
    path('profile', destroyer_app.views.profile, name="profile" ),
    path('question', destroyer_app.views.question, name="question" ),
    path('result', destroyer_app.views.result, name="result" ),
    path('ranking', destroyer_app.views.ranking, name="ranking" ),
    path('answer', destroyer_app.views.answer, name="answer" ),
    path('createuser', destroyer_app.views.createuser, name="createuser"),
]
