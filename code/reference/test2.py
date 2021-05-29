import unittest
from functools import reduce

def xxx(acc, exists):
    print(f'acc={acc}')
    print(f'exists={exists}')
    return acc or exists

class SomeTest(unittest.TestCase):
    def test_isupper(self):
        print("    fff")
        print("    fff".lstrip())
        output = "Kumar_Ravi_003".split("-")
        print("I love Python programming"[7:13])
        print("I love Python programming"[-18:-12])
        print(output)
        print(len("Python"))

        print(" ^ ".join(["Python", "HAHA"]))
        word = [1,2,3,4]
        word[ : ] = [ ]
        print(word)
        print(5.0 / 2)

        t1 = (1,2,3, [34])
        locs = ((1,2), (2,3))
        (l1, l2) = locs
        print('map on a tuple')
        print(list(map(lambda xy: xy[0] + xy[1], locs)))
        print(l1)
        print(l2)
        a = tuple(list(t1)+[5])
        print(a)

        some_dict ={
            'x': 1,
            'y': 2,
            'stuff': {
                'some': 'stuff',
                'f': 1,
                'g': {
                    'a': 3, 'b': 5
                }
            }
        }

        print(some_dict['stuff']['g'])
        print(some_dict['stuff'].get('fgfgfg', "LOL"))
        print(dict(a=1, b=2))
        x=dict(a=1, b=2)
        del x['b']
        print(x)
        print({'a':1, 'b':2})

        set_1 = set([1,2,3,4])

        input_str = 'ABCD'
        vowels = ['a', 'e', 'i', 'o', 'u']
        result = reduce(lambda acc, exists: acc or exists, list(map(lambda vowel: input_str[0].lower() == vowel, vowels)), False)
        print("YES" if result else "NO")


        for k, v in dict(a=10, b=20).items():
            print(f'{k}={v}')
        for i in dict(a=10, b=20):
            print(i)

        d = {0, 1, 2}
        print('result of add1')
        print(d.add(45))
        print('result of add2')
        print(d.add(45))
        print('---------------------------')
        for x in d:
            print(x)
            # print(d.add(x))

        print(list(range(1,6)))

        squared = lambda x,y: x**y
        print(list(zip([1,2,3], [4,5,6])))
        first_names = ['A', 'B', 'C']
        last_names = ['X', 'Y', 'Z']
        names = list(map(lambda t: f'{t[0]} {t[1]}', list(zip(first_names, last_names))))
        print(names)

        input_list = ['AAAA', 'BBBB', 'CCCC']
        print(reduce(lambda acc, x: acc + ' ' + x, input_list, '').strip())
        print(list(range(1, 5)))
        n = 5
        def u(acc, x):
            print(f'acc={acc}')
            print(f'x={x}')
            return acc*x
        # print(reduce(lambda acc, x: acc*x, list(range(n+1)), 2))
        print(reduce(u, list(range(1, n+1)), 1))

        C = [2, 5, 9, 12, 13, 15, 16, 17, 18, 19]
        F = [2, 4, 5, 6, 7, 9, 13, 16]
        H = [1, 2, 5, 9, 10, 11, 12, 13, 15]
        cSet = set(C)
        fSet = set(F)
        hSet = set(H)
        all = set(range(1, 21))
        all3sports = cSet.intersection(fSet).intersection(hSet)
        c_and_f_but_not_h = cSet.intersection(fSet).intersection(all.difference(hSet))
        exactly_2 = filter(lambda x: x[1] == 2, list(map(lambda s: (s, (1 if s in cSet else 0) + (1 if s in fSet else 0) + (1 if s in hSet else 0)), all)))
        no_sports = all.difference(cSet.union(fSet).union(hSet))

        print(sorted(list(all3sports)))
        print(sorted(list(c_and_f_but_not_h)))
        print(sorted(list(map(lambda x: x[0], exactly_2))))
        print(sorted(list(no_sports)))
