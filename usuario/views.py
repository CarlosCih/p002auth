from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# funcion para el manejo de la logica de inicio de sesion de usuario
def user_login(request):
    # verifica si el metodo de la solicitud es POST
    if request.method == 'POST':
        form = LoginForm(request.POST)
        #Valida el formulario
        if form.is_valid():
            cd = form.cleaned_data #Limpia los datos ingresados
            user = authenticate(request, username=cd['username'], password=cd['password'])
            #verifica si el usuario existe
            if user is not None:
                #verifica si el usuario se encuentra activo
                if user.is_active:
                    login(request,user)
                    return HttpResponse("Usuario autentificado correctamente")
                else:
                    return HttpResponse("Cuenta deshabilitada")
            else:
                return HttpResponse("Usuario no encontrado")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

#vista para cargar el dashboard despues de iniciar sesion
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

