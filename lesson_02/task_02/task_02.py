import json


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json', 'r', encoding='utf-8') as json_file:
        order_dict = json.load(json_file)
        print(order_dict)
        new_order = {
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date,
        }

        order_dict['orders'].append(new_order)
        print(order_dict)
        with open('orders.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(order_dict, indent=4, ensure_ascii=False))


order = ['Вобла', 2, 2300, 'user543', '16.02.2022']
write_order_to_json(order[0], order[1], order[2], order[3], order[4])
