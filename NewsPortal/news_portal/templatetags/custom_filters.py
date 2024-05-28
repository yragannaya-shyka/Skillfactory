from django import template


register = template.Library()


FORBIDDEN_WORDS = ['редиска']


@register.filter()
def censor(value):
    if type(value) is str:
        for f_word in FORBIDDEN_WORDS:
            for word in value.split():
                if f_word in word.lower():
                    value = value.replace(word[0] + f_word[1:], word[0] + '*'*(len(f_word)-1))
        return f'{value}'
    else:
        return f'{value} ошибка типа данных.'
