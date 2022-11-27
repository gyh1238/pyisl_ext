import requests
import json
import configparser
import time
from datetime import datetime
from skyfield.api import EarthSatellite
from skyfield.api import load
import numpy as np
from k_means_constrained import KMeansConstrained
import numpy as np

################################################################################
class MyError(Exception):
    def __init___(self,args):
        Exception.__init__(self,"my exception was raised with arguments {0}".format(args))
        self.args = args
uriBase                = "https://www.space-track.org"
requestLogin           = "/ajaxauth/login"
requestCmdAction       = "/basicspacedata/query"
requestFindStarlinks   = "/class/tle_latest/NORAD_CAT_ID/>40000/ORDINAL/1/OBJECT_NAME/STARLINK~~/DECAYED/0/format/tle/orderby/NORAD_CAT_ID%20asc"
requestOMMStarlink1    = "/class/omm/NORAD_CAT_ID/"
requestOMMStarlink2    = "/orderby/EPOCH%20asc/format/json"
config = configparser.ConfigParser()
config.read("./SLTrack.ini")
configUsr = config.get("configuration","username")
configPwd = config.get("configuration","password")
siteCred = {'identity': configUsr, 'password': configPwd}
with requests.Session() as session:
    resp = session.post(uriBase + requestLogin, data = siteCred)
    if resp.status_code != 200:
        raise MyError(resp, "POST fail on login")
    resp = session.get(uriBase + requestCmdAction + requestFindStarlinks)
    if resp.status_code != 200:
        print(resp)
        raise MyError(resp, "GET fail on request for Starlink satellites")
    session.close()
ALL_TLE_DATA = resp.text
################################################################################

################################################################################
ALL_TLE_DATA = ALL_TLE_DATA.split('\r\n')

ts = load.timescale()
sat_list = []
for i in range(int(len(ALL_TLE_DATA) / 2)):
    sat_list.append(EarthSatellite(ALL_TLE_DATA[2*i], ALL_TLE_DATA[2*i + 1], str(i) + 'th STARLINK', ts))
print(sat_list)

t_00 = ts.now()
geo_list_t00 = []
for i in range(int(len(sat_list))):
    geo_list_t00.append(sat_list[i].at(t_00))
pos_list_t00 = []
vel_list_t00 = []
for i in range(int(len(sat_list))):
    pos_list_t00.append(geo_list_t00[i].position.km)
    vel_list_t00.append(geo_list_t00[i].velocity.km_per_s)

t_10 = t_00 + 0.0069444 #10 min
geo_list_t10 = []
for i in range(int(len(sat_list))):
    geo_list_t10.append(sat_list[i].at(t_10))
pos_list_t10 = []
vel_list_t10 = []
for i in range(int(len(sat_list))):
    pos_list_t10.append(geo_list_t10[i].position.km)
    vel_list_t10.append(geo_list_t10[i].velocity.km_per_s)

t_20 = t_10 + 0.0069444 #10 min
geo_list_t20 = []
for i in range(int(len(sat_list))):
    geo_list_t20.append(sat_list[i].at(t_20))
pos_list_t20 = []
vel_list_t20 = []
for i in range(int(len(sat_list))):
    pos_list_t20.append(geo_list_t20[i].position.km)
    vel_list_t20.append(geo_list_t20[i].velocity.km_per_s)

t_30 = t_20 + 0.0069444 #10 min
geo_list_t30 = []
for i in range(int(len(sat_list))):
    geo_list_t30.append(sat_list[i].at(t_30))
pos_list_t30 = []
vel_list_t30 = []
for i in range(int(len(sat_list))):
    pos_list_t30.append(geo_list_t30[i].position.km)
    vel_list_t30.append(geo_list_t30[i].velocity.km_per_s)

t_40 = t_30 + 0.0069444 #10 min
geo_list_t40 = []
for i in range(int(len(sat_list))):
    geo_list_t40.append(sat_list[i].at(t_40))
pos_list_t40 = []
vel_list_t40 = []
for i in range(int(len(sat_list))):
    pos_list_t40.append(geo_list_t40[i].position.km)
    vel_list_t40.append(geo_list_t40[i].velocity.km_per_s)

# t_50 = t_40 + 0.0069444 #10 min
t_50 = t_40 + 0.00416664 #6 min
geo_list_t50 = []
for i in range(int(len(sat_list))):
    geo_list_t50.append(sat_list[i].at(t_50))
pos_list_t50 = []
vel_list_t50 = []
for i in range(int(len(sat_list))):
    pos_list_t50.append(geo_list_t50[i].position.km)
    vel_list_t50.append(geo_list_t50[i].velocity.km_per_s)

t_60 = t_50 + 0.0069444 #10 min
geo_list_t60 = []
for i in range(int(len(sat_list))):
    geo_list_t60.append(sat_list[i].at(t_60))
pos_list_t60 = []
vel_list_t60 = []
for i in range(int(len(sat_list))):
    pos_list_t60.append(geo_list_t60[i].position.km)
    vel_list_t60.append(geo_list_t60[i].velocity.km_per_s)
################################################################################

X_00 = np.array(pos_list_t00[:2048])
X_10 = np.array(pos_list_t10[:2048])
X_20 = np.array(pos_list_t20[:2048])
X_30 = np.array(pos_list_t30[:2048])
X_40 = np.array(pos_list_t40[:2048])
X_50 = np.array(pos_list_t50[:2048])
X_60 = np.array(pos_list_t60[:2048])

clf = KMeansConstrained(
    n_clusters=12,
    size_min=165,
    size_max=175,
    random_state=0
)

#find head
prediction = clf.fit_predict(X_00)
centers = clf.cluster_centers_
centers_idx = []
for center in centers:
    X_temp = X_00 - center
    X_temp2 = []
    for dis in X_temp:
        X_temp2.append(np.linalg.norm(dis))
    centers_idx.append(X_temp2.index(min(X_temp2)))

#00
cluster_mean_distance= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cluster_number = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
X_distance_temp = []
X_distance = []
for i in range(2048):
    X_distance_temp.append(X_00[i] - X_00[centers_idx[prediction[i]]])
for i in range(2048):
    X_distance.append(np.linalg.norm(X_distance_temp[i]))
for i in range(2048):
    cluster_mean_distance[prediction[i]] = cluster_mean_distance[prediction[i]] + X_distance[i]
    cluster_number[prediction[i]] = cluster_number[prediction[i]] + 1
for i in range(12):
    cluster_mean_distance[i] = cluster_mean_distance[i] / cluster_number[i]
print(cluster_mean_distance)

#10
cluster_mean_distance= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cluster_number = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
X_distance_temp = []
X_distance = []
for i in range(2048):
    X_distance_temp.append(X_10[i] - X_10[centers_idx[prediction[i]]])
for i in range(2048):
    X_distance.append(np.linalg.norm(X_distance_temp[i]))
for i in range(2048):
    cluster_mean_distance[prediction[i]] = cluster_mean_distance[prediction[i]] + X_distance[i]
    cluster_number[prediction[i]] = cluster_number[prediction[i]] + 1
for i in range(12):
    cluster_mean_distance[i] = cluster_mean_distance[i] / cluster_number[i]
print(cluster_mean_distance)

#20
cluster_mean_distance= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cluster_number = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
X_distance_temp = []
X_distance = []
for i in range(2048):
    X_distance_temp.append(X_20[i] - X_20[centers_idx[prediction[i]]])
for i in range(2048):
    X_distance.append(np.linalg.norm(X_distance_temp[i]))
for i in range(2048):
    cluster_mean_distance[prediction[i]] = cluster_mean_distance[prediction[i]] + X_distance[i]
    cluster_number[prediction[i]] = cluster_number[prediction[i]] + 1
for i in range(12):
    cluster_mean_distance[i] = cluster_mean_distance[i] / cluster_number[i]
print(cluster_mean_distance)

#30
cluster_mean_distance= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cluster_number = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
X_distance_temp = []
X_distance = []
for i in range(2048):
    X_distance_temp.append(X_30[i] - X_30[centers_idx[prediction[i]]])
for i in range(2048):
    X_distance.append(np.linalg.norm(X_distance_temp[i]))
for i in range(2048):
    cluster_mean_distance[prediction[i]] = cluster_mean_distance[prediction[i]] + X_distance[i]
    cluster_number[prediction[i]] = cluster_number[prediction[i]] + 1
for i in range(12):
    cluster_mean_distance[i] = cluster_mean_distance[i] / cluster_number[i]
print(cluster_mean_distance)

#40
cluster_mean_distance= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cluster_number = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
X_distance_temp = []
X_distance = []
for i in range(2048):
    X_distance_temp.append(X_40[i] - X_40[centers_idx[prediction[i]]])
for i in range(2048):
    X_distance.append(np.linalg.norm(X_distance_temp[i]))
for i in range(2048):
    cluster_mean_distance[prediction[i]] = cluster_mean_distance[prediction[i]] + X_distance[i]
    cluster_number[prediction[i]] = cluster_number[prediction[i]] + 1
for i in range(12):
    cluster_mean_distance[i] = cluster_mean_distance[i] / cluster_number[i]
print(cluster_mean_distance)

#50
cluster_mean_distance= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cluster_number = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
X_distance_temp = []
X_distance = []
for i in range(2048):
    X_distance_temp.append(X_50[i] - X_50[centers_idx[prediction[i]]])
for i in range(2048):
    X_distance.append(np.linalg.norm(X_distance_temp[i]))
for i in range(2048):
    cluster_mean_distance[prediction[i]] = cluster_mean_distance[prediction[i]] + X_distance[i]
    cluster_number[prediction[i]] = cluster_number[prediction[i]] + 1
for i in range(12):
    cluster_mean_distance[i] = cluster_mean_distance[i] / cluster_number[i]
print(cluster_mean_distance)

#60
cluster_mean_distance= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cluster_number = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
X_distance_temp = []
X_distance = []
for i in range(2048):
    X_distance_temp.append(X_60[i] - X_60[centers_idx[prediction[i]]])
for i in range(2048):
    X_distance.append(np.linalg.norm(X_distance_temp[i]))
for i in range(2048):
    cluster_mean_distance[prediction[i]] = cluster_mean_distance[prediction[i]] + X_distance[i]
    cluster_number[prediction[i]] = cluster_number[prediction[i]] + 1
for i in range(12):
    cluster_mean_distance[i] = cluster_mean_distance[i] / cluster_number[i]
print(cluster_mean_distance)

print(cluster_number)