def get_paddingc(vallen):
    if vallen % 4 == 0:
        return vallen
    else:
        return vallen + (4-vallen % 4)


def new_calc_padding(vallen):
    return (vallen + 3) & ~ 3


def get_paddingc2(vallen):
    return vallen + ((4-vallen) & 3)
