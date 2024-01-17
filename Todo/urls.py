from django.urls import path,include
from . import views

app_name='Todo'
urlpatterns=[
    path('',views.TodoList.as_view(),name='Todolist'),
    path('Create/',views.TodoCreate.as_view(),name='Create'),
    path('Edit/<int:pk>',views.EditeTodo.as_view(),name='Edit'),
    path('Delete/<int:pk>',views.DeleteTodo.as_view(),name='Delete'),
    path('api/v1/',include('Todo.api.v1.urls'))
]