def cart_context(request):
    cart = request.session.get("cart", [])
    total_price = sum(
        item.get("box_price", 0) * item["quantity"] if "box_price" in item else
        item.get("cake_price", 0) * item["quantity"] if "cake_price" in item else 0
        for item in cart
    )

    return {"cart": cart, "cart_total": total_price}