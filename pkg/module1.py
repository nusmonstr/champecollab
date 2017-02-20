from sys import exit
from random import randint


unassigned_log = 'unassigned_words.txt'
unassigned_words = []

class Scene(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}

    def enter(self):
        print('This scene is not yet configured. Subclass it and implement enter().')
        exit(1)

    def go(self, direction):
        return self.paths.get(direction, None)

    def add_paths(self, paths):
        self.paths.update(paths)


generic_death = Scene('death', 'You Died')
central_corridor = Scene('Central Corridor', 'This is the description of this room or scene')
laser_weapon_armory = Scene('Laser Weapon Armory', 'This is the description of this room or scene')
the_bridge = Scene('The Bridge', 'This is the description of this room or scene')
escape_pod = Scene('Escape Pod Area', 'This is the description of this room or scene')
the_end_winner = Scene('The End', 'This is the description of this room or scene')
the_end_loser = Scene('The End', 'This is the description of this room or scene')
central_corridor.add_paths({
    'shoot!': generic_death,
    'dodge' : generic_death,
    'tell a joke': laser_weapon_armory})
laser_weapon_armory.add_paths({
    '0132': the_bridge,
    '*' : generic_death})
the_bridge.add_paths({
    'throw the bomb': generic_death,
    'slowly place bomb' : escape_pod})
escape_pod.add_paths({
    '2': the_end_winner,
    '*' : the_end_loser})


class Engine(object):

    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        current_scene = self.scene_map.opening_scene()

        while True:
            print('\n---------')
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)

class Death(Scene):

    quips = [
        'You died. Sucks to suck!',
        'You lose.'
    ]

    def enter(self):
        print(Death.quips[randint(0,len(self.quips)-1)])
        exit(1)

class CentralCorridor(Scene):
    def enter(self):
        msg = '''The Gothons of planet Percal #25 have invaded your ship and destroyed
        your entire crew. You are the last surviving member and your last mission
        is to get the neutron bomb from the weapons armory, put it in the bridge, and blow
        up the ship after getting into an escape pod.

        You're running down the central corridor to the weapons armory when a Gothon
        jumps out, red scaly skin, dark grimy teeth, and evil clown costume. He's blocking
        the door to the armory and about to pull a weapon to blast you.'''

        print(msg)

        action = input('> ')

        if action == 'shoot!':
            print('You miss and he eats you.')
            return 'death'
        elif action == 'dodge':
            print('You\'re to slow for his blaster, you feel the hot searing pain in your side.')
            return 'death'
        elif action == 'tell a joke':
            print('While distracted by your poor Gothon speech, you pull blaster and get him.')
            return 'armory'
        else:
            print('Where are you going with this?')
            return 'central_corridor'

class WeaponArmory(Scene):
    def enter(self):
        msg = '''You dive roll into the armory and slam the door to close button.
        There's a keypad on the lock box where the neutron bomb is kept.
        If you get the code wrong 10 times, you will be electrocuted. The code is 3 digits.'''
        code = '{}{}{}'.format(randint(1,9),randint(1,9),randint(1,9))
        code = '123'
        guess = input('[keypad]> ')
        guesses = 0

        while guess != code and guesses < 10:
            print('BZZZZZZZEDD!')
            guesses += 1
            guess = input('[keypad]> ')

        if guess == code:
            print('The lock dings and pops open! You grab the neutron bomb and run to the bridge!')
            return 'bridge'
        else:
            print('BZZZZZZZEDD!')
            print('You feel a surge of electricty rock you and your vision cuts out.')
            return 'death'

class TheBridge(Scene):
    def enter(self):
        msg = '''You burst into the brige with bomb under arm.'''

        action = input('> ')

        if action == 'throw the bomb':
            print('In a panic you throw the bomb, at the moment of impact, you hear a large explosion.')
            return 'death'
        elif action == 'slowly place bomb':
            print('You gently set the bomb and then turn to run to the escape pod.')
            return 'escape_pod'
        else:
            print('Where are you going with this?')
            return 'bridge'

class EscapePod(Scene):
    def enter(self):
        msg = '''You find the escape pod room. There are 3 bays in front of you, but you realize
        the alert is sounding that 2 of the escape pods are malfunctioning. You know you must choose the right
        one fast because you have only moments before the neutron bomb will explode.'''

        good_pod = randint(1,3)
        guess = input('[pod #]> ')

        if int(guess) != good_pod:
            print('You jump into pod {} and pound on the eject button. As soon as the pod launches you')
            print('hear a very loud whirring sound as the sides of the pod implode crushing you.')
            return 'death'
        else:
            print('You jump into pod {} and pound on the eject button. As soon as the pod launches you')
            print(' peer out the view window to see the ship explode behind you. You win!')
            return 'finished'

class Victory(Scene):
    def enter(self):
        print('Seriously you won!')
        exit(0)


class Map(object):

    scenes = {
        'central_corridor' : CentralCorridor(),
        'armory' : WeaponArmory(),
        'bridge' : TheBridge(),
        'escape_pod' : EscapePod(),
        'death' : Death(),
        'finished' : Victory()
    }
    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        return Map.scenes.get(scene_name)

    def opening_scene(self):
        return self.next_scene(self.start_scene)

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

    a_map = Map('central_corridor')
    a_game = Engine(a_map)
    a_game.play()


    ## Alternatively
    START = central_corridor

if __name__ == "__main__":
    print('Called from if of "module1"')
    main()