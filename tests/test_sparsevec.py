import numpy as np
import pytest
from pgvector.utils import SparseVec, to_db_value


class TestSparseVec:
    def test_to_db_value(self):
        assert isinstance(to_db_value([1, 2, 3]), SparseVec)
        assert isinstance(to_db_value(np.array([1, 2, 3])), SparseVec)
        with pytest.raises(ValueError, match='expected sparsevec'):
            to_db_value(1)

    def test_from_dense(self):
        assert SparseVec.from_dense([1, 2, 3]).indices == [0, 1, 2]
        assert SparseVec.from_dense([1, 2, 3]).values == [1, 2, 3]
        assert SparseVec.from_dense(np.array([1, 2, 3])).indices == [0, 1, 2]
        assert SparseVec.from_dense(np.array([1, 2, 3])).values == [1, 2, 3]

    def test_to_dense(self):
        assert np.array_equal(SparseVec(3, [0, 2], [1, 2]).to_dense(), [1, 0, 2])
        assert np.array_equal(SparseVec(3, [0, 1, 2], [1, 2, 3]).to_dense(), [1, 2, 3])

    def test_to_db(self):
        assert SparseVec(3, [0, 2], [1, 2]).to_db(3) == '{1:1,3:2}/3'
        assert SparseVec(3, [0, 1, 2], [1, 2, 3]).to_db(3) == '{1:1,2:2,3:3}/3'

    def test_to_db_binary(self):
        bin_value = b'\x00\x00\x00\x03\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02?\x80\x00\x00@\x00\x00\x00@@\x00\x00'
        assert SparseVec(3, [0, 1, 2], [1, 2, 3]).to_db_binary() == bin_value

    def test_from_db(self):
        assert SparseVec.from_db(None) is None
        assert SparseVec.from_db('{1:1,2:2,3:3}/3').indices == [0, 1, 2]
        assert SparseVec.from_db('{1:1,2:2,3:3}/3').values == [1, 2, 3]

    def test_from_db_binary(self):
        bin_value = b'\x00\x00\x00\x03\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02?\x80\x00\x00@\x00\x00\x00@@\x00\x00'
        assert SparseVec.from_db_binary(None) is None
        assert SparseVec.from_db_binary(bin_value).indices == [0, 1, 2]
        assert SparseVec.from_db_binary(bin_value).values == [1, 2, 3]
        