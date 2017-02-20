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
        print(Death.quips[randint(0, len(self.quips)-1)])
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
    def enter():
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
    def enter():
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
    def enter():
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
    def enter():
        print('Seriously you won!')
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