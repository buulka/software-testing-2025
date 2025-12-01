import logging
import os

import stripe

from stripeTestTask import settings

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_KEY


def create_session_api(order: dict) -> str | None:
    line_items = [{
        'price_data': {
            'currency': 'rub',
            'product_data': {
                'name': f'Заказ № {order["id"]}',
            },
            'unit_amount': order["num_price"],
        },
        'quantity': 1,
    }]
    mode = 'payment'
    success_url = f'http://{os.environ.get("HOST")}/payment_success/{order["id"]}'
    cancel_url = f'http://{os.environ.get("HOST")}/'

    try:
        if order["coupon_id"] is not None:
            return stripe.checkout.Session.create(
                line_items=line_items,
                mode=mode,
                discounts=[{
                    'coupon': order["coupon_id"],
                }],
                success_url=success_url,
                cancel_url=cancel_url,
            )["id"]

        return stripe.checkout.Session.create(
            line_items=line_items,
            mode=mode,
            success_url=success_url,
            cancel_url=cancel_url
        )["id"]
    except Exception as e:
        logger.error(f'[Заказ №{order["id"]} Ошибка создания сессии', exc_info=e)
        return None


def create_coupon_api(percent: int) -> str | None:
    try:
        return stripe.Coupon.create(
            percent_off=str(percent % 100) + '.' + str(percent // 100),
            duration="forever"
        )['id']
    except Exception as e:
        logger.error(f'Ошибка запроса на создание купона', exc_info=e)
        return None
