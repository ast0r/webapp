def search4vowels(word):
    """comment"""
    vowels = set('iuoae')    
    return vowels.intersection(set(word))


def search4letters(phrase:str, letters:str='aeiou')->set:
    """Поиск введнных букв"""    
    return set(letters).intersection(set(phrase))

