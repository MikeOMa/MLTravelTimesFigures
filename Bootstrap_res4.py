import pickle
import driftmlp
import pandas as pd
from driftmlp.drifter_indexing.discrete_system import h3_default
import numpy as np
np.random.seed(55)
import os
file = os.environ['DRIFTFILE']
import time
from multiprocessing import Pool
discretizer = h3_default(res=4)

stations = np.loadtxt("locations.txt", delimiter=',')
stations = pd.DataFrame(stations, index=range(1, 8))
stations.columns = ['Longitude', 'Latitude']
### Loads in a list of 100 rotation networks 
origins = [stations.iloc[i].loc[['Longitude', 'Latitude']].to_list() for i in range(stations.shape[0])]

from shapely.geometry import Point

def path_and_df(network):
    discretizer = h3_default(res=4, rot=network['rotation'])
    try:
        indices = discretizer.return_inds(origins)
        paths = [driftmlp.shortest_path.get_all_paths(network, src, indices) for src in  indices]
    except:
        return None
    ##We didn't store all the gpd dataframes originally as its' costly memorywise
    rot = network['rotation']
    return {'paths':paths, 'rot':rot}

h3_sys = driftmlp.drifter_indexing.discrete_system.h3_default(res=4)
drift_kwargs = {'variables': ['position', 'drogue', 'datetime'],
                    'drop_na': False,
                    'drogue': True}
print("Making Stories")
start =time.time()
drift_iter = driftmlp.drifter_indexing.driftiter.generator(file)(**drift_kwargs)
story = driftmlp.drifter_indexing.story.get_story(drift_iter, discretizer) 
end = time.time()
print(end-start)
print("Made Stories, now getting paths")
start = time.time()
np.random.seed(100)
seeds = np.random.randint(0,10000,size=100)

def get_bootstrap_paths(seed):
    np.random.seed(seed)
    n = len(story)
    indicies = np.random.randint(0, n, size=n, dtype=int).tolist()
    stories_boot = [story[i] for i in indicies]
    boot_net = driftmlp.form_network.make_transition(stories_boot, day_cut_off=5, observations_per_day=4)
    boot_net['rotation'] = None
    paths = path_and_df(boot_net)
    return paths

p = Pool(10)
boot_paths = list(p.map(get_bootstrap_paths, seeds))
p.close()
print (start- time.time())
pickle.dump(boot_paths, open(f'boot_res_4_{len(boot_paths)}.p','wb'))
