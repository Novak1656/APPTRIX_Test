from django.template import Library

register = Library()


@register.filter
def read_news_data(news_data: dict, key: str) -> str:
    data = news_data.get(key)
    if key == 'publishedAt':
        return data.replace('T', ' ').replace('Z', '')
    return data
