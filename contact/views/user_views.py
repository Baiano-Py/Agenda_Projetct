from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required

def login(request):
    errors = {}
    if request.method == "GET":
        context = {'site_title': 'Contatos - '}

        return render(
            request, 
            'global/login.html',
            context
        )
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user == None:
        errors['login'] = 'Nome de usuario ou senha invalidas'

    
    if errors:
        return render(request, 'global/login.html', {'errors': errors})
        
    login_django(request, user)

    return redirect('contact:index')



def cadastro(request):
    errors = {}
    if request.method == "GET":
        context = {'site_title': 'Contatos - '}

        return render(
            request, 
            'global/cadastro.html',
            context
        )
    else:
        username = request.POST.get('username')
        email = request.POST.get('registerEmail')
        password = request.POST.get('registerPassword')
        confirm_password = request.POST.get('confirmPassword')


        if User.objects.filter(username=username).exists():
            errors['Username'] = 'Esse nome já esta sendo utilizado'
        
        if User.objects.filter(email=email).exists():
            errors['Email'] = 'Esse E-mail já foi registrado'


        if len(password) < 8:
            errors['Password'] = 'A senha precisa ter pelo menos 8 caracteres'

        if password != confirm_password:
            errors['Confirmpassword'] = 'As senhas não coincidem'

        if errors:
            return render(request, 'global/cadastro.html', {'errors': errors})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()   

        context = {'site_title': 'Contatos - '}
        return render(
            request, 
            'global/login.html',
            context
        )


def user_logout(request):
    logout(request)
    return redirect('contact:login')


def account(request):
        context = {'site_title': 'Contatos - '}
        return render(
            request, 
            'global/usuario/account.html',
            context
        )

def account_update(request):
    if request.method == 'POST':

        first_name = request.POST.get('First_Name')
        last_name = request.POST.get('Last_Name')
        email = request.POST.get('Email')


        user = request.user


        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        
        user.save()

        return redirect('contact:account')

    context = {'site_title': 'Contatos - '}
    return render(request, 'global/usuario/account_update.html', context)






def account_delete(request):
    confirmation = request.POST.get('confirmation', 'no')
    user = request.user

    if confirmation == 'yes':
        user.delete() 
        return redirect('contact:login')


    return render(
        request, 
        'global/usuario/account.html',
        {
            'confirmation': confirmation ,
        },
    )



def password_reset(request):

    if request.method == "POST":
        errors = {}

        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')


        if new_password != confirm_password:
            errors['password'] = 'As senhas são diferentes'
        elif not new_password or not confirm_password:
            errors['password'] = 'As senhas não podem estar vazia'
        elif len(new_password) < 8:
            errors['password'] = 'As senhas precisam ter mais de 8 caracteres'
        else:
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Atualiza a sessão do usuário
            return redirect('contact:account')  # Redireciona após alteração bem-sucedida


        context = {
            'errors': errors,
            'site_title': 'Contatos - ',
        }
        return render(request, 'global/usuario/password_reset.html', context)

    # Se a solicitação for GET, apenas renderize o template
    context = {'site_title': 'Contatos - '}
    return render(request, 'global/usuario/password_reset.html', context)


        