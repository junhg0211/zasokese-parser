vowels = 'aeiouy'

acute = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú', 'y': 'ý'}
grave = {'a': 'à', 'e': 'è', 'i': 'ì', 'o': 'ò', 'u': 'ù'}
circumflex = {'a': 'â', 'e': 'ê', 'i': 'î', 'o': 'ô', 'u': 'û'}

acutes = ''.join(acute.values())
graves = ''.join(grave.values())
circumflexes = ''.join(circumflex.values())

inverse_circumflex = {v: k for k, v in circumflex.items()}

apostrophe_sets = [
    {'d', 't'},
    {'s', 'sh'},
    {'t', 's'},
    {'r', 'l'},
]


def get_apostrophe_set(word, *, start: bool) -> set:
    if not word:
        return set()

    if start:
        if word.startswith('sh'):
            phoneme = 'sh'
        else:
            phoneme = word[0]
    else:
        if word.endswith('sh'):
            phoneme = 'sh'
        else:
            phoneme = word[-1]

    result = set()
    for apostrophe_set in apostrophe_sets:
        if phoneme in apostrophe_set:
            result |= apostrophe_set

    return result


def remove_first_phoneme(word):
    if word.startswith('sh'):
        return word[2:]
    return word[1:]


def remove_last_phoneme(word):
    if word.endswith('sh'):
        return word[:-2]
    return word[:-1]


def uncircumflex(string):
    result = list(string)
    for i, letter in enumerate(result):
        if letter in inverse_circumflex:
            result[i] = inverse_circumflex[letter] * 2
    return ''.join(result)


class Word:
    @staticmethod
    def get(word: str, from_dictionary: dict):
        if word in from_dictionary:
            return Word(word, *from_dictionary[word])

    def __init__(self, word: str, noun: str = '', adjective: str = '', verb: str = '', adverb: str = '',
                 postposition: str = '', note: str = '', origin_language: str = '', origin_word: str = '',
                 proper_noun: bool = False):
        self.word = word
        self.noun = noun
        self.adjective = adjective
        self.verb = verb
        self.adverb = adverb
        self.postposition = postposition
        self.note = note
        self.origin_language = origin_language
        self.origin_word = origin_word
        self.proper_noun = proper_noun

    def __repr__(self):
        return ('(PN) ' if self.proper_noun else '') + self.word.upper()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.word == other
        else:
            return self.word == other.word

    def get_meaning(self):
        line = list()
        if self.noun:
            line.append(('고유' if self.proper_noun else '') + f'명. {self.noun}')
        if self.adjective:
            line.append(f'형. {self.adjective}')
        if self.verb:
            line.append(f'동. {self.verb}')
        if self.adverb:
            line.append(f'부. {self.adverb}')
        if self.postposition:
            line.append(f'조. {self.postposition}')
        if self.note:
            line.append(f'비. {self.note}')
        return '  '.join(line)


if __name__ == '__main__':
    print(uncircumflex('vistùqûll'))
