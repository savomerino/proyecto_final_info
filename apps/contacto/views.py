from .forms import ContactoForm
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy



class ConctactoUsuario(CreateView):
    template_name = 'contacto/contacto.html'
    form_class = ContactoForm
    success_url = reverse_lazy('index')
    
    class ContactoUsuario(CreateView):
        template_name = 'contacto/contacto.html'
        form_class = ContactoForm
        success_url = reverse_lazy('apps.contacto:contacto')
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['request'] = self.request
            return context
        
        def from_valid(self, form):
            messages.success(self.request, 'Consulta enviada.')
            return super().form_valid(form)
        
#También debemos aclarar que esto es una
#vista de ejemplo muy básica. Si quieres
#hacer mejoras podrías usar el método “get_form_kwargs()” para pasar el request al
#formulario y así poder acceder al email del
#usuario autenticado si lo hay, también podrías sobrescribir el método “get_success_
#url()” para pasar el id del objeto creado al
#url de éxito y así poder mostrar los detalles del contacto o podrías usar el método
#“form_send_email()” para enviar el correo
#electrónico al destinatario y así separar la
#lógica de la vista del modelo.