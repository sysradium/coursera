import pytest
from itertools import permutations, chain


class UnionUnion:
    def __init__(self, n):
        self.forest = [i for i in range(n)]
        self.size = n

    def get_root(self, p):
        while p != self.forest[p]:
            p = self.forest[p]
        return p

    def are_connected(self, p, q):
        return self.get_root(p) == self.get_root(q)

    def union(self, p, q):
        p_root, q_root = self.get_root(p), self.get_root(q)
        self.forest[p_root] = q_root


@pytest.fixture
def size():
    return 5


@pytest.fixture
def union(size):
    return UnionUnion(size)


def test_by_default_every_is_itself_a_root(union):
    for i in range(union.size):
        assert union.get_root(i) == i


@pytest.mark.parametrize('p, q', permutations(range(size()), 2))
def test_by_default_everyting_isnt_connected(union, p, q):
    assert not union.are_connected(p, q)


@pytest.mark.parametrize('p, q', zip(range(size()), range(size())))
def test_items_are_connected_with_itself(union, p, q):
    assert union.are_connected(p, q)


@pytest.mark.parametrize('p, q', permutations(range(size()), 2))
def test_after_one_union_two_elemnts_are_connected(union, p, q):
    union.union(p, q)
    assert union.are_connected(p, q)


@pytest.mark.parametrize('p, q', permutations(range(size()), 2))
def test_after_one_union_other_elements_are_still_not_connected(union, p, q):
    union.union(p, q)
    all_pairs, connected_pairs = set(permutations(range(union.size), 2)), {(p, q), (q, p)}

    for i, j in all_pairs - connected_pairs:
        assert not union.are_connected(i, j)


def test_when_any_elemnts_from_two_connected_components_connects_it_becomes_one_connected_components(union):
    connected_pairs = [[1, 4], [0, 3]]

    for p, q in connected_pairs:
        union.union(p, q)

    union.union(connected_pairs[0][0], connected_pairs[1][0])

    new_connected_component = chain.from_iterable(connected_pairs)
    for p, q in permutations(new_connected_component, 2):
        assert union.are_connected(p, q)

