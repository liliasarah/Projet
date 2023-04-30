from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import * 


@login_required
def add_to_wishlist(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    wishlist, created = Wishlist.objects.get_or_create(client=request.user.client, produit=produit)

    if created:
        messages.success(request, "Le produit a été ajouté à votre liste de souhaits.")
    else:
        messages.warning(request, "Ce produit est déjà dans votre liste de souhaits.")
    
    return redirect('Acceuil')


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(client=request.user.client)
    context = {'wishlist_items': wishlist_items}
    return render(request, 'wishlist.html', context)


@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Wishlist, id=item_id)
    item.delete()
    messages.success(request, "Le produit a été supprimé de votre liste de souhaits.")
    return redirect('wishlist')


def add_to_cart(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    cart, created = Cart.objects.get_or_create(client=request.user.client)
    cart_item, created = CartItem.objects.get_or_create(produit=produit, cart=cart)
    if not created:
        cart_item.quantite += 1
        cart_item.save()
    return redirect('cart')

def cart(request):
    cart, created = Cart.objects.get_or_create(client=request.user.client)
    cart_items = cart.cartitem_set.all()
    total = sum(item.produit.prix * item.quantite for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    if cart_item.cart.client.user == request.user:
        cart_item.delete()
    return redirect('cart')


