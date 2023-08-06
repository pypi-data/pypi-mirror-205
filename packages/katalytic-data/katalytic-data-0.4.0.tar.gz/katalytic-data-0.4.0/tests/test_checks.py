from katalytic.checks import (
    contains_all_of, contains_any_of, contains_none_of, is_any_of, is_dict_of_sequences, is_generator, is_iterable, is_iterable_or_str, is_iterator, is_none_of, is_primitive,
    is_sequence, is_sequence_of_dicts, is_sequence_of_sequences, is_sequence_or_str, is_sequence_of_dicts_uniform,
    is_dict_of_sequences_uniform, is_sequence_of_sequences_uniform, dicts_share_key_order, dicts_share_value_order, is_singleton, is_equal
)

import pytest


def _generator():
    yield 1


class Test_contains_all_of:
    @pytest.mark.parametrize('wrong_type', [object(), 1, True, False, None, ''])
    def test_haystack_not_iterable(self, wrong_type):
        with pytest.raises(TypeError):
            contains_all_of(wrong_type, [])

    @pytest.mark.parametrize('wrong_type', [object(), 1, True, False, None, ''])
    def test_needles_not_iterable(self, wrong_type):
        with pytest.raises(TypeError):
            contains_all_of([], wrong_type)

    @pytest.mark.parametrize('haystack, needles', [
        (range(10), {1, 3, 5}),
        ({True, False, None}, [True, None]),
        ({True, False, None}, [True, False]),
        ({True, False, None}, [False, None]),
    ])
    def test_True(self, haystack, needles):
        assert contains_all_of(haystack, needles)

    @pytest.mark.parametrize('haystack, needles', [
        (range(10), {True, 1, 3, 5}),
        ([True], {(), 'hello', True}),
        (range(10), [True, False]),
        (range(10), [100, 666]),
        ({None}, (True, False)),
    ])
    def test_False(self, haystack, needles):
        assert not contains_all_of(haystack, needles)


class Test_contains_any_of:
    @pytest.mark.parametrize('wrong_type', [object(), 1, True, False, None, ''])
    def test_haystack_not_iterable(self, wrong_type):
        with pytest.raises(TypeError):
            contains_any_of(wrong_type, [])

    @pytest.mark.parametrize('wrong_type', [object(), 1, True, False, None, ''])
    def test_needles_not_iterable(self, wrong_type):
        with pytest.raises(TypeError):
            contains_any_of([], wrong_type)

    @pytest.mark.parametrize('haystack, needles', [
        (range(10), [True, False]),
        (range(10), [100, 666]),
        ({None}, (True, False)),
    ])
    def test_False(self, haystack, needles):
        assert not contains_any_of(haystack, needles)

    @pytest.mark.parametrize('haystack, needles', [
        (range(10), {True, False, 5}),
        ([True], {(), 'hello', True}),
    ])
    def test_True(self, haystack, needles):
        assert contains_any_of(haystack, needles)


class Test_contains_none_of:
    @pytest.mark.parametrize('wrong_type', [object(), 1, True, False, None, ''])
    def test_haystack_not_iterable(self, wrong_type):
        with pytest.raises(TypeError):
            contains_none_of(wrong_type, [])

    @pytest.mark.parametrize('wrong_type', [object(), 1, True, False, None, ''])
    def test_needles_not_iterable(self, wrong_type):
        with pytest.raises(TypeError):
            contains_none_of([], wrong_type)

    @pytest.mark.parametrize('haystack, needles', [
        (range(10), [True, False]),
        (range(10), [100, 666]),
        ({None}, (True, False)),
    ])
    def test_True(self, haystack, needles):
        assert contains_none_of(haystack, needles)

    @pytest.mark.parametrize('haystack, needles', [
        (range(10), {True, False, 5}),
        ([True], {(), 'hello', True}),
    ])
    def test_False(self, haystack, needles):
        assert not contains_none_of(haystack, needles)


class Test_dicts_share_key_order:
    @pytest.mark.parametrize('wrong_type', [[], set(), (), {}, 1, 1.0, None, 'string', object()])
    def test_not_a_bool(self, wrong_type):
        with pytest.raises(TypeError):
            dicts_share_key_order({}, {}, recursive=wrong_type)

    @pytest.mark.parametrize('wrong_type', [[], set(), (), 1, 1.0, None, 'string', object()])
    def test_not_a_dict(self, wrong_type):
        with pytest.raises(TypeError):
            dicts_share_key_order({}, wrong_type)

        with pytest.raises(TypeError):
            dicts_share_key_order(wrong_type, wrong_type)

        with pytest.raises(TypeError):
            dicts_share_key_order({'a': {}}, {'a': wrong_type}, recursive=True)

    @pytest.mark.parametrize('wrong_type', [[], (), 1, 1.0, None, 'string', object()])
    def test_no_dicts(self, wrong_type):
        with pytest.raises(TypeError):
            dicts_share_key_order(wrong_type, wrong_type, recursive=False)

    @pytest.mark.parametrize('wrong_type', [{}, 1, 1.0, None, 'string', object()])
    def test_not_a_sequence(self, wrong_type):
        with pytest.raises(TypeError):
            dicts_share_key_order([], wrong_type, recursive=True)

        with pytest.raises(TypeError):
            dicts_share_key_order({'a': []}, {'a': wrong_type}, recursive=True)

    def test_empty(self):
        assert dicts_share_key_order({}, {})

    @pytest.mark.parametrize('dict_1, dict_2', [
        [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}],
        [{'a': {'b': 1, 'c': 2}}, {'a': {'b': 1, 'c': 2}}],
        [[{'a': 1, 'b': 2}], [{'a': 3, 'b': 4}]],
    ])
    def test_True(self, dict_1, dict_2):
        assert dicts_share_key_order(dict_1, dict_2, recursive=True)

    @pytest.mark.parametrize('dict_1, dict_2', [
        [{'a': 1, 'b': 2}, {'b': 1, 'a': 2}],
        [{'a': 1, 'b': 2}, {'a': 1, 'c': 2}],
        [{'a': {'b': 1, 'c': 2}}, {'a': {'c': 1, 'b': 2}}],
        [{'a': {'b': 1, 'c': 2}}, {'a': {'x': 1, 'y': 2}}],
        [{'a': {'b': 1, 'c': 2}}, {'z': {'x': 1, 'y': 2}}],
        [[{'a': 1, 'b': 2}], [{'b': 3, 'a': 4}]],
        [[{'a': 1, 'b': 2}], [{'x': 3, 'y': 4}]],
    ])
    def test_False(self, dict_1, dict_2):
        assert not dicts_share_key_order(dict_1, dict_2, recursive=True)


class Test_dicts_share_value_order:
    @pytest.mark.parametrize('wrong_type', [[], set(), (), {}, 1, 1.0, None, 'string', object()])
    def test_not_a_bool(self, wrong_type):
        with pytest.raises(TypeError):
            dicts_share_value_order({}, {}, recursive=wrong_type)

    @pytest.mark.parametrize('wrong_type', [[], set(), (), 1, 1.0, None, 'string', object()])
    def test_not_a_dict(self, wrong_type):
        with pytest.raises(TypeError):
            dicts_share_value_order({}, wrong_type)

        with pytest.raises(TypeError):
            dicts_share_value_order(wrong_type, wrong_type)

    @pytest.mark.parametrize('wrong_type', [[], (), 1, 1.0, None, 'string', object()])
    def test_no_dicts(self, wrong_type):
        with pytest.raises(TypeError):
            dicts_share_value_order(wrong_type, wrong_type, recursive=False)

    @pytest.mark.parametrize('wrong_type', [{}, 1, 1.0, None, 'string', object()])
    def test_not_a_sequence(self, wrong_type):
        with pytest.raises(TypeError):
            dicts_share_value_order([], wrong_type)

    def test_empty(self):
        assert dicts_share_value_order({}, {})

    @pytest.mark.parametrize('dict_1, dict_2', [
        [{'a': 1, 'b': 2}, {'c': 1, 'd': 2}],
        [{'a': {'b': 1, 'c': 2}}, {'b': {'b': 1, 'c': 2}}],
        [[{'a': 1, 'b': 2}], [{'c': 1, 'd': 2}]],
    ])
    def test_simple(self, dict_1, dict_2):
        assert dicts_share_value_order(dict_1, dict_2, recursive=True)
        assert dicts_share_value_order(dict_1, dict_2, recursive=True)
        assert dicts_share_value_order(dict_1, dict_2, recursive=True)

    @pytest.mark.parametrize('dict_1, dict_2', [
        [{'a': {'b': 1, 'c': 2}}, {'b': {'c': 1, 'b': 2}}],
        [{'a': {'b': 1, 'c': 2}}, {'b': {'b': 2, 'c': 1}}],
        [{'a': 1, 'b': 2}, {'c': 2, 'd': 1}],
        [[{'a': 2, 'b': 1}], [{'c': 1, 'd': 2}]],
    ])
    def test_recursive(self, dict_1, dict_2):
        assert not dicts_share_value_order(dict_1, dict_2, recursive=True)


class Test_is_any_of:
    @pytest.mark.parametrize('wrong_type', [object(), 1, True, False, None, ''])
    def test_not_iterable(self, wrong_type):
        with pytest.raises(TypeError):
            is_any_of([], haystack=wrong_type)

    @pytest.mark.parametrize('x, iterable', [
        (0, [1, 2, 3]),
        (4, [1, 2, 3]),
        ('a', {'b': 'a', 'c': 'd'}),
        ({}, [1, 2, 3]),
        (True, {1, None, False}),
    ])
    def test_False(self, x, iterable):
        assert not is_any_of(x, iterable)

    @pytest.mark.parametrize('x, iterable', [
        (2, [1, 2, 3]),
        ('a', {'a': 'b', 'c': 'd'}),
        ({}, [1, 2, {}, 3]),
        (True, {None, True, False}),
    ])
    def test_True(self, x, iterable):
        assert is_any_of(x, iterable)

    @pytest.mark.parametrize('x, iterable', [
        (1, [True, False]),
        (0, [True, False]),
        (True, [0, 1]),
        (False, [0, 1]),
    ])
    def test_bools_are_not_ints(self, x, iterable):
        assert not is_any_of(x, iterable)


class Test_is_dict_of_sequences:
    @pytest.mark.parametrize('correct_type', [{'a': []}, {'a': ()}])
    def test_True(self, correct_type):
        assert is_dict_of_sequences(correct_type)

    @pytest.mark.parametrize('wrong_type', [1, 1.0, True, False, None, object(), {}, iter([]), map(lambda x: x, []), [()], ([], ), {'a': {}}])
    def test_False(self, wrong_type):
        assert not is_dict_of_sequences(wrong_type)


class Test_is_dict_of_sequences_uniform:
    def test_True(self):
        assert is_dict_of_sequences_uniform({'a': (), 'b': ()})
        assert is_dict_of_sequences_uniform({'a': [1], 'b': [1]})
        assert is_dict_of_sequences_uniform({'a': (1, 2, 3), 'b': [10, 20, 30]})

    def test_False(self):
        assert not is_dict_of_sequences_uniform({'a': [1], 'b': [1, 2]})
        assert not is_dict_of_sequences_uniform({'a': [1], 'b': []})
        assert not is_dict_of_sequences_uniform({'a': [1], 'b': [1], 'c': [1, 2]})


class Test_is_equal:
    @pytest.mark.parametrize('a, b', [
        (0, False),
        (0, None),
        (False, None),
        (1, True),
        (0, 1),
        (1, '1'),
    ])
    def test_False(self, a, b):
        assert not is_equal(a, b)

    @pytest.mark.parametrize('a, b', [
        (0, 0),
        (1, 1),
        (False, False),
        (True, True),
        (None, None),
    ])
    def test_True(self, a, b):
        assert is_equal(a, b)


class Test_is_generator:
    @pytest.mark.parametrize('correct_type', [_generator()])
    def test_True(self, correct_type):
        assert is_generator(correct_type)

    @pytest.mark.parametrize('wrong_type', [iter([]), map(bool, []), 1, 1.0, True, False, None, 'string', object(), range(1)])
    def test_False(self, wrong_type):
        assert not is_generator(wrong_type)


class Test_is_iterable:
    @pytest.mark.parametrize('correct_type', [[], set(), (), {}, {}.keys(), {}.values(), {}.items(), range(1), iter([]), map(lambda x: x, [])])
    def test_True(self, correct_type):
        assert is_iterable(correct_type)

    @pytest.mark.parametrize('wrong_type', [1, 1.0, True, False, None, '', bytes('', 'utf-8'), bytearray('', 'utf-8'), object()])
    def test_False(self, wrong_type):
        assert not is_iterable(wrong_type)


class Test_is_iterable_or_str:
    @pytest.mark.parametrize('correct_type', ['', bytes('', 'utf-8'), bytearray('', 'utf-8'), [], set(), (), {}, range(1), iter([]), map(lambda x: x, [])])
    def test_True(self, correct_type):
        assert is_iterable_or_str(correct_type)

    @pytest.mark.parametrize('wrong_type', [1, 1.0, True, False, None, object()])
    def test_False(self, wrong_type):
        assert not is_iterable_or_str(wrong_type)


class Test_is_iterator:
    @pytest.mark.parametrize('correct_type', [iter([]), map(bool, []), _generator()])
    def test_True(self, correct_type):
        assert is_iterator(correct_type)

    @pytest.mark.parametrize('wrong_type', [1, 1.0, True, False, None, 'string', object(), range(1)])
    def test_False(self, wrong_type):
        assert not is_iterator(wrong_type)


class Test_is_none_of:
    @pytest.mark.parametrize('wrong_type', [object(), 1, True, False, None, ''])
    def test_not_iterable(self, wrong_type):
        with pytest.raises(TypeError):
            is_none_of([], haystack=wrong_type)

    @pytest.mark.parametrize('x, iterable', [
        (0, [1, 2, 3]),
        (4, [1, 2, 3]),
        ('a', {'b': 'a', 'c': 'd'}),
        ({}, [1, 2, 3]),
        (True, {1, None, False}),
    ])
    def test_True(self, x, iterable):
        assert is_none_of(x, iterable)

    @pytest.mark.parametrize('x, iterable', [
        (2, [1, 2, 3]),
        ('a', {'a': 'b', 'c': 'd'}),
        ({}, [1, 2, {}, 3]),
        (True, {None, True, False}),
    ])
    def test_False(self, x, iterable):
        assert not is_none_of(x, iterable)

    @pytest.mark.parametrize('x, iterable', [
        (1, [True, False]),
        (0, [True, False]),
        (True, [0, 1]),
        (False, [0, 1]),
    ])
    def test_bools_are_not_ints(self, x, iterable):
        assert is_none_of(x, iterable)


class Test_is_primitive:
    @pytest.mark.parametrize('correct_type', [1, 1.0, True, False, 'string', None])
    def test_True(self, correct_type):
        assert is_primitive(correct_type)

    @pytest.mark.parametrize('wrong_type', [[], set(), (), {}, object()])
    def test_False(self, wrong_type):
        assert not is_primitive(wrong_type)


class Test_is_sequence:
    @pytest.mark.parametrize('correct_type', [[], (), range(1)])
    def test_True(self, correct_type):
        assert is_sequence(correct_type)

    @pytest.mark.parametrize('wrong_type', [1, 1.0, True, False, None, '', bytes('', 'utf-8'), bytearray('', 'utf-8'), object(), {}, iter([]), map(lambda x: x, [])])
    def test_False(self, wrong_type):
        assert not is_sequence(wrong_type)


class Test_is_sequence_of_dicts:
    @pytest.mark.parametrize('correct_type', [[{}], ({}, )])
    def test_True(self, correct_type):
        assert is_sequence_of_dicts(correct_type)

    @pytest.mark.parametrize('wrong_type', [1, 1.0, True, False, None, object(), {}, iter([]), map(lambda x: x, []), [()], ([], ), {'a': []}])
    def test_False(self, wrong_type):
        assert not is_sequence_of_dicts(wrong_type)


class Test_is_sequence_of_dicts_uniform:
    def test_True(self):
        assert is_sequence_of_dicts_uniform([{}, {}])
        assert is_sequence_of_dicts_uniform([{'a': 1}, {'a': 2}])
        assert is_sequence_of_dicts_uniform([{'b': 1, 'a': 1}, {'a': 2, 'b': 2}])

    def test_False(self):
        assert not is_sequence_of_dicts_uniform([{'a': 1}, {'b': 2}])
        assert not is_sequence_of_dicts_uniform([{'a': 1, 'b': 1}, {'b': 2}])


class Test_is_sequence_of_sequences:
    @pytest.mark.parametrize('correct_type', [[[]], [()], ([], ), ((), )])
    def test_True(self, correct_type):
        assert is_sequence_of_sequences(correct_type)

    @pytest.mark.parametrize('wrong_type', [1, 1.0, True, False, None, object(), {}, iter([]), map(lambda x: x, []), [{}], {'a': []}])
    def test_False(self, wrong_type):
        assert not is_sequence_of_sequences(wrong_type)


class Test_is_sequence_of_sequences_uniform:
    def test_True(self):
        assert is_sequence_of_sequences_uniform([[], []])
        assert is_sequence_of_sequences_uniform([
            ['a', 'b', 'c'],
            ['x', 'y', 'z'],
            [1, 2, 3],
            [True, False, None]
        ])

    def test_False(self):
        assert not is_sequence_of_sequences_uniform([[], [1]])
        assert not is_sequence_of_sequences_uniform([['a', 'b', 'c'], ['x', 'y']])


class Test_is_sequence_or_str:
    @pytest.mark.parametrize('correct_type', [[], (), range(1), '', bytes('', 'utf-8'), bytearray('', 'utf-8')])
    def test_True(self, correct_type):
        assert is_sequence_or_str(correct_type)

    @pytest.mark.parametrize('wrong_type', [1, 1.0, True, False, None, object(), {}, iter([]), map(lambda x: x, [])])
    def test_False(self, wrong_type):
        assert not is_sequence_or_str(wrong_type)


class Test_is_singleton:
    @pytest.mark.parametrize('correct_type', [True, False, None])
    def test_True(self, correct_type):
        assert is_singleton(correct_type)

    @pytest.mark.parametrize('wrong_type', ['string', 1, 1.0, [], set(), (), {}, object(), _generator, range(1)])
    def test_False(self, wrong_type):
        assert not is_singleton(wrong_type)
