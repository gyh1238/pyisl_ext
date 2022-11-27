import numpy as np
import function_get_tle

OSC_HZ = 40 * 10**6 # 40MHz
OSC_STD = OSC_HZ * 0.5 * 10**(-6) # 20Hz
TICK_REAL = 10**(-4) # 100us

class SatList:
    number_of_sat = 0
    number_of_delegate_sat = 0
    time_now = 0
    sat_name = []
    sat_fmax = []
    sat_time = []
    sat_pos = []
    sat_local = []
    sat_credit = []
    sat_chain_no = []
    sat_delegate = []
    sat_election = []

    def __init__(self, NumberOfSat, NumberOfDelegateSat, FromText = False):
        self.number_of_sat = NumberOfSat
        self.number_of_delegate_sat = NumberOfDelegateSat
        for i in range(self.number_of_sat):
            # self.sat_name.append(0)
            self.sat_time.append(0)
            self.sat_fmax.append(3)
            # self.sat_pos.append([0, 0, 0])
            self.sat_local.append([])
            self.sat_credit.append(0)
            self.sat_chain_no.append(0)
        for i in range(self.number_of_delegate_sat):
            self.sat_delegate.append(0)
            self.sat_election.append([[], []])
        if FromText:
            _, self.time_now, self.sat_name, self.sat_pos, _ = function_get_tle.get_sat_from_text(self.number_of_sat)
        else:
            _, self.time_now, self.sat_name, self.sat_pos, _ = function_get_tle.get_sat_from_spacetrack(self.number_of_sat)


        self.update_local(self.sat_name, self.sat_pos)
        self.initialization_time()

    def initialization_time(self):
        for i in range(self.number_of_sat):
            # idv_time = np.random.uniform(-3.3, 3.3)
            idv_time = np.random.uniform(-6.6, 6.6)
            idv_time *= 10 ** (-10)
            self.sat_time[i] = idv_time

    def update_time(self, ticks):
        for i in range(self.number_of_sat):
            # osc = np.random.normal(OSC_HZ * ticks, OSC_STD * ticks) / ticks
            # osc = np.random.uniform(OSC_HZ - 20, OSC_HZ + 20) / ticks
            osc = np.random.uniform(OSC_HZ - self.sat_fmax[i], OSC_HZ + self.sat_fmax[i]) / ticks
            self.sat_time[i] += (OSC_HZ / osc) * TICK_REAL * ticks

    def update_delegate_time(self, ticks):
        for delegate_sat in self.sat_delegate:
            self.sat_time[self.sat_name.index(delegate_sat)] = TICK_REAL * ticks

    def update_pos(self):
        self.time_now = function_get_tle.time_pass_sec(self.time_now, 1)
        self.sat_pos = function_get_tle.get_sat_position_by_time(self.time_now)

    def update_local(self, name_list, pos_list):
        self.sat_local = []
        for i in range(self.number_of_sat):
            self.sat_local.append([])

        for i in range(self.number_of_sat):
            sat_pos_temp1 = pos_list - pos_list[i]
            sat_pos_temp2 = [np.linalg.norm(x) for x in sat_pos_temp1]
            for j, dis in enumerate(sat_pos_temp2):
                if 1 < dis < 1000:
                    self.sat_local[i].append(name_list[j])

    def update_credit(self, update_sat, update_value):
        self.sat_credit[self.sat_name.index(update_sat)] += update_value

    def update_chain_no(self, update_sat):
        self.sat_chain_no[self.sat_name.index(update_sat)] += 1