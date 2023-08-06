def apply_discount(original_price, discount_percentage):
    discount_amount = original_price * (discount_percentage / 100)
    discounted_price = original_price - discount_amount
    return discounted_price
