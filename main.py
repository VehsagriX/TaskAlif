import argparse
import os
from literal import FILE_NOT_FOUND, ITEM_NOT_IN_LIST


class Products:
    def __init__(self, path: str):
        self.path = path
        self.products = {}

    def __enter__(self):
        self.load_products()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_products()

    def load_products(self) -> None:
        if not os.path.isfile(self.path):
            raise FileNotFoundError(FILE_NOT_FOUND.format(path = self.path))

        with open(self.path, encoding='utf-8') as f:
            for line in f:
                item = line.replace('\n', '')
                item = item.replace(' ', '')
                if len(item) > 0:
                    key, value = item.split('-')

                self.products[key.strip().lower()] = float(value.strip())
        print(self.products)
        return

    def save_products(self) -> None:
        if self.products:
            with open(self.path, 'w', encoding='utf-8') as f:
                for key, value in self.products.items():
                    f.write(f'{key.title()} - {value}\n\n')

    def show_products(self):
        print(f'Cписок названий продуктов {tuple(self.products.keys())}')

    def add_new_item(self, name: str, price: float):
        self.products[name] = price
        print(f'Успешно добавлено')


    def change_some_item(self, name: str, new_value: float):
        if name not in self.products:
            raise KeyError(ITEM_NOT_IN_LIST.format(name=name))

        self.products[name] = new_value
        print(f'Значение успешно изменено')

    def del_some_item(self, name: str) -> None:
        if name not in self.products:
            raise KeyError(ITEM_NOT_IN_LIST.format(name=name))
        del self.products[name]
        print(f'Продукт успешно удален')


    def show_sum_price(self):
        return sum(self.products.values())


def add(products: Products, arg):
    name_product = input('Введите название продукта:\n')
    price = input('Введите цену:\n')
    if not price.isdigit():
        print('Вы указали не верную ценну, пожалуйста введите верные данные')
        add(products, arg)
        return

    return products.add_new_item(name_product.lower(), float(price))


def delete(products: Products, arg):
    products.show_products()
    name_product = input('Введите продукт который вы хотите удалить:\n')
    return products.del_some_item(name_product.lower())


def change(products: Products, arg):
    product = input('Введите название продукта, цену которого хотите изменить\n')
    price = input('Введите новое значение\n')
    if not price.isdigit():
        print('Вы указали не верную ценну, пожалуйста введите верные данные')
        change(products, arg)
        return
    products.change_some_item(product.lower(), float(price))


def show_amount(products: Products, args):
    return products.show_sum_price()


def main():
    parser = argparse.ArgumentParser(
        description="""Это помощник с работой со списком продуктов. Команды доступные: add, amount, change, delete""")

    parser.add_argument('path', help='Путь к файлу со списком продукций')

    subparsers = parser.add_subparsers(title="Commands", description="""Указать путь и выберите из команд: 
                                                                        добавить продукт-add,
                                                                        удалить продукт-delete, для вывода суммы-amount,
                                                                        изменить цену-change""",
                                       help="Укажите путь к файлу и одну из действий")
    # Add command
    parser_add = subparsers.add_parser('add',
                                       help='Добавляет новый продукт в список')

    parser_add.set_defaults(func=add)

    # Delete command
    parser_delete = subparsers.add_parser('delete', help='Удаляет продукт по заданному названию')
    parser_delete.set_defaults(func=delete)

    # Search command
    parser_search = subparsers.add_parser('amount', help='Выводит сумму продуктов из списка')

    parser_search.set_defaults(func=show_amount)

    # Change command
    parser_change = subparsers.add_parser('change', help='Изменяет цену какого-либо продукт')

    parser_change.set_defaults(func=change)

    args = parser.parse_args()
    print(args)
    if hasattr(args, 'func'):
        with Products(args.path) as products:
            print(args.func(products, args))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
