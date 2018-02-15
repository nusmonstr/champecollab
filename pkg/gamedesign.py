from sys import exit
from random import randint

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


class Engine(object):
    level_dic={'a':'easy','b':'normal','c':'hard'}
    print('Choose your difficulty level.')
    for option in level_dic:
        print(option,') ', level_dic[option])
    while True:
        level = input('> ')
        if level in level_dic:
            print('You\'ve chosen ',level_dic[level],' mode.')
            break
        else:
            print('Please choose a, b, or c')

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
        'You lose.',
        'Dumb Idiot.',
        'An infant could have done better than that.'
    ]

    def enter():
        print(Death.quips[randint(0, len(Death.quips)-1)])
        input()
        exit(1)


class CentralCorridor(Scene):
    def enter():
        msg = '''The Gothons of planet Percal #25 have invaded your ship and destroyed
        your entire crew. You are the last surviving member and your last mission
        is to get the neutron bomb from the weapons armory, put it in the bridge, and blow
        up the ship after getting into an escape pod.

        You're running down the central corridor to the weapons armory when a Gothon
        jumps out, red scaly skin, dark grimy teeth, and evil clown costume. He's blocking
        the door to the armory and about to pull a weapon to blast you.'''
        print(msg)
        options_dic={'a':'shoot!','b':'dodge','c':'tell a joke','d':'pee yourself'}
        print('Choose your next action.')
        for option in options_dic:
            print(option,') ', options_dic[option])
        action = input('> ')
       
        if action == 'a':
            print('You miss and he eats you.')
            return 'death'
        elif action == 'b':
            print('You\'re to slow for his blaster, you feel the hot searing pain in your side.')
            return 'death'
        elif action == 'c':
            print('While distracted by your poor Gothon speech, you pull blaster and get him.')
            return 'keypad'
        elif action == 'd':
            print('The stench of your incontinence scares the monster away.')
            return 'keypad'
        else:
            print('Where are you going with this?')
            return 'central_corridor'


class WeaponArmory(Scene):
    def enter():
        msg = '''You dive roll into the armory and slam the door to close button.
        There's a keypad on the lock box where the neutron bomb is kept.
        If you get the code wrong 10 times, you will be electrocuted. The code is 3 digits.'''
        return 'keypad'
    
class Keypad(Scene):
    code = '{}{}{}'.format(randint(0,9),randint(0,9),randint(0,9))
    def enter():
        from sys import exit
        from random import randint

        msg = '''You dive roll into the armory and slam the door to close button.
        There's a keypad on the lock box where the neutron bomb is kept.
        If you get the code wrong 10 times, you will be electrocuted. The code is 3 digits.'''
        print(msg)
        #code = '{}{}{}'.format(randint(0,9),randint(0,9),randint(0,9))
        guess = input('[keypad entry]> ')
        guesses = 1
        reply=['','','']
        while guess != Keypad.code and guesses < 10:
            counter=0
            if Engine.level=='a':
                for digit in Keypad.code:
                    reply[counter]=abs(int(digit)-int(guess[counter]))
                    counter+=1
                print('The keypad gives you back something... ',reply[0],reply[1],reply[2])
            elif Engine.level=='b':
                for digit in Keypad.code:
                    if digit==guess[counter]:
                        reply[counter]='1'
                    else:
                        reply[counter]='0'
                    counter+=1
                print('The keypad gives you back something... ',reply[0],reply[1],reply[2])
            elif Engine.level=='c':
                for digit in Keypad.code:
                    reply[counter]=abs(int(digit)-int(guess[counter]))
                    counter+=1
                diff=int(reply[0])+int(reply[1])+int(reply[2])
                diff=str(diff)
                print('The keypad gives you back something... ',diff.zfill(3))
            if guesses<9:
                print(' ',10-guesses, ' guesses remaining...')
            elif guesses==9:
                print(' ',10-guesses, ' guess remaining...')
            guesses += 1
            guess = input('[keypad entry]> ')

        if guess == Keypad.code:
            print('The lock dings and pops open! You grab the neutron bomb and run to the bridge!')
            return 'bridge'
        else:
            print('BZZZZZZZEDD!')
            print('You feel a surge of electricty rock you and your vision cuts out.')
            print('You Die')
            return 'death'

class TheBridge(Scene):
    def enter():
        msg = '''You burst into the brige with bomb under arm. You see a few Gothons, but
            but they do not see you yet.'''

        print(msg)
        options_dic={'a':'throw the bomb','b':'sneak in and place the bomb','c':'comeback another day'}
        print('Choose your next action.')
        for option in options_dic:
            print(option,') ', options_dic[option])
        action = input('> ')

        if action == 'a':
            print('In a panic you throw the bomb, at the moment of impact, you hear a large explosion.')
            return 'death'
        elif action == 'b':
            print('You gently set the bomb and then turn to run to the escape pod.')
            return 'escape_pod'
        else:
            print('Where are you going with this? Idiot')
            return 'bridge'


class EscapePod(Scene):
    def enter():
        msg = '''You find the escape pod room. There are 3 bays in front of you, but you realize
        the alert is sounding that 2 of the escape pods are malfunctioning. You know you must choose the right
        one fast because you have only moments before the neutron bomb will explode.'''

        print(msg)
        good_pod=int(Keypad.code)%3
        if good_pod==0:
            good_pod=3
        #good_pod = randint(1,3)
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
    def enter():
        print('You saved the Planet!')
        input()
        exit(0)


class Map(object):
    scenes = {}

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        return Map.scenes.get(scene_name)

    def opening_scene(self):
        return self.next_scene(self.start_scene)


def main():
    print('Only class definitions in this module.')


if __name__ == "__main__":
    print('Called from if of "gamedesign"')
    main()
