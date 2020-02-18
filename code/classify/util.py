import numpy as np

def flip(l, ref):
    assert len(l) == len(ref)
    ref_zeros = len(l) - np.count_nonzero(ref)
    zeros = ref_zeros - np.count_nonzero(l[:ref_zeros])
    print(f"ref_zeros, zeros = {ref_zeros}, {zeros}")
    if zeros / ref_zeros >= 0.5:
        return l
    def flip_(l_):
        if l_ == 0:
            return 1
        if l_ == 1:
            return 0
        return l_
    return list(map(flip_, l))
