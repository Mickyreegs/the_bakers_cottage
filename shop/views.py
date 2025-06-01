from django.shortcuts import render, redirect, get_object_or_404
from .models import SelectionBox, Cake, Order, OrderItem
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.utils.timezone import now
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse


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
            cart.append({
                "box_id": item.id,
                "box_type": item.box_type,
                "box_price": float(item.price),
                "quantity": quantity
            })
        elif item_type == "cake" and Cake.objects.filter(id=item_id).exists():
            item = Cake.objects.get(id=item_id)
            cart.append({
                "cake_id": item.id,
                "cake_type": item.cake_type,
                "cake_price": float(item.price),
                "quantity": quantity
            })

        request.session["cart"] = cart

        request.session["cart_total"] = float(sum(
            item.get("box_price", 0) * item["quantity"] if "box_price" in item else
            item.get("cake_price", 0) * item["quantity"] if "cake_price" in item else 0
            for item in cart
        ))

        request.session.modified = True
        request.session.save()

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
        cart_items = request.session.get("cart", [])

        #Prevent empty order submission before creating the order
        if not cart_items:
            messages.error(request, "Your cart is empty! Please add items before submitting.")
            return redirect("shop")

        user = request.user
        order = Order(user=user, email=user.email)  
        order.save()

        total_price = Decimal(0)

        for item in cart_items:
            cake = Cake.objects.filter(id=item.get("cake_id")).first()
            box = SelectionBox.objects.filter(id=item.get("box_id")).first()
            quantity = item["quantity"]

            if cake or box:
                OrderItem.objects.create(
                    order=order,
                    item_type="cake" if cake else "box",
                    item_id=cake.id if cake else box.id,
                    name=cake.cake_type if cake else box.box_type,
                    price=cake.price if cake else box.price,
                    quantity=quantity
                )
                total_price += (cake.price if cake else box.price) * quantity

        order.total_price = total_price
        order.save()

        request.session["cart"] = []
        request.session["cart_total"] = 0
        request.session.modified = True

        messages.success(request, "Order submitted successfully!")

    return redirect("shop")

    
# ORDER HISTORY – Displays user orders with modification and deletion options.
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).annotate(item_count=Count("order_items")).filter(item_count__gt=0)
    orders = orders.select_related("user").order_by("-created_at")
    
    return render(request, "shop/order_history.html", {"orders": orders, "now": now()})


# MODIFY ORDER – Allows users to update item quantities or remove items.
@login_required
def modify_order(request, order_id):
    order = Order.objects.filter(id=order_id, user=request.user).first()

    if not order:
        messages.warning(request, "This order no longer exists.")
        return redirect("order_history")

    # Prevent modification after pickup time
    if now() >= order.pickup_time:
        messages.warning(request, "You can no longer modify this order.")
        return redirect("order_history")

    if request.method == "POST":
        remove_item_id = request.POST.get("remove_item")

        if remove_item_id:
            item_to_remove = order.order_items.filter(id=remove_item_id).first()
            if item_to_remove:
                item_to_remove.delete()
                messages.success(request, "Item removed successfully!")
            else:
                messages.error(request, "Item not found or already removed.")
        else:
            for item in order.order_items.all():
                try:
                    quantity = int(request.POST.get(f"quantity_{item.id}", item.quantity))
                    if quantity <= 0:
                        item.delete()
                    else:
                        item.quantity = quantity
                        item.save()
                except ValueError:
                    messages.error(request, "Invalid quantity entered.")

            messages.success(request, "Order updated successfully!")

        if not order.order_items.exists():
            order.delete()
            messages.success(request, "Order deleted successfully!")
            return redirect("order_history")
        
        order.total_price = sum(item.quantity * item.price for item in order.order_items.all())
        order.save()

        return redirect("order_history")

    return render(request, "shop/modify_order.html", {"order": order})


# DELETE ORDER – Only before pickup time.
@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if now() < order.pickup_time:
        order.delete()
    
    return redirect("order_history")