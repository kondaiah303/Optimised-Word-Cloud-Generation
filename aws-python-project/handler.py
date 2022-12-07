from projectcode import *


def word_frequency_handler(request, context):
    payload = json.loads(request.get('body'))
    payload = payload.get('text')
    print("reached handler")
    return list_of_words_count(payload)








