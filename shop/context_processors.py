import decimal

from shop.models import BasketItem, PromoCode


def basket_context(request):
    basket_items = BasketItem.objects.all()
    promo_codes = PromoCode.objects.all()
    total = 0

    # work out basket total
    for basket_item in basket_items:
        basket_item.price = basket_item.product.price
        basket_item.price *= basket_item.qty
        total += basket_item.price

    # find and apply active promo code (if one exists)
    active_promo_code = False
    promo_codes = PromoCode.objects.all()
    for promo_code in promo_codes:
        if promo_code.active:
            active_promo_code = True
            if promo_code.discount_type == '%':
                percent_change = 1 - (promo_code.discount_amount * 0.01)
                for basket_item in basket_items:
                    basket_item.discount_price = round(
                        basket_item.price * decimal.Decimal(float(percent_change)), 2
                    )
                    basket_item.save()
            elif promo_code.discount_type == '-':
                for basket_item in basket_items:
                    basket_item.discount_price = basket_item.price - promo_code.discount_amount

    if active_promo_code:
        discount_total = 0
        for basket_item in basket_items:
            discount_total += basket_item.discount_price
    else:
        discount_total = total
        for basket_item in basket_items:
            basket_item.discount_price = basket_item.price

    return {
        'total': total,
        'discount_total': discount_total,
        'basket_count': basket_items.count()
    }
