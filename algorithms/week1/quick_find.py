import pytest
from itertools import permutations, chain


class UnionFind:
    def __init__(self, n):
        self.data = [i for i in range(n)]
        self.size = n

    def are_connected(self, p, q):
        return self.data[p] == self.data[q]

    def union(self, p, q):
        if self.are_connected(p, q):
            return

        q_component = [i for i, element in enumerate(self.data) if element == self.data[q]]
        for i in q_component:
            self.data[i] = self.data[p]


@pytest.fixture
def size():
    return 5


@pytest.fixture
def union(size):
    return UnionFind(size)


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
