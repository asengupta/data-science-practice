import unittest

class SomeTest(unittest.TestCase):
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
        # self.assertTrue('Foo'.isupper())
        x = 5
        print(x)
        y=f'dfdf-{x}'
        print(y)
        print('dd' + 'ff')
        print('dd'  'ff' 'dfdf' 'fdfd')
        # print(y[-2:])
        print(y[-3])
        print('Length=' + str(len(y)))
        print(f'Length={len(y)}')

        x = [1,2,3,4,5]
        x.append(6)
        print(x[:])
        print(x[:-1])
        print(list(map(lambda x: x**2, x)))

        for t in x:
            print(f'{t} LOL')

        for t in range(11, 1, -2):
            print(str(t*t) + " is ok")

        y = [1,2,[4,5]]
        print(y[-1])

        p = 1
        while p<10:
            print(p)
            if p == 5:
                print("p is 5!")
            p += 1


        animals = ['dog', 'cat', 'horse']
        for animal in animals:
            print(animal)

        print(sum(range(11)))

        for t in range(11):
            if t == 5:
                print('Breaking out')
                break
            elif t == 2:
                print("It is 2")
            else:
                print("not yet " + str(t))

        def f(x):
            return x*2

        print(f(4))

        g=lambda x: lambda y: x + y

        print(g(3)(4))
        def h(a, b=2):
            return a+b

        print(h(b=466, a=3))
        # print(h(a=466, 4))
        print('dodg' in animals)

        def j(a,b,*args,**kwargs):
            print(f'sum is {a+b}')
            for arg in args:
                print(arg)
            for kwarg in kwargs:
                print(kwarg)

        j(1,2, 3, 4, foo=34, bar=45)
        print(list(reversed("avishek")))
        print("avishek"[-1:3:-1])

