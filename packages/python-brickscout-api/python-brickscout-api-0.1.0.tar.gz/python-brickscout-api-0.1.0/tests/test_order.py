import sys, os

sys.path.append(os.getcwd() + '/..')

from brickscout.api import BrickScoutAPI


api = BrickScoutAPI(username='brickstarbelgium', password='Planten11$')

orders = api.orders.get_open_orders()

for order in orders.iterator():
    print(f'Order ID: {order.uuid}')
    
    order_shipping_cost = order.selectedOrderHandlingOption.shippingMethodCost.amount
    order_shipping_method = order.selectedOrderHandlingOption.shippingMethodName
    
    order_additional_cost = order.selectedOrderHandlingOption.paymentCost.amount
    order_tax_rate = order.taxRate
    
    print(f'Shipping cost with {order_shipping_method}: {order_shipping_cost} | Additional cost: {order_additional_cost} | Tax rate: {order_tax_rate}%')
    
    print('Items')
    print('-------')
    basket = order.basket
    
    for batch in basket.batches.iterator():
        for item in batch.items.iterator():
            name = item.name
            quantity = item.quantity
            currency = item.lineTotal.currency
            
            net_price = item.unitNetPrice.amount
            total_price = item.lineTotal.amount
            vat_amount = total_price - net_price
            vat_percentage = vat_amount / net_price * 100
            
            print(f'Item: {name} | Quantity: {quantity} | Total price: {total_price} {currency} | Net price: {net_price} {currency} | VAT: {vat_percentage}%')
    
    print('')