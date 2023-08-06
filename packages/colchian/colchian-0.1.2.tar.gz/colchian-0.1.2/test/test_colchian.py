import logging
from colchian import Colchian
import unittest
import typing


class TestJsonTyping(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(level=logging.WARNING)

    def tearDown(self) -> None:
        pass

    def test_version_defined(self):
        try:
            from colchian import __version__
        except ImportError:
            self.fail('__version__ not in package')

    def test_required(self):
        td = {
            'required': str,
            'not required': typing.Union[None, str],
            'also not required': typing.Optional[str],
            'not required but there': typing.Optional[str]
        }
        data = {
            'required': 'x',
            'not required but there': None
        }
        self.assertEqual(data, Colchian.validated(data, td),
                         'required and not required fields work with Union[None, type] and Optional[type]')
        data = {
        }
        with self.assertRaises(Colchian.ValidationError,
                               msg='missing required key in data results in Colchian.ValidationError'):
            Colchian.validated(data, td)

    def test_simple_types(self):
        td = {
            'i': int,
            'f': float,
            's': str,
            'b': bytes,
            't': bool
        }
        data = {
            'i': 1,
            'f': 1.5,
            's': 'test',
            'b': b'test',
            't': True
        }
        self.assertEqual(data, Colchian.validated(data, td),
                         'simple types check out')
    def test_not_simple_types(self):
        td = {
            'i': int,
            'f': float,
        }
        data = {
            'i': 1,
            'f': '1.5'
        }
        with self.assertRaises(Colchian.ValidationError, msg='simple types mismatches'):
            Colchian.validated(data, td, strict=True)  # default
        try:
            Colchian.validated(data, td, strict=False)
        except Colchian.ValidationError:
            self.fail("simple types cast when not strict")
        data = {
            'i': 1,
            'f': 'banana'
        }
        with self.assertRaises(Colchian.ValidationError, msg='simple types mismatches when not strict and no cast'):
            Colchian.validated(data, td, strict=False)

    def test_wildcards(self):
        td = {
            '*:1': {
                'i': int
            },
            '*:2': str,
            'a': float
        }
        data = {
            'x': {'i': 1},
            'y': 'some test',
            'a': 1.2,
            'z': {'i': 123}
        }
        self.assertEqual(data, Colchian.validated(data, td),
                         'wilcards match unmatched values')

    def test_nested_types(self):
        td = {
            'i': int,
            'd': {
                'i': int,
                's': str,
                'd': {
                    'f': float
                }
            }
        }
        data = {
            'i': 1,
            'd': {
                'i': 2,
                's': 'test',
                'd': {
                    'f': 3.0
                }
            }
        }
        self.assertEqual(data, Colchian.validated(data, td),
                         'nested types check out')

    def test_nested_wildcards(self):
        td = {
            'x': {
                '*': {
                    'i': int
                }
            },
            'y': {
                '*:1': {
                    's': str
                },
                '*:2': {
                    'f': float
                }
            }
        }
        data = {
            'x': {
                'a': {'i': 1},
                'b': {'i': 2}
            },
            'y': {
                'a': {'s': 'pi'},
                'b': {'f': .1},
                'c': {'f': 3.14},
                'd': {'s': 'text'}
            }
        }
        self.assertEqual(data, Colchian.validated(data, td),
                         'nested wildcards get correctly resolved')

    def test_custom_type(self):
        class MyInt(int):
            pass
        td = {
            'x': MyInt
        }
        data = {
            'x': 3
        }
        with self.assertRaises(Colchian.ValidationError, msg='custom types fail when strict'):
            Colchian.validated(data, td)
        try:
            result = Colchian.validated(data, td, strict=False)
            self.assertIsInstance(result['x'], MyInt, 'custom type preserved')
        except Colchian.ValidationError:
            self.fail('custom types only validate when not strict')

    def _test_union(self, td):
        data = {
            'x': 3
        }
        try:
            result = Colchian.validated(data, td)
            self.assertEqual(3, result['x'], 'int option resolved correctly for union')
        except Colchian.ValidationError:
            self.fail('int option allowed in union')
        data = {
            'x': 'test'
        }
        try:
            result = Colchian.validated(data, td)
            self.assertEqual('test', result['x'], 'str option resolved correctly for union')
        except Colchian.ValidationError:
            self.fail('str option allowed in union')
        data = {
            'x': 0.3
        }
        with self.assertRaises(Colchian.ValidationError, msg='float option not allowed in str, int union'):
            Colchian.validated(data, td)

    def test_union_variants(self):
        # helper tries int, str, and float value for 'x'
        self._test_union({
            'x': typing.Union[int, str]
        })

        self._test_union({
            'x': (int, str)
        })

        self._test_union({
            'x': (None, typing.Union[int, str])
        })

        td = {
            'x': typing.Union[int, str, None]
        }
        try:
            Colchian.validated({}, td)
        except Colchian.ValidationError:
            self.fail('optional value allowed for None in Union')

        td = {
            'x': typing.Optional[typing.Union[int, str]]
        }
        try:
            Colchian.validated({}, td)
        except Colchian.ValidationError:
            self.fail('optional value allowed for Optional Union')

        td = {
            'x': (None, typing.Union[int, str])
        }
        try:
            Colchian.validated({}, td)
        except Colchian.ValidationError:
            self.fail('optional value allowed for Union paired with None')

    def test_callable(self):
        def yes_no(x, strict, keys):
            if x not in ['yes', 'no']:
                raise Colchian.ValidationError('Only yes or no allowed')
            return True if x == 'yes' else False

        def add_params(x, y, z, strict, keys):
            return x + y + z

        self.assertEqual({'x': True}, Colchian.validated({'x': 'yes'}, {'x': yes_no}),
                         'basic callable returning bool')

        self.assertEqual({'y': True}, Colchian.validated({'y': 'yes'}, {'y': yes_no}),
                         'basic callable returning bool')

        with self.assertRaises(Colchian.ValidationError, msg='strict bool fails on non-bool text'):
            Colchian.validated({'bool': 'not True'}, {'bool': Colchian.text_bool})
        try:
            self.assertEqual({'bool': True}, Colchian.validated({'bool': 'True'}, {'bool': Colchian.text_bool},
                                                                strict=False),
                             'non-bool text is True when not strict')
        except Colchian.ValidationError:
            self.fail('non-bool text does not fail when not strict')
        with self.assertRaises(Colchian.ValidationError, msg='callable fails on mismatched text'):
            Colchian.validated({'x': 'test'}, {'x': yes_no})

        self.assertEqual({'x': 'xab'}, Colchian.validated({'x': 'x'}, {'x': (add_params, 'a', 'b')}),
                         'basic callable returning bool')

    def test_list(self):
        td = {
            'xs': (None, [int]),
            'ys': (None, [int]),
            'zs': (None, [str])
        }
        data = {
            'xs': [0, 1, 2],
            'ys': [],
            'zs': ['x']
        }
        self.assertEqual(data, Colchian.validated(data, td),
                         'basic lists get correctly resolved')
        with self.assertRaises(Colchian.ValidationError, msg='only int accepted in list of int when strict'):
            Colchian.validated({'xs': ['3']}, td)
        self.assertEqual({'xs': [1, 2, 3]}, Colchian.validated({'xs': [1.0, 2, '3']}, td, strict=False),
                         'list int values are cast when not strict')
        with self.assertRaises(Colchian.ValidationError, msg='only str accepted in list of str when strict'):
            Colchian.validated({'zs': [3]}, td)
        self.assertEqual({'zs': ['1.0', '2', '3']}, Colchian.validated({'zs': [1.0, 2, '3']}, td, strict=False),
                         'list str values are cast when not strict')
        self.assertEqual({'xs': [1, 2, 3]},
                         Colchian.validated({'xs': [1.0, 2, '3']}, {'xs': typing.List[int]}, strict=False),
                         'list int values are cast when not strict')

    def test_values(self):
        self.assertEqual({'x': 'a', 'y': 'c'}, Colchian.validated({'x': 'a', 'y': 'c'}, {'x': ('a', 'b'), 'y': 'c'}),
                         'values get correctly resolved')

    def test_type_key(self):
        self.assertEqual({1: 'one'}, Colchian.validated({1: 'one'}, {int: 'one'}),
                         'type keys are validated')
        with self.assertRaises(Colchian.ValidationError, msg='type key mismatch caught'):
            Colchian.validated({'1': 'one'}, {int: 'one'})
        with self.assertRaises(Colchian.ValidationError, msg='type key value mismatch caught'):
            Colchian.validated({1: 'one'}, {int: 'two'})

    def test_callable_key(self):
        def uppercase(x, strict, keys):
            if x.upper() != x:
                raise Colchian.ValidationError('key not in uppercase')
            return x

        def uppercase_no_keywords(x):
            if x.upper() != x:
                raise Colchian.ValidationError('key not in uppercase')
            return x

        self.assertEqual({'ABC': 1}, Colchian.validated({'ABC': 1}, {uppercase: int}),
                         'callable keys are validated')
        with self.assertRaises(Colchian.ValidationError, msg='callable key mismatch caught'):
            Colchian.validated({'Abc': 1}, {uppercase: int})
        with self.assertRaises(Colchian.ValidationError, msg='callable key value mismatch caught'):
            Colchian.validated({'ABC': 'one'}, {uppercase: int})
        with self.assertRaises(Colchian.ValidationError, msg='same result with keywords lacking'):
            Colchian.validated({'ABC': 'one'}, {uppercase_no_keywords: int})

    def test_callable_parameters_key(self):
        def greater(x, y, strict, keys):
            if x <= y:
                raise Colchian.ValidationError(f'{x} not greater than {y}')
            return x
        self.assertEqual({4: 1}, Colchian.validated({4: 1}, {(greater, 3): (greater, 0)}),
                         'callable keys with parameters are validated')
        with self.assertRaises(Colchian.ValidationError, msg='callable key with parameters mismatch caught'):
            Colchian.validated({4: 1}, {(greater, 5): int})

    def test_tuple_restricted_key(self):
        self.assertEqual({3: 1, 4: 1}, Colchian.validated({3: 1, 4: 1}, {(3, 4): 1}),
                         'tuple restricted keys are validated')
        with self.assertRaises(Colchian.ValidationError, msg='tuple restricted key with parameters mismatch caught'):
            Colchian.validated({3: 1, 5: 1}, {(3, 4): 1})
        self.assertEqual({1: 1, 10: 1}, Colchian.validated({1: 1, 10: 1}, {tuple(range(1, 11)): 1}),
                         'tuple restricted keys are validated')

    def test_constructor_override(self):
        class MyDict(dict):
            important = True

        def my_dict_factory(x: MyDict):
            result = type(x)()
            result.important = x.important
            return result

        class MyDict2(MyDict):
            important = True
            also_important = True

        Colchian.type_factories[MyDict] = my_dict_factory

        md = Colchian.validated(MyDict({'a': 1}), {'a': int})
        self.assertEqual(True, md.important, 'attribute on overridden class is set')

        md = MyDict({'a': 1})
        md.important = False
        md = Colchian.validated(md, {'a': int})
        self.assertEqual(False, md.important, 'attribute on overridden class is set correctly')

        md = MyDict2({'a': 1})
        md.important = False
        md = Colchian.validated(md, {'a': int})
        self.assertEqual(False, md.important, 'attribute on overridden class is set correctly on child class')
        self.assertIsInstance(md, MyDict2, 'correct constructor is used in construction validated result')

    def test_key_type(self):
        td = {
            int: int,
        }
        self.assertEqual({1: 2}, Colchian.validated({1: 2}, td), 'int key check works')
        with self.assertRaises(Colchian.ValidationError, msg='cast not allowed when strict'):
            Colchian.validated({'1': 2}, td, strict=True)
        self.assertEqual({1: 2}, Colchian.validated({1: 2}, td, strict=False), 'int cast works when not strict')
        with self.assertRaises(Colchian.ValidationError, msg='impossible cast not allowed') as cm:
            Colchian.validated({'1.0': 2}, td, strict=False)
        self.assertEqual(
            'could not match to only wildcard <class \'int\'>, raised `key `["1.0"]` cannot be cast to <class \'int\'>`',
            str(cm.exception)
        )

    def test_key_type_tuple(self):
        td = {
            (int, str): int,
        }
        self.assertEqual({1: 2}, Colchian.validated({1: 2}, td, strict=True),
                         'int key allowed for (int, str) pair')
        self.assertEqual({'test': 2}, Colchian.validated({'test': 2}, td, strict=True),
                         'str key allowed for (int, str) pair')
        td = {
            (str, int): int,
        }
        self.assertEqual({1: 2}, Colchian.validated({1: 2}, td, strict=True),
                         'no conversion to first type in pair')
        with self.assertRaises(Colchian.ValidationError, msg='float key not allowed for strict (int, str)') as cm:
            Colchian.validated({1.0: 2}, td, strict=True)
        self.assertEqual({1: 2}, Colchian.validated({1: 2}, td, strict=True),
                         'no conversion to first type in pair')
        self.assertEqual({'1.0': 2}, Colchian.validated({1.0: 2}, td, strict=False),
                         'conversion to first type (str, int) if not strict')
        td = {
            (int, str): int,
        }
        self.assertEqual({1: 2}, Colchian.validated({1.0: 2}, td, strict=False),
                         'conversion to first type (int, str) if not strict')
