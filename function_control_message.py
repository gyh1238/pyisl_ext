import numpy as np
import class_blockchain

#velocity of light - km/s
C_VEL = 3 * 10**5
#1 tick for sec
TICK_REAL = 10**(-4) # 100us -> 30km 0.0001
#message mode
IDV_SYNC_REQ = 0    #mod 0 indivisual sync request
IDV_SYNC_REP = 1    #mod 1 indivisual sync reply
LOC_SYNC_PRP = 2    #mod 2 locacl sync propagation
BLO_ELEC_REQ = 3    #mod 3 blo elec req
BLO_ELEC_REP_PRO = 4#mod 4 blo elec rep pros
BLO_ELEC_REP_CON = 5#mod 5 blo elec rep cons
BLO_PRP = 6         #mod 6 blo prp
#message structure
M_MODE = 0      #mode
M_TX = 1        #tx
M_RX = 2        #rx
M_DIS_ALL = 3   #distance(all)
M_DIS_NOW = 4   #distance(now)
M_SUGGEST = 5

def indivisual_sync_request(messages, tx_sat, rx_sat, sat_time_list, sat_pos_list, sat_name):
    messages = add_message(messages, IDV_SYNC_REP, rx_sat, tx_sat, sat_pos_list, sat_name)
    return messages, sat_time_list
def indivisual_sync_reply(messages, tx_sat, rx_sat, sat_time_list, sat_name):
    sat_time_list[sat_name.index(rx_sat)] = ( sat_time_list[sat_name.index(rx_sat)] + sat_time_list[sat_name.index(tx_sat)] ) / 2
    return messages, sat_time_list
def local_sync_propagation(messages, tx_sat, rx_sat, sat_time_list, sat_name):
    sat_time_list[sat_name.index(rx_sat)] = sat_time_list[sat_name.index(tx_sat)]
    return messages, sat_time_list
def block_election_reqest(messages, tx_sat, rx_sat, sat_time_list, sat_pos_list, suggest_sat, sat_local, sat_name, sat_credit):
    if class_blockchain.election_decision(suggest_sat, sat_local[sat_name.index(rx_sat)], sat_credit, sat_name):
        messages = add_message(messages, BLO_ELEC_REP_PRO, rx_sat, tx_sat, sat_pos_list)
    else:
        messages = add_message(messages, BLO_ELEC_REP_CON, rx_sat, tx_sat, sat_pos_list)
    return messages, sat_time_list
def block_election_reply_pros(messages, tx_sat, rx_sat, sat_delegate, sat_election):
    sat_election[sat_delegate.index(rx_sat)][0].append(tx_sat)
    return messages, sat_election
def block_election_reply_cons(messages, tx_sat, rx_sat, sat_delegate, sat_election):
    sat_election[sat_delegate.index(rx_sat)][1].append(tx_sat)
    return messages, sat_election
def block_propagation(messages, rx_sat, sat_name, sat_time_list, sat_chain_no):
    sat_chain_no[sat_name.index(rx_sat)] += 1
    return sat_chain_no
def my_error(error):
    print("error ouccured: " + str(error))
    print("press anything")
    input()
    return

def message_arrived(messages, mode, tx_sat, rx_sat, sat_time_list, sat_pos_list, sat_name):
    if mode == IDV_SYNC_REQ:
        return indivisual_sync_request(messages, tx_sat, rx_sat, sat_time_list, sat_pos_list, sat_name)
    elif mode == IDV_SYNC_REP:
        return indivisual_sync_reply(messages, tx_sat, rx_sat, sat_time_list, sat_name)
    elif mode == LOC_SYNC_PRP:
        return local_sync_propagation(messages, tx_sat, rx_sat, sat_time_list, sat_name)
    # elif mode == BLO_ELEC_REQ:
    #     return block_election_reqest(messages, tx_sat, rx_sat, sat_time_list, sat_pos_list, suggest_sat, sat_local, sat_name, sat_credit)
    # elif mode == BLO_ELEC_REP_PRO:
    #     return block_election_reply_pros(messages, tx_sat, rx_sat, sat_time_list)
    # elif mode == BLO_ELEC_REP_CON:
    #     return block_election_reply_cons(messages, tx_sat, rx_sat, sat_time_list)
    # elif mode == BLO_DELG_PRP:
    #     return block_deleglated_propagation(messages, tx_sat, rx_sat, sat_time_list)
    # elif mode == BLO_MEMB_PRP:
    #     return block_member_propagation(messages, tx_sat, rx_sat, sat_time_list)
    else:
        return my_error("Unknown Mode")

def update_message(messages, sat_time_list, sat_pos_list, sat_local, sat_name, sat_credit, sat_delegate, sat_election, sat_chain_no):
    for message in messages:
        message[M_DIS_NOW] += TICK_REAL * C_VEL
        if message[M_DIS_NOW] >= message[M_DIS_ALL]:
            if message[M_MODE] == BLO_ELEC_REQ:
                messages = block_election_reqest(messages, message[M_TX], message[M_RX], sat_time_list, sat_pos_list, message[M_SUGGEST], sat_local, sat_name, sat_credit)
            if message[M_MODE] == BLO_ELEC_REP_PRO:
                messages, sat_election = block_election_reply_pros(messages, message[M_TX], message[M_RX], sat_delegate, sat_election)
            if message[M_MODE] == BLO_ELEC_REP_CON:
                messages, sat_election = block_election_reply_cons(messages, message[M_TX], message[M_RX], sat_delegate, sat_election)
            if message[M_MODE] == BLO_PRP:
                sat_chain_no = block_propagation(messages, message[M_RX], sat_name, sat_time_list, sat_chain_no)
            else:
                messages, sat_time_list = message_arrived(messages, message[M_MODE], message[M_TX], message[M_RX], sat_time_list, sat_pos_list, sat_name)
            messages.remove(message)
    return messages, sat_time_list, sat_election, sat_chain_no

def add_message(messages, mode, tx_sat, rx_sat, sat_pos_list, sat_name, suggest_sat = 0):
    distance = np.linalg.norm(sat_pos_list[sat_name.index(tx_sat)] - sat_pos_list[sat_name.index(rx_sat)])
    messages.append([mode, tx_sat, rx_sat, distance, 0, suggest_sat])
    return messages