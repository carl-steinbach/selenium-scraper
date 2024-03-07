from pprint import pprint

from bs4 import BeautifulSoup


def print_local_html(html, tag_name, class_name):
    soup = BeautifulSoup(html, "html.parser")
    result = soup.find(tag_name, {"class": class_name})
    print(
        f"-------------------------------------[ result for <{tag_name} class='{class_name}'> "
        f"]-------------------------------------")
    pprint(result)
