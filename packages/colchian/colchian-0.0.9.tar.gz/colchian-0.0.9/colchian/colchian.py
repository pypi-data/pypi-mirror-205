from logging import getLogger
from typing import Union, List, Any
from copy import copy


class Colchian:
    class ValidationError(Exception):
        ...

    """
    Colchian is a library for validating and coercing data structures. You don't typically instantiate this class, but
    instead use the static and class methods to validate data.

    Examples:
    ```python
    from colchian import Colchian

    type_dict = {"an integer": int, "some strings": [str]}
    data = {"an integer": 42, "some strings": ["vastly", "hugely", "mind-bogglingly", "big"]}
    valid_data = Colchian.validated(data, type_dict)
    ```
    """
    ALLOW_INSPECT = True
    """
    If set to `True`, allows Colchian to inspect callables to avoid passing `strict` or `keys` arguments if the 
    callable does not support these. If you set `ALLOW_INSPECT` to `False`, this may improve performance, but then
    all callables must support `strict` and `keys` arguments getting passed to them.
    
    Example:
    ```
    from colchian import Colchian
    
    
    def the_answer(x):
        return x == 42
    
    
    print(Colchian.validated({'answer': 42}, {'answer': the_answer}))
    
    
    def the_answer_no_inspect(x, strict, keys):
        return x == 42
    
    
    Colchian.ALLOW_INSPECT = False
    print(Colchian.validated({'answer': 42}, {'answer': the_answer_no_inspect}))
    ```
    These function identically, but the second one is faster, because it doesn't inspect the callable - it does
    however require the unused `strict` and `keys` arguments. 
    """

    logger = getLogger()

    type_factories = {}
    """
    A dictionary of `type: factory_function` pairs. The factory function is called when a new instance of the type
    needs to be constructed, allowing you to set certain defaults. The factory function must accept a single argument,
    which will be the value of the data being validated. The factory function must return an instance of the type of
    that data, with initialisation or other operations performed on it.
    
    Example:
    ```
    from colchian import Colchian    
    
    class MyDict(dict):
        def __init__(self, p):
            super().__init__()
            self.p = p
            self.script = None
    
    
    def my_dict(d):
        result = type(d)(d.p)  # setting `p` on the result to `d.p`
        result.script = __file__
        return result
        
   
    d = MyDict('42')
    Colchian.type_factories[MyDict] = my_dict  # setting up the factory function for the type
    d2 = Colchian.validated(d, {})
    print(d2.script, d2.p == d2.p)  # print the name of the script that called validated(), and True 
    ``` 
    """

    @staticmethod
    def format_keys(keys: List[Any]) -> str:
        """
        Formats a list of keys into a string for use in error messages

        Args:
            keys: keys of any type (though typically str), that must convert into str

        Returns:
            a string representation of how `keys` would be used to access a dict, in backticks

        Examples:
        ```
        >>> Colchian.format_keys(['a', 'b', 'c'])
        '`["a"]["b"]["c"]`'
        ```
        """
        keys = "".join(
            f"[\"{key}\"]" if i == 0 else f"[\"{key}\"]"
            if isinstance(key, str) and len(key) > 0 and key[0] + key[-1] != "[]"
            else str(key) for i, key in enumerate(keys))
        return f'`{keys}`'

    @classmethod
    def text_bool(cls, x: Any, strict: bool, keys: List[str]) -> bool:
        """
        Usable example of a function that can be used to represent a boolean as case-insensitive text.
        Valid representations are: 't', 'f', 'true', or 'false'. If `strict` is `True`, only those representations
        are allowed, otherwise any non-False representation will return `True`.

        Args:
            x: the value
            strict: allow alternative non-False representations
            keys: keys of the currently validated element

        Returns:
            the boolean value represented by `x`

        Raises:
            ValidationError: if `x` does not represent a bool
        """
        if isinstance(x, bool):
            return x
        if isinstance(x, str):
            if x.lower() in ['f', 'false']:
                return False
            if not strict or x.lower() in ['t', 'true']:
                return True
        raise cls.ValidationError(f'Invalid text_bool value: {x} {cls.format_keys(keys)}')

    @classmethod
    def _execute_callable(cls, x, data_type, *args, strict, keys, **kwargs):
        """
        Execute a callable, and catch any exceptions. The result of the call to the callable is returned.

        Args:
            x:
            data_type:
            *args:
            strict:
            keys:
            **kwargs:

        Returns:
            The function results of the call to `x` with the provided arguments

        Raises:
            ValidationError if the call to `x` raises an exception, containing the exception message
        """
        try:
            return cls._fc(data_type, x, *args, strict=strict, keys=keys, **kwargs)
        except cls.ValidationError as e:
            raise e
        except Exception as e:
            if hasattr(data_type, '__name__'):
                name = data_type.__name__
            else:
                name = 'unnamed function {data_type}'
            raise cls.ValidationError(f'value at {cls.format_keys(keys)} passed to `{name}` raised `{e}`')

    @classmethod
    def _fc(cls, f, *args, **kwargs):
        """
        Helper function that calls a function, and removes `strict` and `keys` arguments if the function does not
        support them (and the class is allowed to use inspect).

        Args:
            f: the callable
            *args: arguments to pass to the callable
            **kwargs: keyword arguments to pass to the callable

        Returns:
            The return value of the callable, as called with the arguments
        """
        if cls.ALLOW_INSPECT:
            import inspect
            i_args = inspect.getargs(f.__code__).args
            if 'keys' in kwargs and 'keys' not in i_args:
                del kwargs['keys']
            if 'strict' in kwargs and 'strict' not in i_args:
                del kwargs['strict']
        return f(*args, **kwargs)

    @classmethod
    def validated(cls, x: Any, data_type: Any, strict: bool = True, _keys: Union[List, None] = None) -> Any:
        """
        Validate a value against a type specification. This function is called recursively, but typically it is called
        directly with `x` and `data_type` as dictionary arguments. Strict validation implies that only keys in the
        `data_type` are allowed in `x`, and that value types must match the defined type. If `strict` is `False`, then
        additional keys will be skipped, and types will be coerced to the defined type if possible.

        Args:
            x: the value to validate, typically a dict
            data_type: the type specification, typically a dict
            strict: whether to validate strictly
            _keys: for internal use in recursion

        Returns:
            The validated value, the same type as `x`, but possibly with some type coercion. The validated value will
            be newly constructed, using the same types as the original. Both dictionary and list types are supported
            for structuring the data.
        """
        if _keys is None:
            _keys = []
        if isinstance(data_type, dict):
            if not isinstance(x, dict):
                raise cls.ValidationError(f'expected {cls.format_keys(_keys)} to be a dict, not a {type(x)}')
            # if a constructor override was provided for type of x, call that with x, instead of the type constructor
            for t in cls.type_factories:
                if isinstance(x, t):
                    result = cls.type_factories[t](x)
                    # no check for multiple matches, first hit wins
                    break
            else:
                result = type(x)()
            wildcards = {
                key: dt for key, dt in data_type.items()
                if callable(key) or isinstance(key, tuple) or key.split(':')[0] == '*'
            }
            values = {}
            used_keys = []
            for key, type_value in data_type.items():
                if key not in wildcards:
                    new_keys = _keys + [key]
                    if not isinstance(key, str) and strict:
                        raise cls.ValidationError(f'non-string dictionary key {cls.format_keys(_keys)}')
                    # if the value is optional
                    if key not in x and (
                            (hasattr(type_value, '__origin__')
                             and type_value.__origin__ == Union
                             and type(None) in type_value.__args__) or
                            (isinstance(type_value, tuple)
                             and None in type_value)):
                        continue
                    if key not in x:
                        raise cls.ValidationError(f'missing required key {key} in {cls.format_keys(_keys)}')
                    if not wildcards:
                        result[key] = cls.validated(x[key], type_value, strict, new_keys)
                    else:
                        values[key] = (x[key], type_value, strict, new_keys)
                    used_keys.append(key)
            if wildcards:
                for key, value in x.items():
                    if key not in used_keys:
                        new_keys = _keys + [key]
                        for wildcard in wildcards:
                            try:
                                if isinstance(wildcard, type):
                                    if not isinstance(key, wildcard):
                                        if strict:
                                            raise cls.ValidationError(
                                                f'key {cls.format_keys(new_keys)} not of specified type {wildcard}')
                                        else:
                                            try:
                                                key = wildcard(key)
                                                new_keys[-1] = key
                                            except ValueError:
                                                raise cls.ValidationError(
                                                    f'key {cls.format_keys(new_keys)} cannot be cast to {wildcard}')
                                elif (
                                    (callable(wildcard) and cls._fc(wildcard, key, strict=strict, keys=new_keys) != key)
                                    or
                                    (isinstance(wildcard, tuple) and callable(wildcard[0]) and
                                     not isinstance(wildcard[0], type) and
                                     cls._fc(wildcard[0], key, *wildcard[1:], strict=strict, keys=new_keys) != key)
                                   ):
                                    raise cls.ValidationError(
                                        f'mismatch between key {cls.format_keys(new_keys)} and generated key')
                                elif (
                                    isinstance(wildcard, tuple) and
                                    (not callable(wildcard[0]) or isinstance(wildcard[0], type)) and
                                    key not in wildcard
                                   ):
                                    types = []
                                    converted = key
                                    for w in wildcard:
                                        if isinstance(w, type):
                                            types.append(w)
                                            try:
                                                if isinstance(key, w):
                                                    converted = key
                                                    break
                                                if id(key) == id(converted) and not strict:
                                                    converted = w(key)
                                            except ValueError:
                                                continue
                                    else:
                                        if id(key) == id(converted):
                                            if types:
                                                raise cls.ValidationError(
                                                    f'key {cls.format_keys(new_keys)} could not be cast to any {types}')
                                            else:
                                                raise cls.ValidationError(
                                                    f'restricted key {cls.format_keys(new_keys)} not in {wildcard}')
                                    key = converted
                                    new_keys[-1] = key
                                y = cls.validated(value, data_type[wildcard], strict, new_keys)
                                break
                            except cls.ValidationError as e:
                                if len(wildcards) == 1:
                                    raise cls.ValidationError(
                                        f'could not match to only wildcard {wildcard}, raised `{e}`')
                                continue
                        else:
                            if strict:
                                raise cls.ValidationError(
                                    f'value of {cls.format_keys(new_keys)} could not be matched to wildcard')
                            result[key] = x[key]
                            continue
                        result[key] = y
                    else:
                        result[key] = cls.validated(*values[key])
            return result
        elif hasattr(data_type, '__origin__') and (data_type.__origin__ == Union):
            result = cls.validated(x, tuple(data_type.__args__), strict, _keys)
        elif isinstance(data_type, tuple):
            if data_type and not isinstance(data_type[0], type) and callable(data_type[0]):
                result = cls._execute_callable(x, data_type[0], *data_type[1:], strict=strict, keys=_keys)
            else:
                for type_value in data_type:
                    # tuple may contain None when checking optional values
                    if type_value is None:
                        continue
                    try:
                        result = cls.validated(x, type_value, strict, _keys)
                        break
                    except cls.ValidationError as e:
                        if len(data_type) == 1:
                            raise e
                        continue
                else:
                    raise cls.ValidationError(
                        f'value does not match any of the optional types at {cls.format_keys(_keys)}')
        elif hasattr(data_type, '__origin__') and (data_type.__origin__ == list):
            result = cls.validated(x, list(data_type.__args__), strict, _keys)
        elif isinstance(data_type, list):
            # read an empty list as a list of any type (any list can be empty)
            data_type = [Any] if not data_type else data_type
            if not isinstance(x, list):
                raise cls.ValidationError(f'expected a list at {cls.format_keys(_keys)}, got {type(x)}')
            if len(data_type) != 1:
                raise cls.ValidationError(
                    f'multiple types for list content unexpected at {cls.format_keys(_keys)}: {data_type}')
            result = [cls.validated(elem, data_type[0], strict, _keys + [f'[{n}]']) for n, elem in enumerate(x)]
        elif isinstance(data_type, type):
            if isinstance(x, data_type):
                result = x
            else:
                if strict:
                    raise cls.ValidationError(f'strict type mismatch (no casting) at {cls.format_keys(_keys)}, '
                                              f'expected `{data_type.__name__}`, found `{type(x).__name__}`')
                try:
                    result = data_type(x)
                except ValueError:
                    raise cls.ValidationError(f'type mismatch, casting failed at {cls.format_keys(_keys)}, '
                                              f'expected `{data_type.__name__}`, found `{type(x).__name__}`')
        elif data_type is Any:
            result = x
        elif callable(data_type):
            result = cls._execute_callable(x, data_type, strict=strict, keys=_keys)
        elif x != data_type:
            # remaining option is identity, the "data_type" is a value that's required
            raise cls.ValidationError(f'value "{x}" does not match expected "{data_type}" at {cls.format_keys(_keys)}')
        else:
            result = copy(data_type)
        return result
