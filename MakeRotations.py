import os
import pickle
from multiprocessing import Pool

import driftmlp
from driftmlp.rotations import random_ll_rot
from driftmlp.drifter_indexing.discrete_system import h3_default
import numpy as np

p = Pool(18)
seed=10
np.random.seed(seed)
rotations = [random_ll_rot() for i in range(100)]  #
file = os.environ['DRIFTFILE']
res=4
discretizer = h3_default(res=res)

def get_network(rot):
    drift_kwargs = {'variables': ['position', 'drogue', 'datetime'],
                    'drop_na': False,
                    'drogue': True,
                    'lon_lat_transform': rot}
    net = DriftMLP.network_from_file(fname=file, drift_kwargs=drift_kwargs, discretizer = discretizer, visual=False)
    net['discretizer'] = None
    print(net['gpd'])
    return net


to_store = list(p.map(get_network, rotations))
pickle.dump(to_store, open(f'rotations_{len(rotations)}_{res}_{seed}.p', 'wb'))
p.close()
