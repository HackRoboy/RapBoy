
def prepare_text(text):
    if text[-1]=='.':
        return text
    elif text[-1] in [',', '/', ')']:
        return text[:-1]+'.'
    else:
        return text + '.'