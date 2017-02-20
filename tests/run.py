#from nose import tests
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from pkg import module1
#from ..pkg import module1, module2


def test1():
    print('Test module running on 1')
    module1.main()

if __name__ == "__main__":
    print('Called from if of "tests/run"')
    test1()

'''
To change current working dir to the one containing your script you can use:
import os
os.chdir(os.path.dirname(__file__))
print(os.getcwd())
'''