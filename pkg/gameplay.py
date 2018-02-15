from gamedesign import *


def main():
   
    a_map = Map('central_corridor')
    a_map.scenes.update({'central_corridor': CentralCorridor})
    #a_map.scenes.update({'armory': WeaponArmory})
    a_map.scenes.update({'keypad': Keypad})
    a_map.scenes.update({'bridge': TheBridge})
    a_map.scenes.update({'escape_pod': EscapePod})
    a_map.scenes.update({'death': Death})
    a_map.scenes.update({'finished': Victory})
    a_game = Engine(a_map)
    a_game.play()


if __name__ == "__main__":
    #print('Called from if of "gameplay"')
    main()
