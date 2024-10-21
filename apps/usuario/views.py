from apps.usuario.models import Usuario
from apps.posts.models import Comentario, Post
from .forms import RegistroUsuarioForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from django.contrib.auth.models import Group

# Create your views here.

class RegistrarUsuario(CreateView):
    template_name = 'registration/registrar.html'
    form_class = RegistroUsuarioForm

    def form_valid(self, form):
        # Guarda el usuario antes de agregarlo al grupo
        self.object = form.save()
        
        # Agrega al grupo 'Registrado' después de guardar
        group = Group.objects.get(name='Registrado')
        self.object.groups.add(group)

        messages.success(self.request, 'Registro exitoso. Por favor, inicia sesión.')
        return redirect('apps.usuario:login')  # Redirige al login en lugar de redirigir de nuevo al formulario de registro

class LoginUsuario(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        messages.success(self.request, 'Login existoso.')

        return reverse('apps.usuario:login')


class LogoutUsuario(LogoutView):
    template_name = 'registration/logout.html'
    
    def get_succes_url(self):
        messages.success(self.request, "¡Sesión cerrada correctamente!")
        return reverse('apps.usuario:logout')
    
    """ def get(self, request, *args, **kwargs):
    messages.success(self.request, "¡Sesion cerrada correctamente!")
    return super().get(request, *args, **kwargs) """

class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'registration/usuario_list.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(is_superuser=True)
        return queryset

class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'registration/eliminar_usuario.html'
    success_url = reverse_lazy('apps.usuario:usuario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        colaborador_group = Group.objects.get(name='Colaborador')
        es_Colaborador = colaborador_group in self.object.groups.all()
        context['es_colaborador'] = es_Colaborador
        return context
    
    def post(self, request, *args, **kwargs):
        eliminar_comentarios = request.POST.get('eliminar_comentarios', False)
        eliminar_posts = request.POST.get('eliminar_posts', False)
        self.object = self.get_object()
        if eliminar_comentarios:
            Comentario.objects.filter(usuario= self.object).delete()
        
        if eliminar_posts:
            Post.objects.filter(autor=self.object).delete()
        messages.success(request, f'Usuario {self.object.username} eliminado correctamente')
        return self.delete(request, *args, **kwargs)
#sin embargo, cuando mejores el código en
#tu proyecto puedes usar, por ejemplo, SweetAlert para mostrar un mensaje emergente
#del registro exitoso y que se redirija a la página de iniciar sesión (puedes buscar
# en la documentación de Django e investigar
#sobre mensajes: https://docs.djangoproject.
#com/en/4.2/ref/contrib/messages/ y sobre
#mensajes SweeAlert: https://lipis.github.io/
#bootstrap-sweetalert/). Lo mismo puedes
#hacer para “login”, “logout” o “contacto” e
#incluso para “comentarios” (app que crearemos luego).