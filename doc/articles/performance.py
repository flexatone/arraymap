


import os
import sys
import timeit
import typing as tp
from itertools import repeat

import automap
from automap import AutoMap
from automap import FrozenAutoMap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.append(os.getcwd())



class MapProcessor:
    NAME = ''
    SORT = -1

    def __init__(self, array: np.ndarray):
        self.array = array
        self.list = array.tolist()
        self.faml = FrozenAutoMap(self.list)
        self.fama = FrozenAutoMap(self.array)
        self.d = dict(zip(self.list, range(len(self.list))))

#-------------------------------------------------------------------------------
class FAMLInstantiate(MapProcessor):
    NAME = 'FAM(L): instantiate'
    SORT = 0

    def __call__(self):
        fam = FrozenAutoMap(self.list)
        assert len(fam) == len(self.list)

class FAMAInstantiate(MapProcessor):
    NAME = 'FAM(A), instantiate'
    SORT = 0

    def __call__(self):
        fam = FrozenAutoMap(self.array)
        assert len(fam) == len(self.list)

class DictInstantiate(MapProcessor):
    NAME = 'Dict, instantiate'
    SORT = 0

    def __call__(self):
        d = dict(zip(self.list, range(len(self.list))))
        assert len(d) == len(self.list)

#-------------------------------------------------------------------------------
class FAMLLookup(MapProcessor):
    NAME = 'FAM(L): lookup'
    SORT = 0

    def __call__(self):
        for k in self.list:
            _ = self.faml[k]

class FAMALookup(MapProcessor):
    NAME = 'FAM(A), lookup'
    SORT = 0

    def __call__(self):
        for k in self.list:
            _ = self.fama[k]

class DictLookup(MapProcessor):
    NAME = 'Dict, lookup'
    SORT = 0

    def __call__(self):
        for k in self.list:
            _ = self.d[k]

#-------------------------------------------------------------------------------
class FAMLItems(MapProcessor):
    NAME = 'FAM(L): items'
    SORT = 0

    def __call__(self):
        for k, v in self.faml.items():
            pass

class FAMAItems(MapProcessor):
    NAME = 'FAM(A), items'
    SORT = 0

    def __call__(self):
        for k, v in self.fama.items():
            pass

class DictItems(MapProcessor):
    NAME = 'Dict, items'
    SORT = 0

    def __call__(self):
        for k, v in self.d.items():
            pass







#-------------------------------------------------------------------------------
NUMBER = 100

def seconds_to_display(seconds: float) -> str:
    seconds /= NUMBER
    if seconds < 1e-4:
        return f'{seconds * 1e6: .1f} (µs)'
    if seconds < 1e-1:
        return f'{seconds * 1e3: .1f} (ms)'
    return f'{seconds: .1f} (s)'


def plot_performance(frame):
    fixture_total = len(frame['fixture'].unique())
    cat_total = len(frame['size'].unique())
    processor_total = len(frame['cls_processor'].unique())
    fig, axes = plt.subplots(cat_total, fixture_total)

    # cmap = plt.get_cmap('terrain')
    cmap = plt.get_cmap('plasma')

    color = cmap(np.arange(processor_total) / processor_total)

    # category is the size of the array
    for cat_count, (cat_label, cat) in enumerate(frame.groupby('size')):
        for fixture_count, (fixture_label, fixture) in enumerate(
                cat.groupby('fixture')):
            ax = axes[cat_count][fixture_count]

            # set order
            fixture['sort'] = [f.SORT for f in fixture['cls_processor']]
            fixture = fixture.sort_values('sort')

            results = fixture['time'].values.tolist()
            names = [cls.NAME for cls in fixture['cls_processor']]
            # x = np.arange(len(results))
            names_display = names
            post = ax.bar(names_display, results, color=color)

            # density, position = fixture_label.split('-')
            # cat_label is the size of the array
            title = f'{cat_label:.0e}\n{fixture_label}'

            ax.set_title(title, fontsize=6)
            ax.set_box_aspect(0.6) # makes taller tan wide
            time_max = fixture['time'].max()
            ax.set_yticks([0, time_max * 0.5, time_max])
            ax.set_yticklabels(['',
                    seconds_to_display(time_max * .5),
                    seconds_to_display(time_max),
                    ], fontsize=6)
            # ax.set_xticks(x, names_display, rotation='vertical')
            ax.tick_params(
                    axis='x',
                    which='both',
                    bottom=False,
                    top=False,
                    labelbottom=False,
                    )

    fig.set_size_inches(9, 3.5) # width, height
    fig.legend(post, names_display, loc='center right', fontsize=8)
    # horizontal, vertical
    fig.text(.05, .96, f'AutoMap Performance: {NUMBER} Iterations', fontsize=10)
    fig.text(.05, .90, get_versions(), fontsize=6)

    fp = '/tmp/automap.png'
    plt.subplots_adjust(
            left=0.075,
            bottom=0.05,
            right=0.80,
            top=0.80,
            wspace=0.5, # width
            hspace=0.5,
            )
    # plt.rcParams.update({'font.size': 22})
    plt.savefig(fp, dpi=300)

    if sys.platform.startswith('linux'):
        os.system(f'eog {fp}&')
    else:
        os.system(f'open {fp}')


#-------------------------------------------------------------------------------

class FixtureFactory:
    NAME = ''

    @staticmethod
    def get_array(size: int) -> np.ndarray:
        raise NotImplementedError()

    @classmethod
    def get_label_array(cls, size: int) -> tp.Tuple[str, np.ndarray]:
        array = cls.get_array(size)
        return cls.NAME, array


class FFInt(FixtureFactory):
    NAME = 'int-64'

    @staticmethod
    def get_array(size: int) -> np.ndarray:
        array = np.arange(size)
        array.flags.writeable = False
        return array

class FFFloat(FixtureFactory):
    NAME = 'float-64'

    @staticmethod
    def get_array(size: int) -> np.ndarray:
        array = np.arange(size) / 0.5
        array.flags.writeable = False
        return array

class FFString(FixtureFactory):
    NAME = 'string-U4'

    @staticmethod
    def get_array(size: int) -> np.ndarray:
        array = np.array([hex(e) for e in range(size)])
        array.flags.writeable = False
        return array




def get_versions() -> str:
    import platform
    return f'OS: {platform.system()} / AutoMap / NumPy: {np.__version__}\n'


CLS_PROCESSOR = (
    FAMLInstantiate,
    FAMLLookup,
    FAMLItems,

    FAMAInstantiate,
    FAMALookup,
    FAMAItems,

    DictInstantiate,
    DictLookup,
    DictItems,

    )

CLS_FF = (
    FFInt,
    FFFloat,
    FFString,
)


def run_test():
    records = []
    for size in (1_000, 10_000, 100_000):
        for ff in CLS_FF:
            fixture_label, fixture = ff.get_label_array(size)
            for cls in CLS_PROCESSOR:
                runner = cls(fixture)

                record = [cls, NUMBER, fixture_label, size]
                print(record)
                try:
                    result = timeit.timeit(
                            f'runner()',
                            globals=locals(),
                            number=NUMBER)
                except OSError:
                    result = np.nan
                finally:
                    pass
                record.append(result)
                records.append(record)

    f = pd.DataFrame.from_records(records,
            columns=('cls_processor', 'number', 'fixture', 'size', 'time')
            )
    print(f)
    plot_performance(f)

if __name__ == '__main__':

    run_test()



