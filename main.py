import json
import requests
import urlextract


def get_links() -> list:
    """
    Принимает многострочный текст на вход, для извлечения ссылок из него. При вводе пустой строки он прерывается.
    Использует библиотеку urlextract
    :param path: Путь к текстовому файлу
    :return: Список строк(ссылок)
    """
    # # Читаем входящие строки
    strings = "\n".join(iter(input, ""))

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
    :param links: список ссылок
    :return: json файл с доступными методами
    """
    # Словарь проверяемых методов
    methods = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put,
        'DELETE': requests.delete,
        'HEAD': requests.head,
        'OPTIONS': requests.options
    }

    res = {}

    for link in links:
        res[link] = {}
        for method in methods:
            r = methods[method](link)
            if r.status_code != 405:
                res[link][method] = r.status_code

    js = json.dumps(res, indent=4)
    return js


if __name__ == '__main__':
    lst = get_links()
    print(lst)
    result = get_links_allow_methods(lst)

    print(result)
