from django.shortcuts import render, redirect
from django.views.generic import View
from product.models import Product
from django.conf import settings
import json
import os
from .models import Contact
from django.contrib import messages


class Home(View):
    def get(self, request):
        latest_products = Product.objects.all().order_by('-created_at')[:8]  
        context = {
            'latest_products': latest_products
        }
        return render(request, 'home.html', context)


def dealer_list(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'data.json')

    dealers = []
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            dealers = json.load(f)
    except FileNotFoundError:
        print(f"Xəta: dealers.json faylı {json_file_path} yolunda tapılmadı")
    except json.JSONDecodeError:
        print(f"Xəta: {json_file_path} faylından JSON dekodlaşdırıla bilmədi")
    except Exception as e:
        print(f"Gözlənilməz xəta baş verdi: {e}")

    context = {
        'dealers': dealers,
        'page_title': 'Dilerlərin siyahısı (xaricdə)'
    }
    return render(request, 'dealer_list.html', context) 


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, "Mesajınız uğurla göndərildi!")
            return redirect('core:contact')
        else:
            messages.error(request, "Zəhmət olmasa, bütün xanaları doldurun.")

    return render(request, 'contact.html')
