from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from contact.models import Contact
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache



def index(request):
    if request.user.is_authenticated:
        contacts = Contact.objects.filter(show=True).order_by('-id')

        paginator = Paginator(contacts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)


        context = {
            'page_obj': page_obj,
            'site_title': 'Contatos - '
        }

        return render(
            request, 
            'contact/index.html',
            context
        )
    else:
        return render(request, 'global/login.html')
    
def my_contact(request):
    if request.user.is_authenticated:
        user = request.user
        contacts = Contact.objects.filter(show=True, owner=user).order_by('-id')

        paginator = Paginator(contacts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)


        context = {
            'page_obj': page_obj,
            'site_title': 'Contatos - ',
            'header_type': 'user_contact',
        }

        return render(
            request, 
            'contact/my_contact.html',
            context
        )
    else:
        return render(request, 'global/login.html')



def contact(request, contact_id):
    if request.user.is_authenticated:
        single_contact = get_object_or_404(Contact, pk=contact_id)

        contact_name = f'{single_contact.first_name} {single_contact.last_name}'

        context = {
            'contact': single_contact,
            'site_title': f'{contact_name} - '

        }

        return render(
            request, 
            'contact/contact.html',
            context
        )
    else:
        return render(request, 'global/login.html')
    

def search(request):
        if request.user.is_authenticated:
            search_value = request.GET.get('q', '').strip()

            if search_value == '':
                return redirect('contact:index')

            contacts = Contact.objects.filter(show=True)\
            .filter(
                    Q(first_name__icontains=search_value) |
                    Q(last_name__icontains=search_value) 
                    )\
            .order_by('-id')

            paginator = Paginator(contacts, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)


            context = {
                'page_obj': page_obj,
                'site_title': 'Contatos - '
            }

            return render(
                request, 
                'contact/index.html',
                context
    )
        else:
            return render(request, 'global/login.html')

    