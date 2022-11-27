import numpy as np

class block:
    time_stamp = 0
    prev_hash = 0
    mod_no = 0
    group_no = 0
    member_credit = 0
    witness = 0

class block_chain:
    blockchain = []

    def add_block(self):
        new_block = block()
        self.blockchain.append(new_block)

def election_decision(suggest_sat, sat_local, sat_credit, sat_name):
    credible_sats = find_credible_sats(sat_local, sat_credit, sat_name)
    if suggest_sat == credible_sats:
        return True
    else:
        return False

def find_credible_sats(sat_local, sat_credit, sat_name):
    credit_local = []
    credit_local_name = []
    for sat in sat_local:
        credit_local.append(sat_credit[sat_name.index(sat)])
        credit_local_name.append(sat)
    max_credit_local = max(credit_local)
    return credit_local_name[credit_local.index(max_credit_local)]