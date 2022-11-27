from k_means_constrained import KMeansConstrained
import numpy as np
import pickle
import class_sat_list

sat_list = class_sat_list.SatList(2048, 12, True)
sat_pos_temp = sat_list.sat_pos

print(sat_list.sat_name[0])
print(sat_list.sat_pos[0])
print(sat_list.sat_name[2])
print(sat_list.sat_pos[2])
print(sat_list.sat_name[1000])
print(sat_list.sat_pos[1000])
print(sat_list.sat_name[1500])
print(sat_list.sat_pos[1500])
print(sat_list.sat_name[2002])
print(sat_list.sat_pos[2002])
input()

sat_pos_temp[1] = sat_pos_temp[2]
sat_pos_temp[411] = sat_pos_temp[412]
X = np.array(sat_pos_temp)

clf = KMeansConstrained(
    n_clusters=12,
    size_min=165,
    size_max=175,
    random_state=0
)

prediction = clf.fit_predict(X)
centers = clf.cluster_centers_

centers_idx = []
for center in centers:
    X_temp = X - center
    X_temp2 = []
    for dis in X_temp:
        X_temp2.append(np.linalg.norm(dis))
    centers_idx.append(X_temp2.index(min(X_temp2)))

cluster_mean_distance= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cluster_number = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
X_distance_temp = []
X_distance = []
for i in range(2048):
    X_distance_temp.append(X[i] - X[centers_idx[prediction[i]]])
for i in range(2048):
    X_distance.append(np.linalg.norm(X_distance_temp[i]))
for i in range(2048):
    cluster_mean_distance[prediction[i]] = cluster_mean_distance[prediction[i]] + X_distance[i]
    cluster_number[prediction[i]] = cluster_number[prediction[i]] + 1
for i in range(12):
    cluster_mean_distance[i] = cluster_mean_distance[i] / cluster_number[i]

print(cluster_mean_distance)
print(cluster_number)
print(prediction)
print(centers)
print(centers_idx)

# f = open("./delegate_and_member2.txt", 'w')
# for i in range(2048):
#     my_name = sat_list.sat_name[i]
#     my_head_name = sat_list.sat_name[centers_idx[prediction[i]]]
#     f.write(str(my_head_name))
#     f.write(' ')
#     f.write(str(my_name))
#     f.write('\n')
# f.close()

# center_name = []
# for idx in centers_idx:
#     center_name.append(sat_list.sat_name[idx])
# with open("./data/STARLINK_CenterSat_temp", "wb") as fp:
#     pickle.dump(center_name, fp)
#
# with open("./data/STARLINK_POS_temp", "wb") as fp:
#     pickle.dump(X, fp)
#
# with open("./data/STARLINK_Center_temp", "wb") as fp:
#     pickle.dump(centers, fp)
#
# with open("./data/STARLINK_Cluster_temp", "wb") as fp:
#     pickle.dump(prediction, fp)

centers_pos = []
for idx in centers_idx:
    centers_pos.append(sat_list.sat_pos[idx])
print(centers_pos)

with open("./data/STARLINK_CenterSat_POS_temp", "wb") as fp:
    pickle.dump(centers_pos, fp)