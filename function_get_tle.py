import requests
import configparser
from skyfield.api import EarthSatellite
from skyfield.api import load

def get_sat_from_spacetrack(number_of_sat):
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
    ALL_TLE_DATA = ALL_TLE_DATA.split('\r\n')

    ts = load.timescale()
    earthsat_list = []
    for i in range(int(len(ALL_TLE_DATA) / 2)):
        earthsat_list.append(EarthSatellite(ALL_TLE_DATA[2*i], ALL_TLE_DATA[2*i + 1], str(i) + 'th STARLINK', ts))
    # print(sat_list)

    t_now = ts.now()
    geo_list = []
    pos_list = []
    vel_list = []
    for i in range(int(len(earthsat_list))):
        geo_list.append(earthsat_list[i].at(t_now))
    for i in range(int(len(earthsat_list))):
        pos_list.append(geo_list[i].position.km)
        vel_list.append(geo_list[i].velocity.km_per_s.tolist())
    name_list = []
    for i in range(int(len(earthsat_list))):
        name_list.append(earthsat_list[i].model.satnum)

    return earthsat_list[:number_of_sat], t_now, name_list[:number_of_sat], pos_list[:number_of_sat], vel_list[:number_of_sat]

def get_sat_from_text(number_of_sat):
    filePath = './STARLINK_TLE.txt'
    f=open(filePath, 'r')
    ALL_TLE_DATA = f.read()
    f.close()

    ALL_TLE_DATA = ALL_TLE_DATA.split('\n\n')

    ts = load.timescale()
    earthsat_list = []
    for i in range(int(len(ALL_TLE_DATA) / 2)):
        earthsat_list.append(EarthSatellite(ALL_TLE_DATA[2*i], ALL_TLE_DATA[2*i + 1], str(i) + 'th STARLINK', ts))
    # print(sat_list)

    # t_now = ts.now()
    t_fixed = ts.utc(2022, 9, 2, 6, 0, 0)
    # print(t_now.utc_strftime())
    # print(t_fixed.utc_strftime())

    geo_list = []
    pos_list = []
    vel_list = []
    for i in range(int(len(earthsat_list))):
        geo_list.append(earthsat_list[i].at(t_fixed))
    for i in range(int(len(earthsat_list))):
        pos_list.append(geo_list[i].position.km)
        vel_list.append(geo_list[i].velocity.km_per_s.tolist())
    name_list = []
    for i in range(int(len(earthsat_list))):
        name_list.append(earthsat_list[i].model.satnum)

    return earthsat_list[:number_of_sat], t_fixed, name_list[:number_of_sat], pos_list[:number_of_sat], vel_list[:number_of_sat]

def time_pass_sec(t_now, t_pass):
    t_now += t_pass / 86400
    return t_now

def get_sat_position_by_time(earthsat_list, time):
    pos_list = []
    geo_list = []
    for i in range(int(len(earthsat_list))):
        geo_list.append(earthsat_list[i].at(time))
    for i in range(int(len(earthsat_list))):
        pos_list.append(geo_list[i].position.km.tolist())
    return pos_list