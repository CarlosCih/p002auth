from django.shortcuts import redirect, render
from django.contrib import messages
from usuario.models import Profile
from .forms import LoginForm, ProfileEditForm, UserEditForm, UserRegistrationForm
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

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #Se cre un nuevo objeto de usuario sin guardarlo aun en la base de datos
            new_user = user_form.save(commit=False)
            #Se encripta la contraseña proporcionada por el usuario
            new_user.set_password(user_form.cleaned_data['password'])
            #Se guarda el usuario en la base de datos
            new_user.save()
            #Se crea el perfil de usuario asociado al nuevo usuario
            Profile.objects.create(user=new_user)
            #Se renderiza la plantilla html del registro exitoso
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
            #Si el formulario no es valido, se vuelve a mostrar el formulario con los errores
            user_form = UserRegistrationForm()
        #Se renderiza la plantilla html del formulario de registro
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado correctamente', extra_tags='success')
        else:
            messages.error(request, 'Error al actualizar el perfil', extra_tags='danger')
    else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
    