def _init(_q):
    global q
    q = _q


def _type_num_is_numeric(typenum):
    if typenum >= 4 and typenum <=9:
        return True
    return False


def _get_numeric_only_subtable(tab):
    t = q('0#0!', tab)
    cols = q.cols(t).py()
    numeric_cols = []
    for c in cols:
        if _type_num_is_numeric(t[c].t):
            numeric_cols.append(c)
    return tab[numeric_cols]


class PandasMeta:
    # Dataframe properties
    @property
    def columns(self):
        return q('{if[99h~type x; x:value x]; cols x}', self).py()

    @property
    def dtypes(self):
        return q('{0#x}', self).pd().dtypes

    @property
    def empty(self):
        return q('{0~count x}', self).py()

    @property
    def ndim(self):
        return q('{if[99h~type x; x:value x]; count cols x}', self).py()

    @property
    def shape(self):
        return tuple(q('{if[99h~type x; x:value x]; (count x; count cols x)}', self).py())

    @property
    def size(self):
        return q('{count[x] * count[cols x]}', self).py()

    def mean(self, axis: int = 0, numeric_only: bool = False):
        tab = self
        if 'Keyed' in str(type(tab)):
            tab = q('{(keys x) _ 0!x}', tab)
        if numeric_only:
            tab = _get_numeric_only_subtable(tab)

        key_str = '' if axis == 0 else '`$string '
        val_str = '' if axis == 0 else '"f"$value '
        query_str = 'cols tab' if axis == 0 else 'til count tab'
        where_str = ' where not (::)~/:r[;1]'
        return q(
            '{[tab]'
            f'r:{{[tab; x] ({key_str}x; avg {val_str}tab[x])}}[tab;] each {query_str};'
            f'(,/) {{(enlist x 0)!(enlist x 1)}} each r{where_str}}}',
            tab
        )

    def median(self, axis: int = 0, numeric_only: bool = False):
        tab = self
        if 'Keyed' in str(type(tab)):
            tab = q('{(keys x) _ 0!x}', tab)
        if numeric_only:
            tab = _get_numeric_only_subtable(tab)

        key_str = '' if axis == 0 else '`$string '
        val_str = '' if axis == 0 else '"f"$value '
        query_str = 'cols tab' if axis == 0 else 'til count tab'
        where_str = ' where not (::)~/:r[;1]'
        return q(
            '{[tab]'
            f'r:{{[tab; x] ({key_str}x; med {val_str}tab[x])}}[tab;] each {query_str};'
            f'(,/) {{(enlist x 0)!(enlist x 1)}} each r{where_str}}}',
            tab
        )

    def mode(self, axis: int = 0, numeric_only: bool = False, dropna: bool = True):
        tab = self
        if 'Keyed' in str(type(tab)):
            tab = q('{(keys x) _ 0!x}', tab)
        if numeric_only:
            tab = _get_numeric_only_subtable(tab)
        x_str = 'x: x where not null x; ' if dropna else ''
        query_str = 'cols tab' if axis == 0 else 'til count tab'
        cols_str = 'tab[x]' if axis == 0 else 'value tab[x]'
        maxc_str = 'x[1]' if axis ==0 else 'raze x _ 0'
        cs_str = 'cols tab' if axis == 0 else '`idx,`$string each til count r[0][1]'
        m_str = '{1 _ raze x}' if axis == 0 else '{x: raze x; x iasc null x}'
        flip_m = 'flip ' if axis == 0 else ''
        mode_query = f'{{{x_str}(x l) where d=max d:1_deltas (l:where differ x),count x:asc x}}' \
            if numeric_only else f'{{{x_str}x where f=max f:@[0*i;i:x?x;+;1]}}'
        return q(
            '{[tab]'
            f'r:{{[tab; x] (x; {mode_query}'
            f'[{cols_str}])}}[tab;] each {query_str};'
            f'maxc: max {{count {maxc_str}}} each r;'
            'r:{[x; y] $[not y=t:count x 1;'
            '[qq: x 1; (x 0;(y - t){[z; t]z,z[t]}[;t]/qq)];'
            '(x 0; x 1)]}[;maxc] each r;'
            f'cs: {cs_str};'
            f'm: {m_str} each r;'
            f'cs !/: {flip_m}m}}',
            tab
        )
