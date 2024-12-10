import os



class FileActions:
    def __init__(self, path: str):
        self.sheet = {}
        self.file_name = path
        with open(path, encoding='utf-8') as file:
            for line in file:
                key, value = line.strip().split('-')
                self.sheet[key.strip()] = float(value.strip())

    def validate(self):
        pass

    @staticmethod
    def add_new_data():
        name = input('Введите название продукта:')
        price = input('Введите цену продукта:')
        with open(name,'a', encoding='utf-8') as f:
            f.write(f'\n{name} - {price}')
        print(f'Продукт добавлен: {name} - {price}')

    def change_list(self):
        name = self._get_existing_name()
        if name:
            price = input('Введите цену продукта:')
            self.sheet[name] = float(price)
            self._commit()
            print(f'Продукт изменен: {name} - {price}')

    def delete(self):
        name = self._get_existing_name()
        if name:
            del self.sheet[name]
            self._commit()
            print(f'Продукт удален: {name}')

    def total(self):
        result = sum(list(self.sheet.values()))
        print(f'Сумма = {result}')

    def _commit(self):
        with open(self.file_name, 'wt', encoding='utf-8') as file:
            for key, value in self.sheet.items():
                file.write(f'{key} - {value}\n')


    def _get_existing_name(self):
        while True:
            name = input('Введите название продукта (пустая строка для отмены):\n')
            if not name:
                return ''
            if name not in self.sheet:
                print(f'Нет такого продукта! Имеются: {tuple(self.sheet.keys())}')
                continue
            return name



def main():

    path = input('Укажите путь к файлу:\n')
    action = input('Укажите действие')
    if not os.path.exists(path):
        print('File not found')
        return
    else:
        file_actions = FileActions(path)
        actions = {'Добавить': file_actions.add_new_data, 'Изменить': file_actions.change_list, 'Удалить': file_actions.delete,
                   'Сумма': file_actions.total}
        while True:
            separator_length = len(str(file_actions.sheet)) + 8
            print('=' * separator_length)
            print(f'Товары: {file_actions.sheet}')
            if not action:
                break
            if action not in actions:
                continue
            actions[action]()


if __name__ == '__main__':
    pass