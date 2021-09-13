
import time
from multiprocessing import Pool 
## driftmlp is the package implementing this methodology
import driftmlp
## h3 to convert locations to their h3 indices.
## Where possible we use driftmlp.helpers.return_h3_inds()
import h3.api.basic_int as h3
import driftmlp.drifter_indexing.discrete_system as dds
## core python packages
import os
import numpy as np #
import pandas as pd
import pickle
import gc

from driftmlp import DefaultSystem


def discrete_sensetivity(discretizer):
    drift_iter = driftmlp.drifter_indexing.driftiter.generator(os.environ["DRIFTFILE"])(**drift_kwargs)
    stories = driftmlp.drifter_indexing.story.get_story(drift_iter, discretizer= discretizer) 
    dis_inds = discretizer.return_inds([i[['Longitude', 'Latitude']].to_list() for _,i in stations.iterrows()])
    final_tt = {}
    print("Currently running")
    print(discretizer.res)
    for times in trial_cut_offs:
        if times%5 == 0:
            print(times)
        network = driftmlp.form_network.make_transition(stories, times, 4)
        final_tt[times] = driftmlp.shortest_path.AllPairwisePaths(network, dis_inds) 
    return final_tt
stations = np.loadtxt("locations.txt", delimiter=',')
stations = pd.DataFrame(stations, index=range(1, 8))
stations.columns = ['Longitude', 'Latitude']
stations['h3'] = DefaultSystem.return_inds([i[['Longitude', 'Latitude']].to_list() for _,i in stations.iterrows()])

trial_cut_offs = list(np.arange(0.5,14.0,0.5))

drift_kwargs = {'variables': ['position', 'drogue', 'datetime'],
                    'drop_na': False,
                    'drogue': True}
print("Making Stories")
start =time.time()
#trial_cut_offs = list(np.arange(2,40.0,2))



start = time.time()

discretizers = [dds.h3_default(res=3), dds.h3_default(res=4),
        dds.lon_lat_grid(0.5), dds.lon_lat_grid(1), dds.lon_lat_grid(1.5)]
res=  list(map(discrete_sensetivity, discretizers))
pickle.dump(res, open("Sensitivity_gridtime.p", 'wb'))
print(time.time()-start)
