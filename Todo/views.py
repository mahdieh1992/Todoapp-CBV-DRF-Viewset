from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .models import Todo


user=get_user_model()


class TodoCreate(CreateView):
    model = Todo
    template_name = 'Todo/index.html'
    fields = ('Title',)
    success_url = reverse_lazy('Todo:Todolist')

    def form_valid(self, form):
        instance=form.save(commit=False)
        instance.user=self.request.user
        instance.save()
        return super(TodoCreate, self).form_valid(form)


class EditeTodo(UpdateView):
    template_name = 'Todo/Update.html'
    model = Todo
    fields = ('Title','Completed')
    success_url = reverse_lazy('Todo:Todolist')


class DeleteTodo(DeleteView):
    template_name = 'Todo/Delete.html'
    model = Todo
    success_url = reverse_lazy('Todo:Todolist')


class TodoList(ListView):
    model = Todo
    template_name = 'Todo/index.html'

    def get_queryset(self):
        request=self.request
        userget = self.request.user
        active=request.GET.get('active')
        completed=request.GET.get('completed')
        alluser=request.GET.get('all')

        if active:
            queryset=userget.todouser.filter(Is_active=True)
            return queryset
        elif completed:
            queryset = userget.todouser.filter(Completed=True)
            return queryset
        elif alluser:
            queryset = userget.todouser.all()
            return queryset
        else:
            queryset = userget.todouser.all()
            return queryset

    def get_context_data(self,**kwargs):
        context=super(TodoList, self).get_context_data()
        return context
