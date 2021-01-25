import os
import pickle
from multiprocessing import Pool

import driftmlp
from driftmlp.rotations import random_ll_rot
from driftmlp.drifter_indexing.discrete_system import h3_default
import gc
file = os.environ['DRIFTFILE']

drogue_setting = [True, False, None]

res=3
def make_default(drogue, res = 3):
    discretizer = h3_default(res)
    drift_kwargs = {'variables': ['position', 'drogue', 'datetime'],
                    'drop_na': False,
                    'drogue': drogue}
    net = driftmlp.network_from_file(
        fname=file, drift_kwargs=drift_kwargs, store_story=True, discretizer=discretizer)
    net['discretizer'] = None
    return net


# Run all 3 at the same time. they need about 1.5gb ram each to run.
# So change this to a lower nuumber if you have <8gb ram.
net = make_default(True)
pickle.dump(net, open("DefaultNetwork.p", 'wb'))
p = Pool(3)

to_store = list(p.map(make_default, drogue_setting))
dict_of_networks = {drogue: net for drogue,
                    net in zip(drogue_setting, to_store)}
pickle.dump(dict_of_networks, open(f'default_networks.p', 'wb'))
del dict_of_networks
del to_store
gc.collect()
def get_res_4(drogue):
    return make_default(drogue, res=4)

to_store = list(p.map(get_res_4, drogue_setting))
dict_of_networks = {drogue: net for drogue,
                    net in zip(drogue_setting, to_store)}
pickle.dump(dict_of_networks, open(f'default_networks_res4.p', 'wb'))
p.close()
