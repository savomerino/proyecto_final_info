from apps.usuario.models import Usuario
from apps.posts.models import Comentario, Post
from .forms import RegistroUsuarioForm, LoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import Group

class RegistrarUsuario(CreateView):
    template_name = 'registration/registrar.html'
    form_class = RegistroUsuarioForm

    def form_valid(self, form):
        # Guarda el usuario si el formulario es válido
        user = form.save()

        # Agrega al usuario al grupo 'Registrado'
        group = Group.objects.get(name='Registrado')
        user.groups.add(group)

        messages.success(self.request, 'Registro exitoso. Por favor, inicia sesión.')
        return redirect('apps.usuario:login')

    def form_invalid(self, form):
        messages.error(self.request, 'Error en el registro. Por favor, corrige los errores.')
        return super().form_invalid(form)


class LoginUsuario(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def get_success_url(self):
        messages.success(self.request, 'Login exitoso.')
        return reverse('apps.usuario:usuario_list')


class LogoutUsuario(LogoutView):
    template_name = 'registration/logout.html'

    def get_success_url(self):
        messages.success(self.request, "¡Sesión cerrada correctamente!")
        return reverse('apps.usuario:login')


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
            Comentario.objects.filter(usuario=self.object).delete()
        if eliminar_posts:
            Post.objects.filter(autor=self.object).delete()
        messages.success(request, f'Usuario {self.object.username} eliminado correctamente')
        return self.delete(request, *args, **kwargs)
