"""
AMMM Lab Heuristics
Instance file validator (Priority Assignment Version)
"""

from AMMMGlobals import AMMMException

# Validate instance attributes read from a DAT file.
# It checks only format and structure, not feasibility.
# Use instance.checkInstance() for feasibility validation.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Required parameter: N (number of members)
        if 'N' not in data.__dict__:
            raise AMMMException('Parameter N (number of members) is missing from input data.')

        N = data.N
        if not isinstance(N, int) or N <= 0:
            raise AMMMException('N must be a positive integer.')

        # Required parameter: m (NxN bid matrix)
        if 'm' not in data.__dict__:
            raise AMMMException('Parameter m (bid matrix) is missing from input data.')

        m = data.m
        if not isinstance(m, list) or len(m) != N:
            raise AMMMException('Bid matrix m must be a list with N rows.')

        for i, row in enumerate(m):
            if not isinstance(row, list) or len(row) != N:
                raise AMMMException(f'Row {i} of bid matrix m must contain exactly N={N} elements.')
            for j, val in enumerate(row):
                if not isinstance(val, (int, float)) or val < 0:
                    raise AMMMException(f'Invalid bid value m[{i}][{j}] = {val}. Must be a non-negative number.')
