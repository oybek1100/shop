from django.shortcuts import render , get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product, Category   , OrderDetail , Comment
from .forms import OrderForm , ProductForm , CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg 
from decimal import Decimal
from django.core.paginator import Paginator




def index(request, category_id=None):
    categories = Category.objects.all()
    search_query = request.GET.get('search')
    
    # Dastlab barcha mahsulotlar
    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)  #

    if search_query:
        products = products.filter(name__icontains=search_query)  
    
    # Rating
    products = products.annotate(avg_rating=Avg('comments__rating')).order_by('-avg_rating')



    # Paginator
    paginator = Paginator(products, 8)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number) 

    # Context
    context = {
        'products': page_obj,  
        'categories': categories,
        'page_obj': page_obj
    }
    return render(request, 'shop/home.html', context)



def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        related_products = Product.objects.filter(category = product.category).exclude(id=product_id)
        context = {
            'product': product,
            'related_products': related_products
        }
        return render(request, 'shop/detail.html' , context = context)
    except Product.DoesNotExist:
        return render(request, '')
    


def order_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = OrderForm()
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            
            # Narxni to'g'ri formatga o'tkazish
            try:
                if hasattr(product.price, '__iter__'):  # Tuple yoki list bo'lsa
                    product_price = Decimal(str(product.price[0]))
                else:
                    product_price = Decimal(str(product.price))
            except (TypeError, ValueError, IndexError) as e:
                messages.error(request, f'Narx formatida xatolik: {str(e)}')
                return render(request, 'shop/order_detail.html', {
                    'product': product,
                    'form': form
                })
            
            if product.quantity < order.quantity:
                messages.error(request, 'Siz so‘ragan mahsulot miqdori yetarli emas')
            else:
                product.quantity -= order.quantity
                product.save()
                
                order.total_price = product_price * Decimal(str(order.quantity))
                order.save()
                
                messages.success(request, 'Sizning buyurtmangiz qabul qilindi')
                return redirect('shop:product_detail', product_id=product.id)
    
    return render(request, 'shop/order_detail.html', {
        'product': product,
        'form': form
    })

def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, 'Mahsulot muvaffaqiyatli qo‘shildi')
            return redirect('shop:index')
    context = {
        'form': form
    }
    return render(request, 'shop/add_product.html', context)


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.add_message(
            request, messages.SUCCESS, 'Mahsulot muvaffaqiyatli o‘chirildi')
        return redirect('shop:index')
    return render(request, 'shop/delete_product.html', {'product': product})


def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, 'Mahsulot muvaffaqiyatli yangilandi')
            return redirect('shop:index')
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'shop/update_product.html', context)


def add_comment(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_text = request.POST.get('comment')
        rating = request.POST.get('rating')

        if name and email and comment_text:
            Comment.objects.create(
                product=product,
                name=name,
                email=email,
                comment=comment_text,
                rating=rating 
            )
            messages.success(request, "Comment added successfully!")
        else:
            messages.error(request, "Fill all fields!")
        
        return redirect('shop:product_detail',   product_id=product.id)
    
    return render('')


def expensive_product(request):
    products = Product.objects.order_by('-price')
    return render(request, 'shop/home.html', {'products': products})

def cheap_product(request):
    products = Product.objects.order_by('price')
    return render(request, 'shop/home.html', {'products': products})











    
       