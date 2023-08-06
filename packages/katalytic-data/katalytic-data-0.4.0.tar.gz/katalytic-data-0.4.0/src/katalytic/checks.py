import collections
import inspect


def contains_all_of(haystack, needles):
    if not is_iterable(haystack):
        raise TypeError(f'<haystack> expects an iterable. Got {type(haystack).__name__}: {haystack!r}')
    elif not is_iterable(needles):
        raise TypeError(f'<needles> expects an iterable. Got {type(needles).__name__}: {needles!r}')

    for needle in needles:
        if not is_any_of(needle, haystack):
            return False

    return True


def contains_any_of(haystack, needles):
    if not is_iterable(haystack):
        raise TypeError(f'<haystack> expects an iterable. Got {type(haystack).__name__}: {haystack!r}')
    elif not is_iterable(needles):
        raise TypeError(f'<needles> expects an iterable. Got {type(needles).__name__}: {needles!r}')

    for needle in needles:
        if is_any_of(needle, haystack):
            return True

    return False


def contains_none_of(haystack, needles):
    return not contains_any_of(haystack, needles)


def dicts_share_key_order(data_1, data_2, recursive=False):
    if not isinstance(recursive, bool):
        raise TypeError(f'<data_2> must be True or False. Got {type(recursive)}')

    if isinstance(data_1, dict):
        if not isinstance(data_2, dict):
            raise TypeError(f'<data_2> must be a dict. Got {type(data_2)}')

        if list(data_1.keys()) != list(data_2.keys()):
            return False

        if recursive:
            return all(
                dicts_share_key_order(v_1, v_2, recursive=recursive)
                for v_1, v_2 in zip(data_1.values(), data_2.values()))
        else:
            return True
    elif recursive and is_sequence(data_1):
        if not is_sequence(data_2):
            raise TypeError(f'<data_2> must be a sequence. Got {type(data_2)}')

        return all(
            dicts_share_key_order(d_1, d_2, recursive=recursive)
            for d_1, d_2 in zip(data_1, data_2))
    elif not recursive:
        raise TypeError(f'<data_1> and <data_2> must be dicts. Got {type(data_1)} and {type(data_2)}')
    else:
        return True


def dicts_share_value_order(data_1, data_2, recursive=False):
    if not isinstance(recursive, bool):
        raise TypeError(f'<data_2> must be True or False. Got {type(recursive)}')

    if isinstance(data_1, dict):
        if not isinstance(data_2, dict):
            raise TypeError(f'<data_2> must be a dict. Got {type(data_2)}')

        if list(data_1.values()) != list(data_2.values()):
            return False

        if recursive:
            return all(
                dicts_share_value_order(v_1, v_2, recursive=recursive)
                for v_1, v_2 in zip(data_1.values(), data_2.values()))
        else:
            return True
    elif recursive and is_sequence(data_1):
        return all(
            dicts_share_value_order(d_1, d_2, recursive=recursive)
            for d_1, d_2 in zip(data_1, data_2))
    elif not recursive:
        raise TypeError(f'<data_1> and <data_2> must be dicts. Got {type(data_1)} and {type(data_2)}')
    else:
        return True


def is_any_of(needle, haystack):
    if not is_iterable(haystack):
        raise TypeError(f'<haystack> expects an iterable. Got {type(haystack).__name__}: {haystack!r}')

    return any(is_equal(needle, x) for x in haystack)


def is_dict_of_sequences(x):
    return isinstance(x, dict) and len(x) >= 1 and all(is_sequence(v) for v in x.values())


def is_dict_of_sequences_uniform(x):
    """Each sequence must have the same length as the others"""
    if not is_dict_of_sequences(x):
        return False

    n = len(list(x.values())[0])
    return all(len(v) == n for v in x.values())


def is_equal(a, b):
    if is_singleton(a) or is_singleton(b):
        return a is b
    else:
        return a == b


def is_generator(x):
    return inspect.isgenerator(x)


def is_iterable(x):
    try:
        # The only reliable way to determine whether an object is iterable is to call iter(obj).
        iter(x)
        # str, bytes, bytearray are theoretically a iterables,
        # but in practice we use them as primitives
        return not isinstance(x, (str, bytes, bytearray))
    except TypeError:
        return False


def is_iterable_or_str(x):
    return isinstance(x, collections.abc.Iterable)


def is_iterator(x):
    return isinstance(x, collections.abc.Iterator)


def is_none_of(needle, haystack):
    return not is_any_of(needle, haystack)


def is_primitive(x):
    """str is theoretically a collection, but in practice we use it as a primitive"""
    return isinstance(x, (str, int, float, bool, type(None)))


def is_sequence(x):
    """str is theoretically an sequence, but in practice we use it as a primitive"""
    return isinstance(x, collections.abc.Sequence) and not isinstance(x, (str, bytes, bytearray))


def is_sequence_of_dicts(x):
    return is_sequence(x) and len(x) >= 1 and all(isinstance(xi, dict) for xi in x)


def is_sequence_of_dicts_uniform(x):
    """Each dict must have the same keys as the others"""
    if not is_sequence_of_dicts(x):
        return False

    keys = set(x[0].keys())
    return all(set(xi.keys()) == keys for xi in x)


def is_sequence_of_sequences(x):
    return is_sequence(x) and len(x) >= 1 and all(is_sequence(xi) for xi in x)


def is_sequence_of_sequences_uniform(x):
    """Each sequence must have the same length as the others"""
    if not is_sequence_of_sequences(x):
        return False

    n = len(x[0])
    return all(len(xi) == n for xi in x)


def is_sequence_or_str(x):
    """str is theoretically an sequence, but in practice we use it as a primitive"""
    return isinstance(x, collections.abc.Sequence)


def is_singleton(x):
    return isinstance(x, (bool, type(None)))
