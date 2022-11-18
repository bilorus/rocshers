import json
import requests
import urlextract


def get_links() -> list:
    """
    Принимает многострочный текст на вход, для извлечения ссылок из него. При вводе пустой строки он прерывается.
    Использует библиотеку urlextract для выделения ссылок из текста.
    :param path: Путь к текстовому файлу
    :return: Список строк(ссылок)
    """
    # Читаем входящие строки
    print('Введите строки для обработки. Введите пустую строку и нажмите "enter" для начала выполнения скрипта')
    strings = "\n".join(iter(input, ""))
    print('Ожидайте...')

    # Собираем список ссылок из строк
    links = []
    extractor = urlextract.URLExtract()
    for i, string in enumerate(strings.split('\n')):
        url = extractor.find_urls(string)
        if url:
            links.append(*url)
        else:
            print(f'Строка {i}: {string.strip()} не является ссылкой')
    return links


def get_links_allow_methods(links: list) -> json:
    """
    Принимает на вход список ссылок, проверяет какие методы доступны по ссылке (код ответа != 405) из словаря methods,
    делая запросы с помощью библиотеки requests
    :param links: список ссылок (list['str'..])
    :return: json файл с доступными методами
    """
    # Словарь проверяемых методов
    methods = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put,
        'DELETE': requests.delete,
        'HEAD': requests.head,
        'OPTIONS': requests.options,
        'PATCH': requests.patch
    }

    result = {}

    for link in links:
        result[link] = {}
        for method in methods:
            response = methods[method](link)
            if response.status_code != 405:
                result[link][method] = response.status_code

    js = json.dumps(result, indent=4)
    return js


if __name__ == '__main__':
    lst = get_links()
    result = get_links_allow_methods(lst)

    print(result)
