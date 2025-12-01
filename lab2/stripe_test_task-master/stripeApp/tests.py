from django.test import TestCase, Client
from unittest.mock import patch
from stripeApp.models import Item, Order, Discount
from stripeApp import logic, stripe_client


class IntegrationTests(TestCase):
    def __init__(self):
        self.client = Client()

    def test_create_sample_order(self):
        i1 = Item.objects.create(title='T-shirt', price=1500) # 15.00
        i2 = Item.objects.create(title='Mug', price=750) # 7.50
        d = Discount.objects.create(coupon_id='coup_1', output_amount=10) # 10% off
        order = Order.objects.create(discount_coupon=d)
        order.items.add(i1, i2)
        order.save()

        return order


    def test_get_order_data_success(self):
        order = self.create_sample_order()
        data = logic.get_order_data(order.id)

        assert data is not None
        assert data['id'] == order.id
        assert any(item['title'] == 'T-shirt' for item in data['items'])

        assert data['num_price'] == 2250
        assert data['percent'] == 10


    def test_get_order_data_nonexistent(self):
        data = logic.get_order_data(999999)
        assert data is None


    def test_show_order_list_page_renders(self):
        order = self.create_sample_order()
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        self.assertIn('T-shirt', content)


    @patch('stripeApp.stripe_client.stripe')
    def test_create_coupon_api_success_and_failure(self, mock_stripe_module):

        mock_stripe_module.Coupon.create.return_value = {'id': 'cp_test_123'}
        new_id = stripe_client.create_coupon_api(25)
        self.assertEqual(new_id, 'cp_test_123')

        mock_stripe_module.Coupon.create.side_effect = Exception('stripe error')
        new_id2 = stripe_client.create_coupon_api(50)
        self.assertIsNone(new_id2)


    @patch('stripeApp.stripe_client.stripe')
    def test_create_session_api_success_and_exception(self, mock_stripe_module):
        order = self.create_sample_order()

        order_dict = logic.get_order_data(order.id)

        mock_stripe_module.checkout.Session.create.return_value = {'url': 'https://checkout.test/session/1'}
        url = stripe_client.create_session_api(order_dict)
        self.assertIsNotNone(url)
        assert url.startswith('https://')

        mock_stripe_module.checkout.Session.create.side_effect = Exception('network')
        url2 = stripe_client.create_session_api(order_dict)
        self.assertIsNone(url2)
