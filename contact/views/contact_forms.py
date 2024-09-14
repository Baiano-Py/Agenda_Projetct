from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from contact.forms import ContactForm
from contact.models import Contact



def create(request):    
    if request.user.is_authenticated:
        form_action = reverse('contact:create')

        if request.method == 'POST':
            form = ContactForm(request.POST, request.FILES)

            context = {
                'form': form,
                'form_action': form_action,
                'button_text': 'Create Contact'
            }

            if form.is_valid():
                contact = form.save(commit=False)
                contact.owner = request.user
                contact.save()
                return redirect('contact:index')

            return render(
                request, 
                'contact/create.html',
                context
            )

        context = {
            'form': ContactForm(),
            'form_action': form_action,
            'button_text': 'Create Contact'
        }

        return render(
            request, 
            'contact/create.html',
            context
        )
    else:
        return redirect('contact:login')


def update(request, contact_id): 
    if request.user.is_authenticated:
        contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)   
        form_action = reverse('contact:update', args=(contact_id,))

        if request.method == 'POST':
            form = ContactForm(request.POST, request.FILES, instance=contact,)

            context = {
                'form': form,
                'form_action': form_action,
                'button_text': 'Save'
            }

            if form.is_valid():
                contact = form.save()
                return redirect('contact:index',)

            return render(
                request, 
                'contact/create.html',
                context
            )

        context = {
            'form': ContactForm(instance=contact),
            'form_action': form_action,
            'button_text': 'Save'
        }

        return render(
            request, 
            'contact/create.html',
            context
        )
    else:
        return render(request, 'global/login.html')


def delete(request, contact_id): 
    if request.user.is_authenticated:
        contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)

        confirmation = request.POST.get('confirmation', 'no')

        if confirmation == 'yes':
            contact.delete() 
            return redirect('contact:my_contact')


        return render(
            request, 
            'contact/contact.html',
            {
                'contact': contact,
                'confirmation': confirmation ,
            },
        )
    else:
        return render(request, 'global/login.html')
