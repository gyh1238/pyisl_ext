import numpy as np
import time
import class_sat_list
import class_blockchain
# import get_tle_from_spacetrack
import function_control_message
import random
from k_means_constrained import KMeansConstrained

NUMBER_OF_SAT = 2048
NUMBER_OF_DELEGATE = 12

#sat
sat_list = class_sat_list.SatList(NUMBER_OF_SAT, NUMBER_OF_DELEGATE)

# total_degree = 0
# for i in range(NUMBER_OF_SAT):
#     total_degree += len(sat_list.sat_local[i])
# print(total_degree)
# input()

#blockchain

#messages
messages= []

# # find delegate
X = np.array(sat_list.sat_pos)
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

#
# # delegate credit
for i, delegate_sat_idx in enumerate(centers_idx):
    sat_list.sat_delegate[i] = sat_list.sat_name[delegate_sat_idx]
    sat_list.sat_credit[delegate_sat_idx] += 100
    for sat_delegate_local in sat_list.sat_local[delegate_sat_idx]:
        sat_list.sat_credit[sat_list.sat_name.index(sat_delegate_local)] += 50

# sat_list.sat_credit = np.random.randint(100, 200, size=(NUMBER_OF_SAT))

ticks = 1
while True:
    # time update
    sat_list.update_time(1)
    sat_list.update_delegate_time(ticks)
    # print(sat_list.sat_time)

    #message policy
    #200 -> 0.02s
    #1000 -> 0.1s
    #10000 -> 1s
    #100000 -> 10s
    # # message test
    # if ticks == 2:
    #     function_control_message.add_message(messages,
    #                                          function_control_message.IDV_SYNC_REQ,
    #                                          sat_list.sat_name[0],
    #                                          sat_list.sat_name[1],
    #                                          sat_list.sat_pos,
    #                                          sat_list.sat_name,
    #                                          )

    # random local
    temp_sat = ticks % NUMBER_OF_SAT
    # for temp_sat in range(0, 2048):
    if sat_list.sat_local[temp_sat]:
        # print(temp_sat)
        # print(sat_list.sat_name[temp_sat])
        # print(sat_list.sat_local[temp_sat])
        # print(random.choice(sat_list.sat_local[temp_sat]))
        # input()
        function_control_message.add_message(messages,
                                             function_control_message.IDV_SYNC_REQ,
                                             sat_list.sat_name[temp_sat],
                                             random.choice(sat_list.sat_local[temp_sat]),
                                             sat_list.sat_pos,
                                             sat_list.sat_name,
                                             )

    # local sum
    # temp_sat = ticks % NUMBER_OF_SAT
    # # for temp_sat in range(0, 2048):
    # if sat_list.sat_local[temp_sat]:
    #     for temp_sat_local in sat_list.sat_local[temp_sat]:
    #         # print(temp_sat)
    #         # print(sat_list.sat_name[temp_sat])
    #         # print(sat_list.sat_local[temp_sat])
    #         # print(temp_sat_local)
    #         # input()
    #         function_control_message.add_message(messages,
    #                                              function_control_message.IDV_SYNC_REQ,
    #                                              sat_list.sat_name[temp_sat],
    #                                              temp_sat_local,
    #                                              sat_list.sat_pos,
    #                                              sat_list.sat_name,
    #                                              )

    # # # credit random
    # temp_sat = ticks % NUMBER_OF_SAT
    # if sat_list.sat_local[temp_sat]:
    #     credit_local = []
    #     for sat in sat_list.sat_local[temp_sat]:
    #         credit_local.append(sat_list.sat_credit[sat_list.sat_name.index(sat)])
    #     max_credit_local = max(credit_local)
    #     max_credit_local_index = credit_local.index(max_credit_local)
    #
    #     function_control_message.add_message(messages,
    #                                          function_control_message.IDV_SYNC_REQ,
    #                                          sat_list.sat_name[temp_sat],
    #                                          sat_list.sat_local[temp_sat][max_credit_local_index],
    #                                          sat_list.sat_pos,
    #                                          sat_list.sat_name,
    #                                          )

    # credit reinforce
    # temp_sat = ticks % NUMBER_OF_SAT
    # # sat_list.sat_time[temp_sat] = ticks * 0.0001
    # # temp_sat2 = (ticks + 1024) % NUMBER_OF_SAT
    # # sat_list.sat_time[temp_sat2] = ticks * 0.0001
    # if sat_list.sat_local[temp_sat]:
    #     random.shuffle(sat_list.sat_local[temp_sat])
    #     credit_local = []
    #     for sat in sat_list.sat_local[temp_sat]:
    #         credit_local.append(sat_list.sat_credit[sat_list.sat_name.index(sat)])
    #     max_credit_local = max(credit_local)
    #     max_credit_local_index = credit_local.index(max_credit_local)
    #     local_max = sat_list.sat_local[temp_sat][max_credit_local_index]
    #
    #     function_control_message.add_message(messages,
    #                                          function_control_message.IDV_SYNC_REQ,
    #                                          sat_list.sat_name[temp_sat],
    #                                          local_max,
    #                                          sat_list.sat_pos,
    #                                          sat_list.sat_name,
    #                                          )
    #     sat_list.sat_credit[sat_list.sat_name.index(local_max)] += 10
    #
    # temp_sat2 = (ticks + 128) % NUMBER_OF_SAT
    # if sat_list.sat_local[temp_sat2]:
    #     credit_local = []
    #     for sat in sat_list.sat_local[temp_sat2]:
    #         credit_local.append(sat_list.sat_credit[sat_list.sat_name.index(sat)])
    #     max_credit_local = max(credit_local)
    #     max_credit_local_index = credit_local.index(max_credit_local)
    #
    #     function_control_message.add_message(messages,
    #                                          function_control_message.IDV_SYNC_REQ,
    #                                          sat_list.sat_name[temp_sat2],
    #                                          sat_list.sat_local[temp_sat2][max_credit_local_index],
    #                                          sat_list.sat_pos,
    #                                          sat_list.sat_name,
    #                                          )
    #     local_max = sat_list.sat_local[temp_sat2][max_credit_local_index]
    #     sat_list.sat_credit[sat_list.sat_name.index(local_max)] += 10
    #
    # temp_sat3 = (ticks + 256) % NUMBER_OF_SAT
    # if sat_list.sat_local[temp_sat3]:
    #     credit_local = []
    #     for sat in sat_list.sat_local[temp_sat3]:
    #         credit_local.append(sat_list.sat_credit[sat_list.sat_name.index(sat)])
    #     max_credit_local = max(credit_local)
    #     max_credit_local_index = credit_local.index(max_credit_local)
    #
    #     function_control_message.add_message(messages,
    #                                          function_control_message.IDV_SYNC_REQ,
    #                                          sat_list.sat_name[temp_sat3],
    #                                          sat_list.sat_local[temp_sat3][max_credit_local_index],
    #                                          sat_list.sat_pos,
    #                                          sat_list.sat_name,
    #                                          )
    #     local_max = sat_list.sat_local[temp_sat3][max_credit_local_index]
    #     sat_list.sat_credit[sat_list.sat_name.index(local_max)] += 10
    #
    # temp_sat4 = (ticks + 384) % NUMBER_OF_SAT
    # if sat_list.sat_local[temp_sat4]:
    #     credit_local = []
    #     for sat in sat_list.sat_local[temp_sat4]:
    #         credit_local.append(sat_list.sat_credit[sat_list.sat_name.index(sat)])
    #     max_credit_local = max(credit_local)
    #     max_credit_local_index = credit_local.index(max_credit_local)
    #
    #     function_control_message.add_message(messages,
    #                                          function_control_message.IDV_SYNC_REQ,
    #                                          sat_list.sat_name[temp_sat4],
    #                                          sat_list.sat_local[temp_sat4][max_credit_local_index],
    #                                          sat_list.sat_pos,
    #                                          sat_list.sat_name,
    #                                          )
    #     local_max = sat_list.sat_local[temp_sat4][max_credit_local_index]
    #     sat_list.sat_credit[sat_list.sat_name.index(local_max)] += 10
    #
    # temp_sat5 = (ticks + 512) % NUMBER_OF_SAT
    # if sat_list.sat_local[temp_sat5]:
    #     credit_local = []
    #     for sat in sat_list.sat_local[temp_sat5]:
    #         credit_local.append(sat_list.sat_credit[sat_list.sat_name.index(sat)])
    #     max_credit_local = max(credit_local)
    #     max_credit_local_index = credit_local.index(max_credit_local)
    #
    #     function_control_message.add_message(messages,
    #                                          function_control_message.IDV_SYNC_REQ,
    #                                          sat_list.sat_name[temp_sat5],
    #                                          sat_list.sat_local[temp_sat5][max_credit_local_index],
    #                                          sat_list.sat_pos,
    #                                          sat_list.sat_name,
    #                                          )
    #     local_max = sat_list.sat_local[temp_sat5][max_credit_local_index]
    #     sat_list.sat_credit[sat_list.sat_name.index(local_max)] += 10
    #
    # temp_sat6 = (ticks + 640) % NUMBER_OF_SAT
    # if sat_list.sat_local[temp_sat6]:
    #     credit_local = []
    #     for sat in sat_list.sat_local[temp_sat6]:
    #         credit_local.append(sat_list.sat_credit[sat_list.sat_name.index(sat)])
    #     max_credit_local = max(credit_local)
    #     max_credit_local_index = credit_local.index(max_credit_local)
    #
    #     function_control_message.add_message(messages,
    #                                          function_control_message.IDV_SYNC_REQ,
    #                                          sat_list.sat_name[temp_sat6],
    #                                          sat_list.sat_local[temp_sat6][max_credit_local_index],
    #                                          sat_list.sat_pos,
    #                                          sat_list.sat_name,
    #                                          )
    #     local_max = sat_list.sat_local[temp_sat6][max_credit_local_index]
    #     sat_list.sat_credit[sat_list.sat_name.index(local_max)] += 10
    #
    # temp_sat7 = (ticks + 768) % NUMBER_OF_SAT
    # if sat_list.sat_local[temp_sat7]:
    #     credit_local = []
    #     for sat in sat_list.sat_local[temp_sat7]:
    #         credit_local.append(sat_list.sat_credit[sat_list.sat_name.index(sat)])
    #     max_credit_local = max(credit_local)
    #     max_credit_local_index = credit_local.index(max_credit_local)
    #
    #     function_control_message.add_message(messages,
    #                                          function_control_message.IDV_SYNC_REQ,
    #                                          sat_list.sat_name[temp_sat7],
    #                                          sat_list.sat_local[temp_sat7][max_credit_local_index],
    #                                          sat_list.sat_pos,
    #                                          sat_list.sat_name,
    #                                          )
    #     local_max = sat_list.sat_local[temp_sat7][max_credit_local_index]
    #     sat_list.sat_credit[sat_list.sat_name.index(local_max)] += 10
    #
    # temp_sat8 = (ticks + 896) % NUMBER_OF_SAT
    # if sat_list.sat_local[temp_sat8]:
    #     credit_local = []
    #     for sat in sat_list.sat_local[temp_sat8]:
    #         credit_local.append(sat_list.sat_credit[sat_list.sat_name.index(sat)])
    #     max_credit_local = max(credit_local)
    #     max_credit_local_index = credit_local.index(max_credit_local)
    #
    #     function_control_message.add_message(messages,
    #                                          function_control_message.IDV_SYNC_REQ,
    #                                          sat_list.sat_name[temp_sat8],
    #                                          sat_list.sat_local[temp_sat8][max_credit_local_index],
    #                                          sat_list.sat_pos,
    #                                          sat_list.sat_name,
    #                                          )
    #     local_max = sat_list.sat_local[temp_sat8][max_credit_local_index]
    #     sat_list.sat_credit[sat_list.sat_name.index(local_max)] += 10
    #
    # temp_sat9 = (ticks + 1024) % NUMBER_OF_SAT
    # if sat_list.sat_local[temp_sat9]:
    #     credit_local = []
    #     for sat in sat_list.sat_local[temp_sat9]:
    #         credit_local.append(sat_list.sat_credit[sat_list.sat_name.index(sat)])
    #     max_credit_local = max(credit_local)
    #     max_credit_local_index = credit_local.index(max_credit_local)
    #
    #     function_control_message.add_message(messages,
    #                                          function_control_message.IDV_SYNC_REQ,
    #                                          sat_list.sat_name[temp_sat9],
    #                                          sat_list.sat_local[temp_sat9][max_credit_local_index],
    #                                          sat_list.sat_pos,
    #                                          sat_list.sat_name,
    #                                          )
    #     local_max = sat_list.sat_local[temp_sat9][max_credit_local_index]
    #     sat_list.sat_credit[sat_list.sat_name.index(local_max)] += 10

    #message update
    messages, sat_list.sat_time, sat_list.sat_election, sat_list.sat_chain_no = \
        function_control_message.update_message(messages,
                                                sat_list.sat_time,
                                                sat_list.sat_pos,
                                                sat_list.sat_local,
                                                sat_list.sat_name,
                                                sat_list.sat_credit,
                                                sat_list.sat_delegate,
                                                sat_list.sat_election,
                                                sat_list.sat_chain_no,
                                                )
    #ticks
    ticks += 1

    # print(sat_list.sat_name)
    # print(sat_list.sat_time)
    # print(messages)
    # input()

    #for test
    if ticks % 100 == 0:
        print("ticks: ", ticks)
        print(np.std(sat_list.sat_time))
        print(np.mean(sat_list.sat_time))
        print(np.max(sat_list.sat_time))

    if ticks % 20000 == 0:
        # print(sat_list.sat_credit )
        input()