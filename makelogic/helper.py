"""
Tiny little helper functions. Too small and independent to add anywhere else
"""


def no_duplicates(seq):
    """ Remove all duplicates from a sequence and preserve its order """

    # source: https://www.peterbe.com/plog/uniqifiers-benchmark
    # Author: Dave Kirby
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]
