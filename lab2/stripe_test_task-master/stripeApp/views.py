import logging

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stripeApp import stripe_client, logic
from .models import Discount, Order

logger = logging.getLogger(__name__)


@api_view()
def create_session(request, order_id: int) -> Response:
    logger.info(f'[Заказ №{order_id}] Запрос на получение session_id')

    order_data = logic.get_order_data(order_id)
    if order_data is None:
        logger.error(f'[Заказ №{order_id}]  Ошибка получения информации по заказу')
        return Response(status=status.HTTP_404_NOT_FOUND)

    logger.info(f'[Заказ №{order_id}] Получена информация по заказу: {order_data}')

    session_id = stripe_client.create_session_api(order_data)
    if session_id is None:
        logger.error(f'[Заказ №{order_id}]  Ошибка получения id сессии')
        return Response(status=status.HTTP_404_NOT_FOUND)

    logger.info(f'[Заказ №{order_id}] Получен session_id: {session_id}')
    return Response({'id': session_id})


@api_view(["POST"])
def create_coupon(request) -> Response:
    amount = request.data["percent"]

    coupon_id = stripe_client.create_coupon_api(amount)

    if coupon_id is None:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        if amount // 100 != 0:
            output_amount = str(amount % 100) + '.' + str(amount // 100) + '%'
        else:
            output_amount = str(amount) + '%'
        new_discount = Discount.objects.create(amount=amount, coupon_id=coupon_id, output_amount=output_amount)
        new_discount.save()
    except Exception as e:
        logger.error(f'[Купон {coupon_id}] Ошибка сохранения в БД')
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    logger.info(f'Купон {coupon_id} создан')
    return Response(status=status.HTTP_201_CREATED)


@api_view()
def show_order_page(request, order_id: int) -> HttpResponse:
    order_data = logic.get_order_data(order_id)

    if order_data is None:
        logger.error(f'[Заказ №{order_id}]  Ошибка получения информации по заказу')
        return Response(status=status.HTTP_404_NOT_FOUND)

    logger.info(f'[Заказ №{order_id}] Получена информация по заказу: {order_data}')

    if order_data["coupon_id"] is None:
        percent = None
        logger.info(f'[Заказ №{order_id}] Cкидочный купон не применен')
    else:
        percent = Discount.objects.get(coupon_id=order_data["coupon_id"]).output_amount

        logger.info(f'[Заказ №{order_id}] Номер купона: {order_data["coupon_id"]}\nРазмер скидки: {percent}')

    ctx = {
        'order_id': order_id,
        'name': f'Заказ № {order_id}',
        'description': order_data['items'],
        'price': order_data['price'],
        'discount': percent
    }

    return render(request, "order.html", context=ctx)


@api_view()
def show_success_payment_page(request, order_id: int) -> HttpResponse:
    ctx = {
        'order_id': order_id
    }

    return render(request, "payment_success.html", context=ctx)


@api_view()
def show_order_list_page(request) -> HttpResponse:
    orders = Order.objects.all()
    orders_list = []

    for order in orders:
        orders_list.append(logic.get_order_data(order.id))

    ctx = {
        'orders_list': orders_list,
    }
    return render(request, "order_list.html", context=ctx)