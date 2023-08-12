from django import template


register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(text):
   new_text = text

   stop_list = [
      'text',
      'about'
         ]

   for bad in stop_list:
      new_text = new_text.replace(bad, bad[:1] + '*' * (len(bad) - 1))
      if type(bad) != str:
         raise TypeError('должна быть строка')
   return new_text
