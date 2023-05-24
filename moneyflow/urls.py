from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), #Pagina principal
    path('signup/', views.signup),
    path('login/', views.log_in),
    path('about/', views.about), #Pagina /about
    path('general/', views.general),
    path('show/', views.show),
    path('insert/', views.insert),
    path('withheld/', views.withheld),
    path('details/<int:id>/', views.move_detail, name='details'),
    path('update/<int:id>',views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('logout/', views.log_out)
]