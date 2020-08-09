import os
import pickle
from multiprocessing import Pool

import DriftMLP
from DriftMLP.rotations import random_ll_rot

file = os.environ['DRIFTFILE']

drogue_setting = [True, False, None]


def make_default(drogue):
    drift_kwargs = {'variables': ['position', 'drogue', 'datetime'],
                    'drop_na': False,
                    'drogue': drogue}
    net = DriftMLP.network_from_file(
        fname=file, drift_kwargs=drift_kwargs, store_story=True)
    return net


# Run all 3 at the same time. they need about 1.5gb ram each to run.
# So change this to a lower nuumber if you have <8gb ram.
p = Pool(3)
to_store = list(p.map(make_default, drogue_setting))
dict_of_networks = {drogue: net for drogue,
                    net in zip(drogue_setting, to_store)}
pickle.dump(dict_of_networks, open(f'default_networks.p', 'wb'))
p.close()
