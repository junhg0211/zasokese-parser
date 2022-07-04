import csv


dictionary = dict()

with open('res/Krispikasévapy - 자소크어.csv', newline='', encoding='utf-8') as file:
    spam_reader = csv.reader(file)
    for row in spam_reader:
        if row[0] == '단어':
            continue
        if row[0].startswith('('):
            continue
        dictionary[row[0]] = row[1:]

words_by_length = sorted(dictionary.keys(), key=len, reverse=True)

before_e_table = dict()

with open('res/before_e_table.csv', newline='') as file:
    spam_reader = csv.reader(file)
    for row in spam_reader:
        before_e_table[row[0]] = row[1]


if __name__ == '__main__':
    from pprint import pprint
    pprint(dictionary)
    print(dictionary['j'])
