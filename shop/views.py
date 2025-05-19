from django.shortcuts import render, redirect, get_object_or_404
from .models import SelectionBox, Cake, Order, OrderItem
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from decimal import Decimal

# SHOP VIEW – Displays available cakes and selection boxes.
def shop(request):
    selection_boxes = SelectionBox.objects.all()
    cakes = Cake.objects.all()
    
    cart = request.session.get("cart", [])
    print("Cart Session Data:", cart)

    # Calculate cart total
    cart_total = Decimal(0)
    for item in cart:
        try:
            price = Cake.objects.get(id=item["cake_id"]).price if item.get("cake_id") else SelectionBox.objects.get(id=item["box_id"]).price
            cart_total += price * item["quantity"]
        except (Cake.DoesNotExist, SelectionBox.DoesNotExist):
            continue

    return render(request, "shop/shop.html", {"selection_boxes": selection_boxes, "cakes": cakes, "cart": cart, "cart_total": cart_total})


# ADD TO CART – Stores selected items in session before checkout.
def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        item_type = request.POST.get("item_type")
        quantity = int(request.POST.get("quantity", 1))

        cart = request.session.get("cart", [])

        if item_type == "box" and SelectionBox.objects.filter(id=item_id).exists():
            item = SelectionBox.objects.get(id=item_id)
            cart.append({"box_id": item.id, "box_type": item.box_type, "quantity": quantity})
        elif item_type == "cake" and Cake.objects.filter(id=item_id).exists():
            item = Cake.objects.get(id=item_id)
            cart.append({"cake_id": item.id, "cake_type": item.cake_type, "quantity": quantity})

        request.session["cart"] = cart

    return redirect("shop")


# REMOVE FROM CART – Users can delete items from their cart before checkout.
def remove_from_cart(request, item_id):
    cart = request.session.get("cart", [])

    # Remove only first matching item to allow quantity adjustments instead of full deletion
    for item in cart:
        if str(item.get("cake_id") or item.get("box_id")) == str(item_id):
            cart.remove(item)
            break

    request.session["cart"] = cart
    return redirect("shop")


# SUBMIT ORDER – Processes the cart and submits the order.
@login_required  
def submit_order(request):
    if request.method == "POST":
        user = request.user

        order = Order.objects.create(
            user=user,
            email=user.email,
            pickup_time=datetime.now() + timedelta(hours=1)
        )

        total_price = Decimal(0)
        cart_items = request.session.get("cart", [])

        for item in cart_items:
            cake = Cake.objects.get(id=item["cake_id"]) if item.get("cake_id") else None
            box = SelectionBox.objects.get(id=item["box_id"]) if item.get("box_id") else None
            quantity = item["quantity"]

            OrderItem.objects.create(order=order, cake=cake, box=box, quantity=quantity)
            total_price += (cake.price if cake else box.price) * quantity

        order.total_price = total_price
        order.save()

        # Clear session cart after order submission
        request.session["cart"] = []

        return redirect("order_history")

    
# ORDER HISTORY – Displays user orders with modification and deletion options.
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).select_related("user").order_by("-created_at")
    return render(request, "shop/order_history.html", {"orders": orders, "now": datetime.now()})


# MODIFY ORDER – Allows users to update item quantities or remove items.
@login_required
def modify_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Prevent modification after pickup time
    if datetime.now() >= order.pickup_time:
        return redirect("order_history")

    if request.method == "POST":
        for item in order.orderitem_set.all():
            quantity = int(request.POST.get(f"quantity_{item.id}", item.quantity))
            
            if quantity == 0:
                item.delete()
            else:
                item.quantity = quantity
                item.save()

        if order.orderitem_set.count() == 0:
            order.delete()
        else:
            order.total_price = sum(item.quantity * (item.cake.price if item.cake else item.box.price) for item in order.orderitem_set.all())
            order.save()

        return redirect("order_history")

    return render(request, "shop/modify_order.html", {"order": order})


# DELETE ORDER – Only before pickup time.
@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if datetime.now() < order.pickup_time:
        order.delete()
    
    return redirect("order_history")