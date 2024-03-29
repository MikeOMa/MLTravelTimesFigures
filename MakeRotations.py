import os
import pickle
from multiprocessing import Pool

import driftmlp
from driftmlp.rotations import random_ll_rot
from driftmlp.drifter_indexing.discrete_system import h3_default
import numpy as np

RES=4
file = os.environ['DRIFTFILE']
def get_network(rot):

    discretizer = h3_default(res=RES)
    drift_kwargs = {'variables': ['position', 'drogue', 'datetime'],
                    'drop_na': False,
                    'drogue': True,
                    'lon_lat_transform': rot}
    net = driftmlp.network_from_file(fname=file, drift_kwargs=drift_kwargs, discretizer = discretizer, visual=False)
    net['discretizer'] = None
    return net


p = Pool(18)
SEED=10
np.random.seed(SEED)
rotations = [random_ll_rot() for i in range(30)] 



to_store = list(p.map(get_network, rotations))
pickle.dump(to_store, open(f'rotations_{len(rotations)}_{RES}_{SEED}.p', 'wb'))
p.close()
