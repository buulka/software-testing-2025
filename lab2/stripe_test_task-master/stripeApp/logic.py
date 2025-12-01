import logging

from django.core.exceptions import ObjectDoesNotExist

from stripeApp.models import Order

logger = logging.getLogger(__name__)


def get_order_data(order_id: int) -> dict | None:
    try:
        order = Order.objects.get(id=order_id)
        order_sum = 0
        items = []

        for item in order.items.all():
            order_sum += item.price
            items.append({'name': item.name,
                          'price': item.price,
                          'output_price': f'{item.price // 100}.{item.price % 100} руб.'
                          })
        if order.discount_coupon is not None:
            coupon_id = order.discount_coupon.coupon_id
            percent = order.discount_coupon.output_amount
        else:
            coupon_id = None
            percent = None

        order_output_price = f'{order_sum // 100}.{order_sum % 100} руб.'
        return {'id': order_id, 'items': items, 'num_price': order_sum, 'price': order_output_price, 'coupon_id': coupon_id, 'percent': percent}
    except ObjectDoesNotExist:
        logger.error(f'[Заказ №{order_id}] Заказа №{order_id} не существует')
        return None
    except Exception as e:
        logger.error(f'[Заказ №{order_id}]', exc_info=e)
        return None
