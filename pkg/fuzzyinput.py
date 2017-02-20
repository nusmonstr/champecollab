unassigned_log = 'unassigned_words.txt'
unassigned_words = []
direction_words = ['north', 'south', 'east', 'west', 'down', 'up', 'left', 'right', 'back']
verbs = ['go', 'stop', 'kill', 'shoot', 'stop', 'turn', 'head']
nouns = ['door', 'bear', 'princess', 'cabinet']


def convert_numbers(s):
    try:
        return int(s)
    except ValueError:
        return None


def sentence_breakdown():
    stuff = input('> ').lower()
    words = stuff.split()
    sentence = []
    for word in words:
        if word in direction_words:
            sentence.append(('direction', word))
        elif word in verbs:
            sentence.append(('verb', word))
        elif word in nouns:
            sentence.append(('noun', word))
        elif convert_numbers(word):
            sentence.append(('number', convert_numbers(word)))
        else:
            try:
                int(word)
                print('Number is {}'.format(int(word)))
            except:
                pass
            sentence.append(('unassigned', word))
    unassigned_words.extend([y for x,y in sentence if x == 'unassigned'])
    return sentence


def text2int(textnum, numwords={}):
    if not numwords:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):  numwords[word] = (1, idx)
        for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

    ordinal_words = {'first': 1, 'second': 2, 'third': 3, 'fifth': 5, 'eighth': 8, 'ninth': 9, 'twelfth': 12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]

    textnum = textnum.replace('-', ' ')

    current = result = 0
    for word in textnum.split():
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)

            if word not in numwords:
                raise Exception("Illegal word: " + word)

            scale, increment = numwords[word]

        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


class ParserError(Exception):
    pass


class Sentence(object):
    def __init__(self, subject, verb, object):
        self.subject = subject[1]
        self.verb = verb[1]
        self.object = object[1]


def peek(word_list):
    if word_list:
        word = word_list[0]
        return word[0]
    else:
        return None


def match(word_list, expecting):
    if word_list:
        word = word_list.pop(0)

        if word[0] == expecting:
            return word
        else:
            return None
    else:
        return None


def skip(word_list, word_type):
    while peek(word_list) == word_type:
        match(word_list, word_type)


def parse_verb(word_list):
    skip(word_list, 'unassigned')

    if peek(word_list) == 'verb':
        return match(word_list, 'verb')
    else:
        raise ParserError('Expected a verb next.')


def parse_object(word_list):
    skip(word_list, 'unassigned')
    next = peek(word_list)

    if next == 'noun':
        return match(word_list, 'noun')
    if next == 'direction':
        return match(word_list, 'direction')
    else:
        raise ParserError('Expected a noun or direction next.')


def parse_subject(word_list, subj):
    verb = parse_verb(word_list)
    obj = parse_object(word_list)

    return Sentence(subj, verb, obj)


def parse_sentence(word_list):
    skip(word_list, 'unassigned')
    start = peek(word_list)

    if start == 'noun':
        subj = match(word_list, 'noun')
        return parse_subject(word_list, 'subj')
    elif start == 'verb':
        # assume the subject is the player then
        return parse_subject(word_list, ('noun', 'player'))
    else:
        raise ParserError('Must start with subject, object, or verb not: {}.'.format(start))


def main():
    print(sentence_breakdown())
    print(text2int('one hundred'))
    with open(unassigned_log, 'a') as save_for_later:
        for word in unassigned_words:
            save_for_later.write(word+'\n')

if __name__ == "__main__":
    print('Called from if of "module1"')
    main()