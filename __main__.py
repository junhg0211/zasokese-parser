from copy import copy

from dictionary import dictionary, words_by_length, before_e_table
from util import vowels, acute, Word, grave, uncircumflex, graves, circumflexes, remove_first_phoneme, \
    get_apostrophe_set, remove_last_phoneme

j_word = Word.get('J', dictionary)
die_word = Word.get('die', dictionary)
que_word = Word.get('-ùque', dictionary)
de_word = Word.get('dé', dictionary)
eie_word = Word.get('éie', dictionary)
oie_word = Word.get('öie', dictionary)

log = False

# line = 'Aniskas nira!'
# line = 'Miros Quorsin. Quovizashùll felosh!'
# line = 'Dozirémicinéstara'
# line = 'Mashasorisic u, Jémicin da dotè.'
# line = 'Doic, ä Micinas Has da micè Ékupyl Süt u naputùll zamè.'
# line = "Zam svo aquè Émicinas Kupyl dutisùdull Süt lo devèia, Kupy da Sivy roy uagizè Éskil vizashè."
# line = "Semü da shainùie veshè Émicinas, Dis 'vofas Sivyl masha micùll Süt u naputè."
# line = "Sirosic, ä Sivyxs ol Goly roy uagiziksùll, " \
#        "Micinas Golyl 'aputùsua oh Öshéskie da dravià' tou tagùll Jíc l'oh ätè."
# line = 'Sirosicémog, Olégolys Ruintginümy roy uagizùll ä Micinas todè.'
# line = "J Sch krifàd lo Kadas dé Zasospikêruçel"
# line = 'Siro degro Shaia dé 1-les 2-les Tavlas vagìz e.'
# line = "Daditutaÿr die Media d'uatash ufas ä Liviavonnatio die Guo d'iksùm."
line = input()

words = line.replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace('"', '').split(' ')
original_words = copy(words)


def match_convert(term_):
    if term_.lower() in map(lambda x: x.lower(), dictionary.keys()):
        return Word(term_, *dictionary[term_])


for i, word in enumerate(words):
    # í -> éi
    for vowel in set(vowels) - {'e'}:
        word = word.replace(acute[vowel], f'é{vowel}')

    word = [word]
    # noinspection PyTypeChecker
    words[i] = word
    previous_word = original_words[i-1] if i else ''
    next_word = original_words[i+1] if i != len(original_words) - 1 else ''

    j = -1
    while j < len(word) - 1:
        j += 1
        term = word[j]
        log and print(word, j)

        if len(word) == 1 and term == 'J':
            log and print(1)
            word[j] = j_word
            continue

        if term == 'dé':
            log and print(2)
            word[j] = de_word
            continue

        if term == 'éie':
            log and print(2.5)
            word[j] = eie_word
            continue

        # make it proper noun if the before word is J
        if words[i - 1][0] in (j_word, die_word, eie_word, oie_word) and not isinstance(word[0], Word):
            log and print(3)
            if 'x' in term:
                before_word, after_word = term.split('x', 1)
                word[j:j+1] = [before_word, '-x', '=' + after_word]
            word[j] = Word(word[j], word[j], proper_noun=True)
            continue

        # split é
        if term.lower() != 'é' and 'é' in term.lower():
            log and print(4)
            a, later = term.lower().split('é', 1)
            word[j:j+1] = [a + '!', 'é', '!' + later]
            if '=!' in word:
                word.remove('=!')
            if '!' in word:
                word.remove('!')
            j -= 1
            continue

        # check if the word right before the é ends with vowels
        if term.endswith('!'):
            log and print(5)
            if term == '=!':
                word.remove(term)
                j -= 1
                continue

            if term[:-1] in before_e_table:
                zasok = before_e_table[term[:-1]]
            else:
                tmp = term
                if tmp.startswith('!'):
                    tmp = tmp[1:]
                try:
                    zasok = sorted(filter(lambda x: x.startswith(tmp[:-1]), words_by_length),
                                   key=lambda x: abs(len(uncircumflex(x)) - len(tmp) + 1))[0]
                except IndexError:
                    zasok = ''
            if zasok:
                word[j] = Word.get(zasok, dictionary)
                continue
            else:
                word[j] = term[:-1]

        # check if the word right after the é starts with h
        if term.startswith('!'):
            log and print(6)
            if 'h' + term[1:].lower() in dictionary:
                zasok = match_convert('h' + term[1:].lower())
                word[j] = zasok
                continue
            else:
                term = term[1:]

        # convert to word if the word is matched with one in the dictionary
        if zasok := match_convert(term.lower()):
            log and print(7)
            word[j] = zasok
            continue

        # startswith convert
        extra_e = 0
        if any(uncircumflex(term).lower().replace('-', '').startswith((the_word := zasok).lower())
               for zasok in map(lambda x: x[:-1] if x.endswith('que') or x.endswith('ie') else x, words_by_length)):
            log and print(9)
            the_word = uncircumflex(term)[:len(the_word)]
            if the_word.endswith('qu') or the_word.endswith('i'):
                extra_e = 1
                the_word += 'e'
            zasok = Word.get(the_word.lower() if the_word != "J'" else "J'", dictionary)
            after_word = uncircumflex(term)[len(zasok.word) - extra_e:]
            if any(a_grave in term for a_grave in (graves + circumflexes)) and after_word[0] in grave:
                after_word = grave[after_word[0]] + after_word[1:]
            word[j:j+1] = [zasok, '=' + after_word]

            if zasok.word == "J'":
                if 'x' in word[j+1]:
                    before_word, after_word = word[j+1].split('x', 1)
                    word[j+1:j+2] = [before_word, '-x', '=' + after_word]
                word[j+1] = Word(word[j+1][1:], word[j+1][1:], proper_noun=True)
                j += 1

            continue

        # abbreviated with apostrophe at the start
        previous_phoneme_set = get_apostrophe_set(previous_word, start=False)
        if term.startswith("'") \
            and any(term[1:].lower().startswith(remove_first_phoneme(the_word := zasok).lower())
                    for zasok in filter(lambda x: any(x.startswith(phoneme) for phoneme in previous_phoneme_set),
                                        words_by_length)):
            log and print(10)
            the_word = Word.get(the_word.lower(), dictionary)
            word[j:j+1] = [the_word, '=' + term[len(the_word.word):]]
            continue

        # abbreviated with apostrophe at the last
        last_phoneme_set = get_apostrophe_set(next_word, start=True)
        if term.endswith("'") and not term.startswith('=') \
                and any(term[:-1].lower().endswith(remove_last_phoneme(the_word := zasok).lower())
                        for zasok in filter(lambda x: any(x.endswith(phoneme) for phoneme in last_phoneme_set),
                                            words_by_length)):
            log and print(11)
            the_word = Word.get(the_word, dictionary)
            word[j] = the_word
            continue

        # mà-
        if any(term.lower().replace('-', '').startswith((the_word := zasok).lower())
               for zasok in map(lambda x: x[:-1], filter(lambda x: x.endswith('-'), words_by_length))):
            log and print(12)
            the_word = Word.get(the_word + '-', dictionary)
            word[j:j+1] = [the_word, term[len(the_word.word)-1:]]
            continue

        # only -ùque
        if uncircumflex(term).startswith('=ùqu'):
            log and print(13)
            if term == '=ùque':
                word[j] = que_word
            else:
                term = uncircumflex(term)
                word[j:j+1] = [que_word, '=' + grave[term[4]] + term[5:]]
            continue

        # -às
        if term.startswith('=') \
                and any(uncircumflex(term[1:].lower()).startswith((the_word := zasok)[1:].lower())
                        for zasok in filter(lambda x: x.startswith('-'), words_by_length)):
            log and print(14)
            the_word = Word.get(the_word, dictionary)
            back_word = term[len(the_word.word):]
            if back_word:
                if any(a_grave in back_word + term for a_grave in circumflexes + graves) and back_word[0] in grave:
                    back_word = grave[back_word[0]] + back_word[1:]
                word[j:j+1] = [the_word, '=' + back_word]
            else:
                word[j] = the_word
            continue

        # ê -> ée
        if 'ê' in term:
            log and print(15)
            word[j] = term.replace('ê', 'ée')
            j -= 1

        if term == '=':
            log and print(16)
            word.remove('=')
            j -= 1
            continue


if __name__ == '__main__':
    print(line)
    for i, terms in enumerate(words):
        word = original_words[i]
        print('\n', word, sep='')
        for term in terms:
            if isinstance(term, Word):
                print('', format(term.word, '10s'), term.get_meaning(), sep='\t')
            else:
                print(term)
