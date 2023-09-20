# Import required packages #
import pandas as pd
import numpy as np
import os

path= "C:\\Users\\qiyu\\OneDrive - Chalmers\\Road Data"
os.chdir(path)

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter

# Supress scientific notation while printing #
pd.options.display.float_format = '{:.2f}'.format

# Import ODYM dynamic stock model #
from dynamic_stock_model import DynamicStockModel as DSM

pd.set_option('mode.chained_assignment', None)

# Flags for different scenarios and set-ups#
flag_scale_sensitivity = 0  # 0 for default value, 1 for + standard error, 2 for - standard error #
flag_shape_sensitivity = 0  # 0 for default value, 1 for + standard error, 2 for - standard error #

flag_future = 1  # 0 for no new construction, 1 for mean new construction #

# set current directory
idx = pd.IndexSlice

# Load data #
# Read in file with pickle #
pickle_file_path = "C:\\Users\\qiyu\\OneDrive - Chalmers\\Road Data\\road_mfa.pkl"
road = pd.read_pickle(pickle_file_path)

# Load material intensity data, cited from Klimatkalky #
road_MI = pd.read_excel('Road_MI.xlsx', index_col=0)  # Material intensity CSV file for road #

# Group the data so that categories match the material intensity #
def conditions(row):  # iterating over rows in the data #
    two_lane = 8  # Cut off width for types of two lane road#
    one_lane = 5

    #  The logical order of if statements is very important#
    if (row['Slitlagertyp'] == "grus"):
        return "Gravel road"
    elif (row['Bredd'] <= one_lane):
        return "One lane road"
    elif (row['Bredd'] > one_lane) and (row['Bredd'] <= two_lane):
        return "Two lane road"
    elif row['Typ'] == "Infartsväg/Utfartsväg":
        return "One lane road"
    elif row['Typ'] == "Mötesfri väg":
        return "Meeting free road"
    elif row['Typ'] == "Motorväg":
        return "Highway"
    else:
        return "Two lane road"

road.loc[:, 'MI Category'] = road.apply(conditions, axis=1)   

# Group the data according to region #
def regions(row):  # iterating over rows in the data #  
    if row['lan'] in ("01", "09"):
        return "Stockholm"
    elif row['lan'] in ("20", "21", "23", "22"):
        return "Middle"
    elif row['lan'] in ("24", "25"):
        return "North"
    elif row['lan'] in ("06", "10", "07", "08", "12"):
        return "South"
    elif row['lan'] in ("13", "14", "17"):
        return "West"
    else:
        return "East"
    
road.loc[:, 'Region'] = road.apply(regions, axis=1)

# Add Weibull scale parameters to the model based on region#

if flag_scale_sensitivity == 0:
    def scale(row):  # iterating over rows in the data #
        if row['Region'] == "Middle":  # Middle #
            return 4.03 * np.exp(1.14)
        elif row['Region'] == "North":  # North #
            return 4.03 * np.exp(1.24)
        elif row['Region'] == "Stockholm":  # Stockholm #
            return 4.03 * np.exp(1)
        elif row['Region'] == "South":  # South #
            return 4.03 * np.exp(1.19)
        elif row['Region'] == "East":  # East #
            return 4.03 * np.exp(1.03)
        elif row['Region'] == "West":  # West #
            return 4.03 * np.exp(1.20)
        else:
            return 4.03 * np.exp(1.20)

elif flag_scale_sensitivity == 1:
    def scale(row):  # iterating over rows in the data #
        if row['Region'] == "Middle":  # Middle #
            return 4.03 * np.exp(1.14 + 0.14)
        elif row['Region'] == "North":  # North #
            return 4.03 * np.exp(1.24 + 0.24)
        elif row['Region'] == "Stockholm":  # Stockholm #
            return 4.03 * np.exp(1)
        elif row['Region'] == "South":  # South #
            return 4.03 * np.exp(1.19 + 0.19)
        elif row['Region'] == "East":  # East #
            return 4.03 * np.exp(1.03 + 0.03)
        elif row['Region'] == "West":  # West #
            return 4.03 * np.exp(1.20 + 0.2)
        else:
            return 4.03 * np.exp(1.20)

elif flag_scale_sensitivity == 2:
    def scale(row):  # iterating over rows in the data #
        if row['Region'] == "Middle":  # Middle #
            return 4.03 * np.exp(1.14 - 0.14)
        elif row['Region'] == "North":  # North #
            return 4.03 * np.exp(1.24 - 0.24)
        elif row['Region'] == "Stockholm":  # Stockholm #
            return 4.03 * np.exp(1)
        elif row['Region'] == "South":  # South #
            return 4.03 * np.exp(1.19 - 0.19)
        elif row['Region'] == "East":  # East #
            return 4.03 * np.exp(1.03 - 0.03)
        elif row['Region'] == "West":  # West #
            return 4.03 * np.exp(1.20 - 0.2)
        else:
            return 4.03 * np.exp(1.20)

road.loc[:, 'Scale'] = road.apply(scale, axis=1)

# Add Shape parameter #
if flag_shape_sensitivity == 0:
    def shapes(row):
        if row['Region'] == "Middle":  # Middle #
            return 3.0199
        elif row['Region'] == "North":  # North #
            return 3.0199
        elif row['Region'] == "Stockholm":  # Stockholm #
            return 3.0199
        elif row['Region'] == "South":  # South #
            return 3.0199
        elif row['Region'] == "East":  # East #
            return 3.0199
        else:  # West #
            return 3.0199

elif flag_shape_sensitivity == 1:
    def shapes(row):
        if row['Region'] == "Middle":  # Middle #
            return 3.1623
        elif row['Region'] == "North":  # North #
            return 3.1623
        elif row['Region'] == "Stockholm":  # Stockholm #
            return 3.1623
        elif row['Region'] == "South":  # South #
            return 3.1623
        elif row['Region'] == "East":  # East #
            return 3.1623
        else:  # West #
            return 3.1623

elif flag_shape_sensitivity == 2:
    def shapes(row):
        if row['Region'] == "Middle":  # Middle #
            return 2.884
        elif row['Region'] == "North":  # North #
            return 2.884
        elif row['Region'] == "Stockholm":  # Stockholm #
            return 2.884
        elif row['Region'] == "South":  # South #
            return 2.884
        elif row['Region'] == "East":  # East #
            return 2.884
        else:  # West #
            return 2.884

road.loc[:, 'Shape'] = road.apply(shapes, axis=1)

# Retrieve the material intensity values for stock calculation #
One_lane_road_MI = road_MI.loc[['One lane road']]
Highway_MI = road_MI.loc[['Highway']]
Two_lane_road_MI = road_MI.loc[['Two lane road']]
Meeting_free_road_MI = road_MI.loc[['Meeting free road']]
Gravel_road_MI = road_MI.loc[['Gravel road']]

def nonew(length):  # Create dataframe for future scenarios, for roads with multiple ownership #

    test = pd.concat([length]*36, ignore_index=True)

    l = [i for i in range(2010, 2046) for _ in range(3)] # Create a list of years for the new dataframe # 
    test['Construction year'] = l

    return test

def one_nonew(length):  # Create dataframe for future scenarios, for state owned roads #

    test = pd.concat([length]*36, ignore_index=True)

    year = np.arange(2010, 2046) # Create a list of years for the new dataframe # 
    test['Construction year'] = year

    return test

def two_nonew(length):  # Create dataframe for future scenarios, for state owned roads #

    test = pd.concat([length]*36, ignore_index=True)

    l = [i for i in range(2010, 2046) for _ in range(2)] # Create a list of years for the new dataframe # 
    test['Construction year'] = l

    return test

# Cumulatively sum up stocks of different types of roads and convert them into the format needed for MFA #
m_one_lane_m = road.loc[road['MI Category'] == 'One lane road']
m_one_lane_m = m_one_lane_m.loc[m_one_lane_m['Region'] == 'Middle']
m_one_lane_m['Stock'] = m_one_lane_m['Bredd'] * m_one_lane_m['Length']
m_one_lane_m  = m_one_lane_m .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_one_lane_m  = pd.DataFrame(m_one_lane_m )
m_one_lane_m .reset_index(inplace=True)
m_one_lane_m = nonew(m_one_lane_m)


m_one_lane_n = road.loc[road['MI Category'] == 'One lane road']
m_one_lane_n = m_one_lane_n.loc[m_one_lane_n['Region'] == 'North']
m_one_lane_n['Stock'] = m_one_lane_n['Bredd'] * m_one_lane_n['Length']
m_one_lane_n = m_one_lane_n.groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_one_lane_n = pd.DataFrame(m_one_lane_n)
m_one_lane_n.reset_index(inplace=True)
m_one_lane_n = nonew(m_one_lane_n)

m_one_lane_st = road.loc[road['MI Category'] == 'One lane road']
m_one_lane_st = m_one_lane_st.loc[m_one_lane_st['Region'] == 'Stockholm']
m_one_lane_st['Stock'] = m_one_lane_st['Bredd'] * m_one_lane_st['Length']
m_one_lane_st = m_one_lane_st.groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_one_lane_st = pd.DataFrame(m_one_lane_st)
m_one_lane_st.reset_index(inplace=True)
m_one_lane_st = nonew(m_one_lane_st)


m_one_lane_s = road.loc[road['MI Category'] == 'One lane road']
m_one_lane_s = m_one_lane_s.loc[m_one_lane_s['Region'] == 'South']
m_one_lane_s['Stock'] = m_one_lane_s['Bredd'] * m_one_lane_s['Length']
m_one_lane_s = m_one_lane_s.groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_one_lane_s = pd.DataFrame(m_one_lane_s)
m_one_lane_s.reset_index(inplace=True)
m_one_lane_s = nonew(m_one_lane_s)

m_one_lane_e = road.loc[road['MI Category'] == 'One lane road']
m_one_lane_e = m_one_lane_e.loc[m_one_lane_e['Region'] == 'East']
m_one_lane_e['Stock'] = m_one_lane_e['Bredd'] * m_one_lane_e['Length']
m_one_lane_e = m_one_lane_e.groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_one_lane_e = pd.DataFrame(m_one_lane_e)
m_one_lane_e.reset_index(inplace=True)
m_one_lane_e = nonew(m_one_lane_e)


m_one_lane_w = road.loc[road['MI Category'] == 'One lane road']
m_one_lane_w = m_one_lane_w.loc[m_one_lane_w['Region'] == 'West']
m_one_lane_w['Stock'] = m_one_lane_w['Bredd'] * m_one_lane_w['Length']
m_one_lane_w = m_one_lane_w .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_one_lane_w = pd.DataFrame(m_one_lane_w)
m_one_lane_w.reset_index(inplace=True)
m_one_lane_w = nonew(m_one_lane_w)

m_highway_m = road.loc[road['MI Category'] == 'Highway']
m_highway_m = m_highway_m.loc[m_highway_m['Region'] == 'Middle']
m_highway_m['Stock'] = m_highway_m['Bredd'] * m_highway_m['Length']
m_highway_m = m_highway_m .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_highway_m = pd.DataFrame(m_highway_m)
m_highway_m.reset_index(inplace=True)
m_highway_m = one_nonew(m_highway_m)

m_highway_n = road.loc[road['MI Category'] == 'Highway']
m_highway_n = m_highway_n.loc[m_highway_n['Region'] == 'North']
m_highway_n['Stock'] = m_highway_n['Bredd'] * m_highway_n['Length']
m_highway_n = m_highway_n .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_highway_n = pd.DataFrame(m_highway_n)
m_highway_n.reset_index(inplace=True)
m_highway_n = one_nonew(m_highway_n)


m_highway_st = road.loc[road['MI Category'] == 'Highway']
m_highway_st = m_highway_st.loc[m_highway_st['Region'] == 'Stockholm']
m_highway_st['Stock'] = m_highway_st['Bredd'] * m_highway_st['Length']
m_highway_st = m_highway_st .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_highway_st = pd.DataFrame(m_highway_st)
m_highway_st.reset_index(inplace=True)
m_highway_st = nonew(m_highway_st)


m_highway_s = road.loc[road['MI Category'] == 'Highway']
m_highway_s = m_highway_s.loc[m_highway_s['Region'] == 'South']
m_highway_s['Stock'] = m_highway_s['Bredd'] * m_highway_s['Length']
m_highway_s = m_highway_s .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_highway_s = pd.DataFrame(m_highway_s)
m_highway_s.reset_index(inplace=True)
m_highway_s = nonew(m_highway_s)


m_highway_e = road.loc[road['MI Category'] == 'Highway']
m_highway_e = m_highway_e.loc[m_highway_e['Region'] == 'East']
m_highway_e['Stock'] = m_highway_e['Bredd'] * m_highway_e['Length']
m_highway_e = m_highway_e .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_highway_e = pd.DataFrame(m_highway_e)
m_highway_e.reset_index(inplace=True)
m_highway_e = one_nonew(m_highway_e)


m_highway_w = road.loc[road['MI Category'] == 'Highway']
m_highway_w = m_highway_w.loc[m_highway_w['Region'] == 'West']
m_highway_w['Stock'] = m_highway_w['Bredd'] * m_highway_w['Length']
m_highway_w = m_highway_w .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_highway_w = pd.DataFrame(m_highway_w)
m_highway_w.reset_index(inplace=True)
m_highway_w = two_nonew(m_highway_w)


m_two_m = road.loc[road['MI Category'] == 'Two lane road']
m_two_m = m_two_m.loc[m_two_m['Region'] == 'Middle']
m_two_m['Stock'] = m_two_m['Bredd'] * m_two_m['Length']
m_two_m = m_two_m .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_two_m = pd.DataFrame(m_two_m)
m_two_m.reset_index(inplace=True)
m_two_m = nonew(m_two_m)


m_two_n = road.loc[road['MI Category'] == 'Two lane road']
m_two_n = m_two_n.loc[m_two_n['Region'] == 'North']
m_two_n['Stock'] = m_two_n['Bredd'] * m_two_n['Length']
m_two_n = m_two_n .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_two_n = pd.DataFrame(m_two_n)
m_two_n.reset_index(inplace=True)
m_two_n = nonew(m_two_n)

m_two_st = road.loc[road['MI Category'] == 'Two lane road']
m_two_st = m_two_st.loc[m_two_st['Region'] == 'Stockholm']
m_two_st['Stock'] = m_two_st['Bredd'] * m_two_st['Length']
m_two_st = m_two_st .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_two_st = pd.DataFrame(m_two_st)
m_two_st.reset_index(inplace=True)
m_two_st = nonew(m_two_st)

m_two_s = road.loc[road['MI Category'] == 'Two lane road']
m_two_s = m_two_s.loc[m_two_s['Region'] == 'South']
m_two_s['Stock'] = m_two_s['Bredd'] * m_two_s['Length']
m_two_s = m_two_s .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_two_s = pd.DataFrame(m_two_s)
m_two_s.reset_index(inplace=True)

m_two_s = nonew(m_two_s)

m_two_e = road.loc[road['MI Category'] == 'Two lane road']
m_two_e = m_two_e.loc[m_two_e['Region'] == 'East']
m_two_e['Stock'] = m_two_e['Bredd'] * m_two_e['Length']
m_two_e = m_two_e .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_two_e = pd.DataFrame(m_two_e)
m_two_e.reset_index(inplace=True)
m_two_e = nonew(m_two_e)


m_two_w = road.loc[road['MI Category'] == 'Two lane road']
m_two_w = m_two_w.loc[m_two_w['Region'] == 'West']
m_two_w['Stock'] = m_two_w['Bredd'] * m_two_w['Length']
m_two_w = m_two_w .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_two_w = pd.DataFrame(m_two_w)
m_two_w.reset_index(inplace=True)
m_two_w = nonew(m_two_w)


m_meet_m = road.loc[road['MI Category'] == 'Meeting free road']
m_meet_m = m_meet_m.loc[m_meet_m['Region'] == 'Middle']
m_meet_m['Stock'] = m_meet_m['Bredd'] * m_meet_m['Length']
m_meet_m = m_meet_m .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_meet_m = pd.DataFrame(m_meet_m)
m_meet_m.reset_index(inplace=True)
m_meet_m = one_nonew(m_meet_m)


m_meet_n = road.loc[road['MI Category'] == 'Meeting free road']
m_meet_n = m_meet_n.loc[m_meet_n['Region'] == 'North']
m_meet_n['Stock'] = m_meet_n['Bredd'] * m_meet_n['Length']
m_meet_n = m_meet_n .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_meet_n = pd.DataFrame(m_meet_n)
m_meet_n.reset_index(inplace=True)
m_meet_n = one_nonew(m_meet_n)


m_meet_st = road.loc[road['MI Category'] == 'Meeting free road']
m_meet_st = m_meet_st.loc[m_meet_st['Region'] == 'Stockholm']
m_meet_st['Stock'] = m_meet_st['Bredd'] * m_meet_st['Length']
m_meet_st = m_meet_st .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_meet_st = pd.DataFrame(m_meet_st)
m_meet_st.reset_index(inplace=True)
m_meet_st = two_nonew(m_meet_st)

m_meet_s = road.loc[road['MI Category'] == 'Meeting free road']
m_meet_s = m_meet_s.loc[m_meet_s['Region'] == 'South']
m_meet_s['Stock'] = m_meet_s['Bredd'] * m_meet_s['Length']
m_meet_s = m_meet_s .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_meet_s = pd.DataFrame(m_meet_s)
m_meet_s.reset_index(inplace=True)
m_meet_s = two_nonew(m_meet_s)


m_meet_e = road.loc[road['MI Category'] == 'Meeting free road']
m_meet_e = m_meet_e.loc[m_meet_e['Region'] == 'East']
m_meet_e['Stock'] = m_meet_e['Bredd'] * m_meet_e['Length']
m_meet_e = m_meet_e .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_meet_e = pd.DataFrame(m_meet_e)
m_meet_e.reset_index(inplace=True)
m_meet_e = one_nonew(m_meet_e)

m_meet_w = road.loc[road['MI Category'] == 'Meeting free road']
m_meet_w = m_meet_w.loc[m_meet_w['Region'] == 'West']
m_meet_w['Stock'] = m_meet_w['Bredd'] * m_meet_w['Length']
m_meet_w = m_meet_w .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_meet_w = pd.DataFrame(m_meet_w)
m_meet_w.reset_index(inplace=True)
m_meet_w = one_nonew(m_meet_w)


m_gravel_m = road.loc[road['MI Category'] == 'Gravel road']
m_gravel_m = m_gravel_m.loc[m_gravel_m['Region'] == 'Middle']
m_gravel_m['Stock'] = m_gravel_m['Bredd'] * m_gravel_m['Length']
m_gravel_m = m_gravel_m .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_gravel_m = pd.DataFrame(m_gravel_m)
m_gravel_m.reset_index(inplace=True)
m_gravel_m = nonew(m_gravel_m)

m_gravel_n = road.loc[road['MI Category'] == 'Gravel road']
m_gravel_n = m_gravel_n.loc[m_gravel_n['Region'] == 'North']
m_gravel_n['Stock'] = m_gravel_n['Bredd'] * m_gravel_n['Length']
m_gravel_n = m_gravel_n .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_gravel_n = pd.DataFrame(m_gravel_n)
m_gravel_n.reset_index(inplace=True)
m_gravel_n = nonew(m_gravel_n)


m_gravel_st = road.loc[road['MI Category'] == 'Gravel road']
m_gravel_st = m_gravel_st.loc[m_gravel_st['Region'] == 'Stockholm']
m_gravel_st['Stock'] = m_gravel_st['Bredd'] * m_gravel_st['Length']
m_gravel_st = m_gravel_st .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_gravel_st = pd.DataFrame(m_gravel_st)
m_gravel_st.reset_index(inplace=True)
m_gravel_st = nonew(m_gravel_st)


m_gravel_s = road.loc[road['MI Category'] == 'Gravel road']
m_gravel_s = m_gravel_s.loc[m_gravel_s['Region'] == 'South']
m_gravel_s['Stock'] = m_gravel_s['Bredd'] * m_gravel_s['Length']
m_gravel_s = m_gravel_s .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_gravel_s = pd.DataFrame(m_gravel_s)
m_gravel_s.reset_index(inplace=True)
m_gravel_s = nonew(m_gravel_s)


m_gravel_e = road.loc[road['MI Category'] == 'Gravel road']
m_gravel_e = m_gravel_e.loc[m_gravel_e['Region'] == 'East']
m_gravel_e['Stock'] = m_gravel_e['Bredd'] * m_gravel_e['Length']
m_gravel_e = m_gravel_e .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_gravel_e = pd.DataFrame(m_gravel_e)
m_gravel_e.reset_index(inplace=True)
m_gravel_e = nonew(m_gravel_e)

m_gravel_w = road.loc[road['MI Category'] == 'Gravel road']
m_gravel_w = m_gravel_w.loc[m_gravel_w['Region'] == 'West']
m_gravel_w['Stock'] = m_gravel_w['Bredd'] * m_gravel_w['Length']
m_gravel_w = m_gravel_w .groupby(["Vaghallartyp","Construction year","Scale","Shape"])["Stock"].sum()
m_gravel_w = pd.DataFrame(m_gravel_w)
m_gravel_w.reset_index(inplace=True)
m_gravel_w = nonew(m_gravel_w)

# define a function for calculating the road area inflow and outflow
def mfa(stock):  # stock is the different type of roads in different regions
    shape_list = stock.iloc[:, 3]
    scale_list = stock.iloc[:, 2]

    DSMforward = DSM(t=list(stock.iloc[:, 1]), s=np.array(stock.iloc[:, 4]),
                     lt={'Type': 'Weibull', 'Shape': shape_list.astype(float), 'Scale': scale_list.astype(float)})

    out_sc, out_oc, out_i = DSMforward.compute_stock_driven_model(NegativeInflowCorrect=True)

    # sum up the road outflow and stock and add years as index #
    out_oc[out_oc < 0] = 0
    out_oc = out_oc.sum(axis=1)
    out_oc = pd.DataFrame(out_oc, index=np.unique(stock['Construction year']))
    out_sc = out_sc.sum(axis=1)
    out_sc = pd.DataFrame(out_sc, index=np.unique(stock['Construction year']))
    out_i = pd.DataFrame(out_i, index=np.unique(stock['Construction year']))

    return out_sc, out_oc, out_i

# Road new construction needs be to distinguished from maintenance based on road type #
if flag_future == 0:
    p_new_construction = pd.read_excel('Road no new construction.xlsx', index_col=0)
    k_new_construction = pd.read_excel('Road no new construction.xlsx', index_col=0)
    s_new_construction = pd.read_excel('Road no new construction.xlsx', index_col=0)

else:
    p_new_construction = pd.read_excel('Road new mean.xlsx', sheet_name='State', index_col=0, header=None)
    k_new_construction = pd.read_excel('Road new mean.xlsx', sheet_name='Municipal', index_col=0, header=None)
    s_new_construction = pd.read_excel('Road new mean.xlsx', sheet_name='Private', index_col=0, header=None)

p_one_lane_new = p_new_construction.iloc[:, 0]
p_highway_new = p_new_construction.iloc[:, 3]
p_two_new = p_new_construction.iloc[:, 1]
p_meet_new = p_new_construction.iloc[:, 2]
p_gravel_new = p_new_construction.iloc[:, 4]

k_one_lane_new = k_new_construction.iloc[:, 0]
k_highway_new = k_new_construction.iloc[:, 3]
k_two_new = k_new_construction.iloc[:, 1]
k_meet_new = k_new_construction.iloc[:, 2]
k_gravel_new = k_new_construction.iloc[:, 4]

s_one_lane_new = s_new_construction.iloc[:, 0]
s_highway_new = s_new_construction.iloc[:, 3]
s_two_new = s_new_construction.iloc[:, 1]
s_meet_new = s_new_construction.iloc[:, 2]
s_gravel_new = s_new_construction.iloc[:, 4]

# MFA one lane roads #
# Privately owned #
p_one_lane_m = m_one_lane_m.loc[m_one_lane_m['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_one_lane_m['Stock'] = p_one_lane_m['Stock'] + p_one_lane_new.cumsum().reset_index(drop=True) /6
p_one_lane_n = m_one_lane_n.loc[m_one_lane_n['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_one_lane_n['Stock'] = p_one_lane_n['Stock'] + p_one_lane_new.cumsum().reset_index(drop=True) /6
p_one_lane_st = m_one_lane_st.loc[m_one_lane_st['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_one_lane_st['Stock'] = p_one_lane_st['Stock'] + p_one_lane_new.cumsum().reset_index(drop=True) /6
p_one_lane_s = m_one_lane_s.loc[m_one_lane_s['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_one_lane_s['Stock'] = p_one_lane_s['Stock'] + p_one_lane_new.cumsum().reset_index(drop=True) /6
p_one_lane_e = m_one_lane_e.loc[m_one_lane_e['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_one_lane_e['Stock'] = p_one_lane_e['Stock'] + p_one_lane_new.cumsum().reset_index(drop=True) /6
p_one_lane_w = m_one_lane_w.loc[m_one_lane_w['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_one_lane_w['Stock'] = p_one_lane_w['Stock'] + p_one_lane_new.cumsum().reset_index(drop=True) /6

p_one_lane_p_sc, p_one_lane_p_oc, p_one_lane_p_i = mfa(p_one_lane_m)
p_one_lane_n_sc, p_one_lane_n_oc, p_one_lane_n_i = mfa(p_one_lane_n)
p_one_lane_st_sc, p_one_lane_st_oc, p_one_lane_st_i = mfa(p_one_lane_st)
p_one_lane_s_sc, p_one_lane_s_oc, p_one_lane_s_i = mfa(p_one_lane_s)
p_one_lane_e_sc, p_one_lane_e_oc, p_one_lane_e_i = mfa(p_one_lane_e)
p_one_lane_w_sc, p_one_lane_w_oc, p_one_lane_w_i = mfa(p_one_lane_w)

# using pandas gymnastics to join all the frames together #
p_one_lane_road_sc = pd.concat(
    [p_one_lane_p_sc, p_one_lane_n_sc, p_one_lane_st_sc, p_one_lane_s_sc, p_one_lane_e_sc, p_one_lane_w_sc],
    axis=1).sort_index(ascending=True)
p_one_lane_road_sc = p_one_lane_road_sc.sum(axis=1)

p_one_lane_road_oc = pd.concat(
    [p_one_lane_p_oc, p_one_lane_n_oc, p_one_lane_st_oc, p_one_lane_s_oc, p_one_lane_e_oc, p_one_lane_w_oc],
    axis=1).sort_index(ascending=True)
p_one_lane_road_oc = p_one_lane_road_oc.sum(axis=1)

p_one_lane_road_i = pd.concat(
    [p_one_lane_p_i, p_one_lane_n_i, p_one_lane_st_i, p_one_lane_s_i, p_one_lane_e_i, p_one_lane_w_i],
    axis=1).sort_index(ascending=True)
p_one_lane_road_i = p_one_lane_road_i.sum(axis=1)

# Kommun owned #
k_one_lane_m = m_one_lane_m.loc[m_one_lane_m['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_one_lane_m['Stock'] = k_one_lane_m['Stock'] + k_one_lane_new.cumsum().reset_index(drop=True) /6
k_one_lane_n = m_one_lane_n.loc[m_one_lane_n['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_one_lane_n['Stock'] = k_one_lane_n['Stock'] + k_one_lane_new.cumsum().reset_index(drop=True) /6
k_one_lane_st = m_one_lane_st.loc[m_one_lane_st['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_one_lane_st['Stock'] = k_one_lane_st['Stock'] + k_one_lane_new.cumsum().reset_index(drop=True) /6
k_one_lane_s = m_one_lane_s.loc[m_one_lane_s['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_one_lane_s['Stock'] = k_one_lane_s['Stock'] + k_one_lane_new.cumsum().reset_index(drop=True) /6
k_one_lane_e = m_one_lane_e.loc[m_one_lane_e['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_one_lane_e['Stock'] = k_one_lane_e['Stock'] + k_one_lane_new.cumsum().reset_index(drop=True) /6
k_one_lane_w = m_one_lane_w.loc[m_one_lane_w['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_one_lane_w['Stock'] = k_one_lane_w['Stock'] + k_one_lane_new.cumsum().reset_index(drop=True) /6

k_one_lane_k_sc, k_one_lane_k_oc, k_one_lane_k_i = mfa(k_one_lane_m)
k_one_lane_n_sc, k_one_lane_n_oc, k_one_lane_n_i = mfa(k_one_lane_n)
k_one_lane_st_sc, k_one_lane_st_oc, k_one_lane_st_i = mfa(k_one_lane_st)
k_one_lane_s_sc, k_one_lane_s_oc, k_one_lane_s_i = mfa(k_one_lane_s)
k_one_lane_e_sc, k_one_lane_e_oc, k_one_lane_e_i = mfa(k_one_lane_e)
k_one_lane_w_sc, k_one_lane_w_oc, k_one_lane_w_i = mfa(k_one_lane_w)

# using pandas gymnastics to join all the frames together #
k_one_lane_road_sc = pd.concat(
    [k_one_lane_k_sc, k_one_lane_n_sc, k_one_lane_st_sc, k_one_lane_s_sc, k_one_lane_e_sc, k_one_lane_w_sc],
    axis=1).sort_index(ascending=True)
k_one_lane_road_sc = k_one_lane_road_sc.sum(axis=1)

k_one_lane_road_oc = pd.concat(
    [k_one_lane_k_oc, k_one_lane_n_oc, k_one_lane_st_oc, k_one_lane_s_oc, k_one_lane_e_oc, k_one_lane_w_oc],
    axis=1).sort_index(ascending=True)
k_one_lane_road_oc = k_one_lane_road_oc.sum(axis=1)

k_one_lane_road_i = pd.concat(
    [k_one_lane_k_i, k_one_lane_n_i, k_one_lane_st_i, k_one_lane_s_i, k_one_lane_e_i, k_one_lane_w_i],
    axis=1).sort_index(ascending=True)
k_one_lane_road_i = k_one_lane_road_i.sum(axis=1)

# State owned #
s_one_lane_m = m_one_lane_m.loc[m_one_lane_m['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_one_lane_m['Stock'] = s_one_lane_m['Stock'] + s_one_lane_new.cumsum().reset_index(drop=True) /6
s_one_lane_n = m_one_lane_n.loc[m_one_lane_n['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_one_lane_n['Stock'] = s_one_lane_n['Stock'] + s_one_lane_new.cumsum().reset_index(drop=True) /6
s_one_lane_st = m_one_lane_st.loc[m_one_lane_st['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_one_lane_st['Stock'] = s_one_lane_st['Stock'] + s_one_lane_new.cumsum().reset_index(drop=True) /6
s_one_lane_s = m_one_lane_s.loc[m_one_lane_s['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_one_lane_s['Stock'] = s_one_lane_s['Stock'] + s_one_lane_new.cumsum().reset_index(drop=True) /6
s_one_lane_e = m_one_lane_e.loc[m_one_lane_e['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_one_lane_e['Stock'] = s_one_lane_e['Stock'] + s_one_lane_new.cumsum().reset_index(drop=True) /6
s_one_lane_w = m_one_lane_w.loc[m_one_lane_w['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_one_lane_w['Stock'] = s_one_lane_w['Stock'] + s_one_lane_new.cumsum().reset_index(drop=True) /6

s_one_lane_s_sc, s_one_lane_s_oc, s_one_lane_s_i = mfa(s_one_lane_m)
s_one_lane_n_sc, s_one_lane_n_oc, s_one_lane_n_i = mfa(s_one_lane_n)
s_one_lane_st_sc, s_one_lane_st_oc, s_one_lane_st_i = mfa(s_one_lane_st)
s_one_lane_s_sc, s_one_lane_s_oc, s_one_lane_s_i = mfa(s_one_lane_s)
s_one_lane_e_sc, s_one_lane_e_oc, s_one_lane_e_i = mfa(s_one_lane_e)
s_one_lane_w_sc, s_one_lane_w_oc, s_one_lane_w_i = mfa(s_one_lane_w)

# using pandas gymnastics to join all the frames together #
s_one_lane_road_sc = pd.concat(
    [s_one_lane_s_sc, s_one_lane_n_sc, s_one_lane_st_sc, s_one_lane_s_sc, s_one_lane_e_sc, s_one_lane_w_sc],
    axis=1).sort_index(ascending=True)
s_one_lane_road_sc = s_one_lane_road_sc.sum(axis=1)

s_one_lane_road_oc = pd.concat(
    [s_one_lane_s_oc, s_one_lane_n_oc, s_one_lane_st_oc, s_one_lane_s_oc, s_one_lane_e_oc, s_one_lane_w_oc],
    axis=1).sort_index(ascending=True)
s_one_lane_road_oc = s_one_lane_road_oc.sum(axis=1)

s_one_lane_road_i = pd.concat(
    [s_one_lane_s_i, s_one_lane_n_i, s_one_lane_st_i, s_one_lane_s_i, s_one_lane_e_i, s_one_lane_w_i],
    axis=1).sort_index(ascending=True)
s_one_lane_road_i = s_one_lane_road_i.sum(axis=1)

# using pandas gymnastics to join all the frames together #
m_one_lane_road_sc = pd.concat(
    [p_one_lane_road_sc, k_one_lane_road_sc, s_one_lane_road_sc],
    axis=1).sort_index(ascending=True)
m_one_lane_road_sc_s = m_one_lane_road_sc.sum(axis=1) # Sum up for mfa based on road category #

m_one_lane_road_oc = pd.concat(
    [p_one_lane_road_oc, k_one_lane_road_oc, s_one_lane_road_oc],
    axis=1).sort_index(ascending=True)
m_one_lane_road_oc_s = m_one_lane_road_oc.sum(axis=1)

m_one_lane_road_i = pd.concat(
    [p_one_lane_road_i, k_one_lane_road_i, s_one_lane_road_i],
    axis=1).sort_index(ascending=True)
m_one_lane_road_i_s = m_one_lane_road_i.sum(axis=1)

# MFA highways #
# Privately owned #
p_highway_st = m_highway_st.loc[m_highway_st['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_highway_st['Stock'] = p_highway_st['Stock'] + p_highway_new.cumsum().reset_index(drop=True) /3
p_highway_s = m_highway_s.loc[m_highway_s['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_highway_s['Stock'] = p_highway_s['Stock'] + p_highway_new.cumsum().reset_index(drop=True) /3
#p_highway_e = m_highway_e.loc[m_highway_e['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
#p_highway_e['Stock'] = p_highway_e['Stock'] + p_highway_new.cumsum().reset_index(drop=True) /3

p_highway_st_sc, p_highway_st_oc, p_highway_st_i = mfa(p_highway_st)
p_highway_s_sc, p_highway_s_oc, p_highway_s_i = mfa(p_highway_s)
#p_highway_e_sc, p_highway_e_oc, p_highway_e_i = mfa(p_highway_e)

# using pandas gymnastics to join all the frames together #
p_highway_sc = pd.concat(
    [p_highway_st_sc, p_highway_s_sc],
    axis=1).sort_index(ascending=True)
p_highway_sc = p_highway_sc.sum(axis=1)

p_highway_oc = pd.concat(
    [p_highway_st_oc, p_highway_s_oc],
    axis=1).sort_index(ascending=True)
p_highway_oc = p_highway_oc.sum(axis=1)

p_highway_i = pd.concat(
    [p_highway_st_i, p_highway_s_i],
    axis=1).sort_index(ascending=True)
p_highway_i = p_highway_i.sum(axis=1)

# Kommun owned #
k_highway_st = m_highway_st.loc[m_highway_st['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_highway_st['Stock'] = k_highway_st['Stock'] + k_highway_new.cumsum().reset_index(drop=True) /3
k_highway_s = m_highway_s.loc[m_highway_s['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_highway_s['Stock'] = k_highway_s['Stock'] + k_highway_new.cumsum().reset_index(drop=True) /3
k_highway_w = m_highway_w.loc[m_highway_w['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_highway_w['Stock'] = k_highway_w['Stock'] + k_highway_new.cumsum().reset_index(drop=True) /3

k_highway_st_sc, k_highway_st_oc, k_highway_st_i = mfa(k_highway_st)
k_highway_s_sc, k_highway_s_oc, k_highway_s_i = mfa(k_highway_s)
k_highway_w_sc, k_highway_w_oc, k_highway_w_i = mfa(k_highway_w)

# using pandas gymnastics to join all the frames together #
k_highway_sc = pd.concat(
    [k_highway_st_sc, k_highway_s_sc, k_highway_w_sc],
    axis=1).sort_index(ascending=True)
k_highway_sc = k_highway_sc.sum(axis=1)

k_highway_oc = pd.concat(
    [k_highway_st_oc, k_highway_s_oc, k_highway_w_oc],
    axis=1).sort_index(ascending=True)
k_highway_oc = k_highway_oc.sum(axis=1)

k_highway_i = pd.concat(
    [k_highway_st_i, k_highway_s_i, k_highway_w_i],
    axis=1).sort_index(ascending=True)
k_highway_i = k_highway_i.sum(axis=1)

# State owned #
s_highway_m = m_highway_m.loc[m_highway_m['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_highway_m['Stock'] = s_highway_m['Stock'] + s_highway_new.cumsum().reset_index(drop=True) /6
s_highway_n = m_highway_n.loc[m_highway_n['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_highway_n['Stock'] = s_highway_n['Stock'] + s_highway_new.cumsum().reset_index(drop=True) /6
s_highway_st = m_highway_st.loc[m_highway_st['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_highway_st['Stock'] = s_highway_st['Stock'] + s_highway_new.cumsum().reset_index(drop=True) /6
s_highway_s = m_highway_s.loc[m_highway_s['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_highway_s['Stock'] = s_highway_s['Stock'] + s_highway_new.cumsum().reset_index(drop=True) /6
s_highway_e = m_highway_e.loc[m_highway_e['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_highway_e['Stock'] = s_highway_e['Stock'] + s_highway_new.cumsum().reset_index(drop=True) /6
s_highway_w = m_highway_w.loc[m_highway_w['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_highway_w['Stock'] = s_highway_w['Stock'] + s_highway_new.cumsum().reset_index(drop=True) /6

s_highway_s_sc, s_highway_s_oc, s_highway_s_i = mfa(s_highway_m)
s_highway_n_sc, s_highway_n_oc, s_highway_n_i = mfa(s_highway_n)
s_highway_st_sc, s_highway_st_oc, s_highway_st_i = mfa(s_highway_st)
s_highway_s_sc, s_highway_s_oc, s_highway_s_i = mfa(s_highway_s)
s_highway_e_sc, s_highway_e_oc, s_highway_e_i = mfa(s_highway_e)
s_highway_w_sc, s_highway_w_oc, s_highway_w_i = mfa(s_highway_w)

# using pandas gymnastics to join all the frames together #
s_highway_sc = pd.concat(
    [s_highway_s_sc, s_highway_n_sc, s_highway_st_sc, s_highway_s_sc, s_highway_e_sc, s_highway_w_sc],
    axis=1).sort_index(ascending=True)
s_highway_sc = s_highway_sc.sum(axis=1)

s_highway_oc = pd.concat(
    [s_highway_s_oc, s_highway_n_oc, s_highway_st_oc, s_highway_s_oc, s_highway_e_oc, s_highway_w_oc],
    axis=1).sort_index(ascending=True)
s_highway_oc = s_highway_oc.sum(axis=1)

s_highway_i = pd.concat(
    [s_highway_s_i, s_highway_n_i, s_highway_st_i, s_highway_s_i, s_highway_e_i, s_highway_w_i],
    axis=1).sort_index(ascending=True)
s_highway_i = s_highway_i.sum(axis=1)

# using pandas gymnastics to join all the frames together #
m_highway_sc = pd.concat(
    [p_highway_sc, k_highway_sc, s_highway_sc],
    axis=1).sort_index(ascending=True)
m_highway_sc_s = m_highway_sc.sum(axis=1)

m_highway_oc = pd.concat(
    [p_highway_oc, k_highway_oc, s_highway_oc],
    axis=1).sort_index(ascending=True)
m_highway_oc_s = m_highway_oc.sum(axis=1)

m_highway_i = pd.concat(
    [p_highway_i, k_highway_i, s_highway_i],
    axis=1).sort_index(ascending=True)
m_highway_i_s = m_highway_i.sum(axis=1)

# MFA two lane wide #
# Privately owned #
p_two_m = m_two_m.loc[m_two_m['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_two_m['Stock'] = p_two_m['Stock'] + p_two_new.cumsum().reset_index(drop=True) /6
p_two_n = m_two_n.loc[m_two_n['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_two_n['Stock'] = p_two_n['Stock'] + p_two_new.cumsum().reset_index(drop=True) /6
p_two_st = m_two_st.loc[m_two_st['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_two_st['Stock'] = p_two_st['Stock'] + p_two_new.cumsum().reset_index(drop=True) /6
p_two_s = m_two_s.loc[m_two_s['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_two_s['Stock'] = p_two_s['Stock'] + p_two_new.cumsum().reset_index(drop=True) /6
p_two_e = m_two_e.loc[m_two_e['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_two_e['Stock'] = p_two_e['Stock'] + p_two_new.cumsum().reset_index(drop=True) /6
p_two_w = m_two_w.loc[m_two_w['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_two_w['Stock'] = p_two_w['Stock'] + p_two_new.cumsum().reset_index(drop=True) /6

p_two_p_sc, p_two_p_oc, p_two_p_i = mfa(p_two_m)
p_two_n_sc, p_two_n_oc, p_two_n_i = mfa(p_two_n)
p_two_st_sc, p_two_st_oc, p_two_st_i = mfa(p_two_st)
p_two_s_sc, p_two_s_oc, p_two_s_i = mfa(p_two_s)
p_two_e_sc, p_two_e_oc, p_two_e_i = mfa(p_two_e)
p_two_w_sc, p_two_w_oc, p_two_w_i = mfa(p_two_w)

# using pandas gymnastics to join all the frames together #
p_two_sc = pd.concat(
    [p_two_p_sc, p_two_n_sc, p_two_st_sc, p_two_s_sc, p_two_e_sc, p_two_w_sc],
    axis=1).sort_index(ascending=True)
p_two_sc = p_two_sc.sum(axis=1)

p_two_oc = pd.concat(
    [p_two_p_oc, p_two_n_oc, p_two_st_oc, p_two_s_oc, p_two_e_oc, p_two_w_oc],
    axis=1).sort_index(ascending=True)
p_two_oc = p_two_oc.sum(axis=1)

p_two_i = pd.concat(
    [p_two_p_i, p_two_n_i, p_two_st_i, p_two_s_i, p_two_e_i, p_two_w_i],
    axis=1).sort_index(ascending=True)
p_two_i = p_two_i.sum(axis=1)

# Kommun owned #
k_two_m = m_two_m.loc[m_two_m['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_two_m['Stock'] = k_two_m['Stock'] + k_two_new.cumsum().reset_index(drop=True) /6
k_two_n = m_two_n.loc[m_two_n['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_two_n['Stock'] = k_two_n['Stock'] + k_two_new.cumsum().reset_index(drop=True) /6
k_two_st = m_two_st.loc[m_two_st['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_two_st['Stock'] = k_two_st['Stock'] + k_two_new.cumsum().reset_index(drop=True) /6
k_two_s = m_two_s.loc[m_two_s['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_two_s['Stock'] = k_two_s['Stock'] + k_two_new.cumsum().reset_index(drop=True) /6
k_two_e = m_two_e.loc[m_two_e['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_two_e['Stock'] = k_two_e['Stock'] + k_two_new.cumsum().reset_index(drop=True) /6
k_two_w = m_two_w.loc[m_two_w['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_two_w['Stock'] = k_two_w['Stock'] + k_two_new.cumsum().reset_index(drop=True) /6


k_two_k_sc, k_two_k_oc, k_two_k_i = mfa(k_two_m)
k_two_n_sc, k_two_n_oc, k_two_n_i = mfa(k_two_n)
k_two_st_sc, k_two_st_oc, k_two_st_i = mfa(k_two_st)
k_two_s_sc, k_two_s_oc, k_two_s_i = mfa(k_two_s)
k_two_e_sc, k_two_e_oc, k_two_e_i = mfa(k_two_e)
k_two_w_sc, k_two_w_oc, k_two_w_i = mfa(k_two_w)

# using pandas gymnastics to join all the frames together #
k_two_sc = pd.concat(
    [k_two_k_sc, k_two_n_sc, k_two_st_sc, k_two_s_sc, k_two_e_sc, k_two_w_sc],
    axis=1).sort_index(ascending=True)
k_two_sc = k_two_sc.sum(axis=1)

k_two_oc = pd.concat(
    [k_two_k_oc, k_two_n_oc, k_two_st_oc, k_two_s_oc, k_two_e_oc, k_two_w_oc],
    axis=1).sort_index(ascending=True)
k_two_oc = k_two_oc.sum(axis=1)

k_two_i = pd.concat(
    [k_two_k_i, k_two_n_i, k_two_st_i, k_two_s_i, k_two_e_i, k_two_w_i],
    axis=1).sort_index(ascending=True)
k_two_i = k_two_i.sum(axis=1)

# State owned #
s_two_m = m_two_m.loc[m_two_m['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_two_m['Stock'] = s_two_m['Stock'] + s_two_new.cumsum().reset_index(drop=True) /6
s_two_n = m_two_n.loc[m_two_n['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_two_n['Stock'] = s_two_n['Stock'] + s_two_new.cumsum().reset_index(drop=True) /6
s_two_st = m_two_st.loc[m_two_st['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_two_st['Stock'] = s_two_st['Stock'] + s_two_new.cumsum().reset_index(drop=True) /6
s_two_s = m_two_s.loc[m_two_s['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_two_s['Stock'] = s_two_s['Stock'] + s_two_new.cumsum().reset_index(drop=True) /6
s_two_e = m_two_e.loc[m_two_e['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_two_e['Stock'] = s_two_e['Stock'] + s_two_new.cumsum().reset_index(drop=True) /6
s_two_w = m_two_w.loc[m_two_w['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_two_w['Stock'] = s_two_w['Stock'] + s_two_new.cumsum().reset_index(drop=True) /6

s_two_s_sc, s_two_s_oc, s_two_s_i = mfa(s_two_m)
s_two_n_sc, s_two_n_oc, s_two_n_i = mfa(s_two_n)
s_two_st_sc, s_two_st_oc, s_two_st_i = mfa(s_two_st)
s_two_s_sc, s_two_s_oc, s_two_s_i = mfa(s_two_s)
s_two_e_sc, s_two_e_oc, s_two_e_i = mfa(s_two_e)
s_two_w_sc, s_two_w_oc, s_two_w_i = mfa(s_two_w)

# using pandas gymnastics to join all the frames together #
s_two_sc = pd.concat(
    [s_two_s_sc, s_two_n_sc, s_two_st_sc, s_two_s_sc, s_two_e_sc, s_two_w_sc],
    axis=1).sort_index(ascending=True)
s_two_sc = s_two_sc.sum(axis=1)

s_two_oc = pd.concat(
    [s_two_s_oc, s_two_n_oc, s_two_st_oc, s_two_s_oc, s_two_e_oc, s_two_w_oc],
    axis=1).sort_index(ascending=True)
s_two_oc = s_two_oc.sum(axis=1)

s_two_i = pd.concat(
    [s_two_s_i, s_two_n_i, s_two_st_i, s_two_s_i, s_two_e_i, s_two_w_i],
    axis=1).sort_index(ascending=True)
s_two_i = s_two_i.sum(axis=1)

# using pandas gymnastics to join all the frames together #
m_two_sc = pd.concat(
    [p_two_sc, k_two_sc, s_two_sc],
    axis=1).sort_index(ascending=True)
m_two_sc_s = m_two_sc.sum(axis=1)

m_two_oc = pd.concat(
    [p_two_oc, k_two_oc, s_two_oc],
    axis=1).sort_index(ascending=True)
m_two_oc_s = m_two_oc.sum(axis=1)

m_two_i = pd.concat(
    [p_two_i, k_two_i, s_two_i],
    axis=1).sort_index(ascending=True)
m_two_i_s = m_two_i.sum(axis=1)

# MFA meetings free road #
# Kommun owned #
k_meet_st = m_meet_st.loc[m_meet_st['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_meet_st['Stock'] = k_meet_st['Stock'] + k_meet_new.cumsum().reset_index(drop=True) /2
k_meet_s = m_meet_s.loc[m_meet_s['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_meet_s['Stock'] = k_meet_s['Stock'] + k_meet_new.cumsum().reset_index(drop=True) /2

k_meet_st_sc, k_meet_st_oc, k_meet_st_i = mfa(k_meet_st)
k_meet_s_sc, k_meet_s_oc, k_meet_s_i = mfa(k_meet_s)


# using pandas gymnastics to join all the frames together #
k_meet_sc = pd.concat(
    [k_meet_st_sc, k_meet_s_sc],
    axis=1).sort_index(ascending=True)
k_meet_sc = k_meet_sc.sum(axis=1)

k_meet_oc = pd.concat(
    [k_meet_st_oc, k_meet_s_oc],
    axis=1).sort_index(ascending=True)
k_meet_oc = k_meet_oc.sum(axis=1)

k_meet_i = pd.concat(
    [k_meet_st_i, k_meet_s_i],
    axis=1).sort_index(ascending=True)
k_meet_i = k_meet_i.sum(axis=1)

# State owned #
s_meet_m = m_meet_m.loc[m_meet_m['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_meet_m['Stock'] = s_meet_m['Stock'] + s_meet_new.cumsum().reset_index(drop=True) /6
s_meet_n = m_meet_n.loc[m_meet_n['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_meet_n['Stock'] = s_meet_n['Stock'] + s_meet_new.cumsum().reset_index(drop=True) /6
s_meet_st = m_meet_st.loc[m_meet_st['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_meet_st['Stock'] = s_meet_st['Stock'] + s_meet_new.cumsum().reset_index(drop=True) /6
s_meet_s = m_meet_s.loc[m_meet_s['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_meet_s['Stock'] = s_meet_s['Stock'] + s_meet_new.cumsum().reset_index(drop=True) /6
s_meet_e = m_meet_e.loc[m_meet_e['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_meet_e['Stock'] = s_meet_e['Stock'] + s_meet_new.cumsum().reset_index(drop=True) /6
s_meet_w = m_meet_w.loc[m_meet_w['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_meet_w['Stock'] = s_meet_w['Stock'] + s_meet_new.cumsum().reset_index(drop=True) /6

s_meet_s_sc, s_meet_s_oc, s_meet_s_i = mfa(s_meet_m)
s_meet_n_sc, s_meet_n_oc, s_meet_n_i = mfa(s_meet_n)
s_meet_st_sc, s_meet_st_oc, s_meet_st_i = mfa(s_meet_st)
s_meet_s_sc, s_meet_s_oc, s_meet_s_i = mfa(s_meet_s)
s_meet_e_sc, s_meet_e_oc, s_meet_e_i = mfa(s_meet_e)
s_meet_w_sc, s_meet_w_oc, s_meet_w_i = mfa(s_one_lane_w)

# using pandas gymnastics to join all the frames together #
s_meet_sc = pd.concat(
    [s_meet_s_sc, s_meet_n_sc, s_meet_st_sc, s_meet_s_sc, s_meet_e_sc, s_meet_w_sc],
    axis=1).sort_index(ascending=True)
s_meet_sc = s_meet_sc.sum(axis=1)

s_meet_oc = pd.concat(
    [s_meet_s_oc, s_meet_n_oc, s_meet_st_oc, s_meet_s_oc, s_meet_e_oc, s_meet_w_oc],
    axis=1).sort_index(ascending=True)
s_meet_oc = s_meet_oc.sum(axis=1)

s_meet_i = pd.concat(
    [s_meet_s_i, s_meet_n_i, s_meet_st_i, s_meet_s_i, s_meet_e_i, s_meet_w_i],
    axis=1).sort_index(ascending=True)
s_meet_i = s_meet_i.sum(axis=1)

# using pandas gymnastics to join all the frames together #
m_meet_sc = pd.concat(
    [k_meet_sc, s_meet_sc],
    axis=1).sort_index(ascending=True)
m_meet_sc_s = m_meet_sc.sum(axis=1)

m_meet_oc = pd.concat(
    [k_meet_oc, s_meet_oc],
    axis=1).sort_index(ascending=True)
m_meet_oc_s = m_meet_oc.sum(axis=1)

m_meet_i = pd.concat(
    [k_meet_i, s_meet_i],
    axis=1).sort_index(ascending=True)
m_meet_i_s = m_meet_i.sum(axis=1)

# MFA gravel road #
# Privately owned #
p_gravel_m = m_gravel_m.loc[m_gravel_m['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_gravel_m['Stock'] = p_gravel_m['Stock'] + p_gravel_new.cumsum().reset_index(drop=True) /6
p_gravel_n = m_gravel_n.loc[m_gravel_n['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_gravel_n['Stock'] = p_gravel_n['Stock'] + p_gravel_new.cumsum().reset_index(drop=True) /6
p_gravel_st = m_gravel_st.loc[m_gravel_st['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_gravel_st['Stock'] = p_gravel_st['Stock'] + p_gravel_new.cumsum().reset_index(drop=True) /6
p_gravel_s = m_gravel_s.loc[m_gravel_s['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_gravel_s['Stock'] = p_gravel_s['Stock'] + p_gravel_new.cumsum().reset_index(drop=True) /6
p_gravel_e = m_gravel_e.loc[m_gravel_e['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_gravel_e['Stock'] = p_gravel_e['Stock'] + p_gravel_new.cumsum().reset_index(drop=True) /6
p_gravel_w = m_gravel_w.loc[m_gravel_w['Vaghallartyp'] == 'enskild'].reset_index(drop=True)
p_gravel_w['Stock'] = p_gravel_w['Stock'] + p_gravel_new.cumsum().reset_index(drop=True) /6

p_gravel_p_sc, p_gravel_p_oc, p_gravel_p_i = mfa(p_gravel_m)
p_gravel_n_sc, p_gravel_n_oc, p_gravel_n_i = mfa(p_gravel_n)
p_gravel_st_sc, p_gravel_st_oc, p_gravel_st_i = mfa(p_gravel_st)
p_gravel_s_sc, p_gravel_s_oc, p_gravel_s_i = mfa(p_gravel_s)
p_gravel_e_sc, p_gravel_e_oc, p_gravel_e_i = mfa(p_gravel_e)
p_gravel_w_sc, p_gravel_w_oc, p_gravel_w_i = mfa(p_gravel_w)

# using pandas gymnastics to join all the frames together #
p_gravel_sc = pd.concat(
    [p_gravel_p_sc, p_gravel_n_sc, p_gravel_st_sc, p_gravel_s_sc, p_gravel_e_sc, p_gravel_w_sc],
    axis=1).sort_index(ascending=True)
p_gravel_sc = p_gravel_sc.sum(axis=1)

p_gravel_oc = pd.concat(
    [p_gravel_p_oc, p_gravel_n_oc, p_gravel_st_oc, p_gravel_s_oc, p_gravel_e_oc, p_gravel_w_oc],
    axis=1).sort_index(ascending=True)
p_gravel_oc = p_gravel_oc.sum(axis=1)

p_gravel_i = pd.concat(
    [p_gravel_p_i, p_gravel_n_i, p_gravel_st_i, p_gravel_s_i, p_gravel_e_i, p_gravel_w_i],
    axis=1).sort_index(ascending=True)
p_gravel_i = p_gravel_i.sum(axis=1)

# Kommun owned #
k_gravel_m = m_gravel_m.loc[m_gravel_m['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_gravel_m['Stock'] = k_gravel_m['Stock'] + k_gravel_new.cumsum().reset_index(drop=True) /6
k_gravel_n = m_gravel_n.loc[m_gravel_n['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_gravel_n['Stock'] = k_gravel_n['Stock'] + k_gravel_new.cumsum().reset_index(drop=True) /6
k_gravel_st = m_gravel_st.loc[m_gravel_st['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_gravel_st['Stock'] = k_gravel_st['Stock'] + k_gravel_new.cumsum().reset_index(drop=True) /6
k_gravel_s = m_gravel_s.loc[m_gravel_s['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_gravel_s['Stock'] = k_gravel_s['Stock'] + k_gravel_new.cumsum().reset_index(drop=True) /6
k_gravel_e = m_gravel_e.loc[m_gravel_e['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_gravel_e['Stock'] = k_gravel_e['Stock'] + k_gravel_new.cumsum().reset_index(drop=True) /6
k_gravel_w = m_gravel_w.loc[m_gravel_w['Vaghallartyp'] == 'kommunal'].reset_index(drop=True)
k_gravel_w['Stock'] = k_gravel_w['Stock'] + k_gravel_new.cumsum().reset_index(drop=True) /6

k_gravel_k_sc, k_gravel_k_oc, k_gravel_k_i = mfa(k_gravel_m)
k_gravel_n_sc, k_gravel_n_oc, k_gravel_n_i = mfa(k_gravel_n)
k_gravel_st_sc, k_gravel_st_oc, k_gravel_st_i = mfa(k_gravel_st)
k_gravel_s_sc, k_gravel_s_oc, k_gravel_s_i = mfa(k_gravel_s)
k_gravel_e_sc, k_gravel_e_oc, k_gravel_e_i = mfa(k_gravel_e)
k_gravel_w_sc, k_gravel_w_oc, k_gravel_w_i = mfa(k_gravel_w)

# using pandas gymnastics to join all the frames together #
k_gravel_sc = pd.concat(
    [k_gravel_k_sc, k_gravel_n_sc, k_gravel_st_sc, k_gravel_s_sc, k_gravel_e_sc, k_gravel_w_sc],
    axis=1).sort_index(ascending=True)
k_gravel_sc = k_gravel_sc.sum(axis=1)

k_gravel_oc = pd.concat(
    [k_gravel_k_oc, k_gravel_n_oc, k_gravel_st_oc, k_gravel_s_oc, k_gravel_e_oc, k_gravel_w_oc],
    axis=1).sort_index(ascending=True)
k_gravel_oc = k_gravel_oc.sum(axis=1)

k_gravel_i = pd.concat(
    [k_gravel_k_i, k_gravel_n_i, k_gravel_st_i, k_gravel_s_i, k_gravel_e_i, k_gravel_w_i],
    axis=1).sort_index(ascending=True)
k_gravel_i = k_gravel_i.sum(axis=1)

# State owned #
s_gravel_m = m_gravel_m.loc[m_gravel_m['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_gravel_m['Stock'] = s_gravel_m['Stock'] + s_gravel_new.cumsum().reset_index(drop=True) /6
s_gravel_n = m_gravel_n.loc[m_gravel_n['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_gravel_n['Stock'] = s_gravel_n['Stock'] + s_gravel_new.cumsum().reset_index(drop=True) /6
s_gravel_st = m_gravel_st.loc[m_gravel_st['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_gravel_st['Stock'] = s_gravel_st['Stock'] + s_gravel_new.cumsum().reset_index(drop=True) /6
s_gravel_s = m_gravel_s.loc[m_gravel_s['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_gravel_s['Stock'] = s_gravel_s['Stock'] + s_gravel_new.cumsum().reset_index(drop=True) /6
s_gravel_e = m_gravel_e.loc[m_gravel_e['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_gravel_e['Stock'] = s_gravel_e['Stock'] + s_gravel_new.cumsum().reset_index(drop=True) /6
s_gravel_w = m_gravel_w.loc[m_gravel_w['Vaghallartyp'] == 'statlig'].reset_index(drop=True)
s_gravel_w['Stock'] = s_gravel_w['Stock'] + s_gravel_new.cumsum().reset_index(drop=True) /6

s_gravel_s_sc, s_gravel_s_oc, s_gravel_s_i = mfa(s_gravel_m)
s_gravel_n_sc, s_gravel_n_oc, s_gravel_n_i = mfa(s_gravel_n)
s_gravel_st_sc, s_gravel_st_oc, s_gravel_st_i = mfa(s_gravel_st)
s_gravel_s_sc, s_gravel_s_oc, s_gravel_s_i = mfa(s_gravel_s)
s_gravel_e_sc, s_gravel_e_oc, s_gravel_e_i = mfa(s_gravel_e)
s_gravel_w_sc, s_gravel_w_oc, s_gravel_w_i = mfa(s_one_lane_w)

# using pandas gymnastics to join all the frames together #
s_gravel_sc = pd.concat(
    [s_gravel_s_sc, s_gravel_n_sc, s_gravel_st_sc, s_gravel_s_sc, s_gravel_e_sc, s_gravel_w_sc],
    axis=1).sort_index(ascending=True)
s_gravel_sc = s_gravel_sc.sum(axis=1)

s_gravel_oc = pd.concat(
    [s_gravel_s_oc, s_gravel_n_oc, s_gravel_st_oc, s_gravel_s_oc, s_gravel_e_oc, s_gravel_w_oc],
    axis=1).sort_index(ascending=True)
s_gravel_oc = s_gravel_oc.sum(axis=1)

s_gravel_i = pd.concat(
    [s_gravel_s_i, s_gravel_n_i, s_gravel_st_i, s_gravel_s_i, s_gravel_e_i, s_gravel_w_i],
    axis=1).sort_index(ascending=True)
s_gravel_i = s_gravel_i.sum(axis=1)

# using pandas gymnastics to join all the frames together #
m_gravel_sc = pd.concat(
    [p_gravel_sc, k_gravel_sc, s_gravel_sc],
    axis=1).sort_index(ascending=True)
m_gravel_sc_s = m_gravel_sc.sum(axis=1)

m_gravel_oc = pd.concat(
    [p_gravel_oc, k_gravel_oc, s_gravel_oc],
    axis=1).sort_index(ascending=True)
m_gravel_oc_s = m_gravel_oc.sum(axis=1)

m_gravel_i = pd.concat(
    [p_gravel_i, k_gravel_i, s_gravel_i],
    axis=1).sort_index(ascending=True)
m_gravel_i_s = m_gravel_i.sum(axis=1)

# Total inflow, outflow, and stock for all Swedish roads #
m_road_i = m_one_lane_road_i_s + m_highway_i_s + m_two_i_s + m_meet_i_s + m_gravel_i_s
m_road_cat_i = pd.concat(
    [m_one_lane_road_i_s, m_highway_i_s, m_two_i_s, m_meet_i_s,
     m_gravel_i_s], axis=1)
m_road_sc = m_one_lane_road_sc_s + m_highway_sc_s + m_two_sc_s + m_meet_sc_s + m_gravel_sc_s
m_road_cat_sc = pd.concat(
    [m_one_lane_road_sc_s, m_highway_sc_s, m_two_sc_s, m_meet_sc_s,
     m_gravel_sc], axis=1)
m_road_oc = m_one_lane_road_oc_s + m_highway_oc_s + m_two_oc_s + m_meet_oc_s + m_gravel_oc_s
m_road_cat_oc = pd.concat(
    [m_one_lane_road_oc_s, m_highway_oc_s, m_two_oc_s, m_meet_oc_s,
     m_gravel_oc], axis=1)

# By road ownership #
# Asphalt new construction inflow #
p_asp_one_lane_new_i = p_one_lane_new.to_frame() @ One_lane_road_MI.iloc[:, 1].to_numpy() 
p_asp_highway_new_i = p_highway_new.to_frame() @ Highway_MI.iloc[:, 1].to_numpy()
p_asp_two_new_i = p_two_new.to_frame() @ Two_lane_road_MI.iloc[:, 1].to_numpy()
p_asp_total_new_i = p_asp_one_lane_new_i + p_asp_highway_new_i + p_asp_two_new_i
p_asp_total_new_cat_i = pd.concat([p_asp_one_lane_new_i, p_asp_highway_new_i, p_asp_two_new_i], axis=1)

p_asp_total_new_cat_i['3'] = 0
p_asp_total_new_cat_i.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road']

# Asphalt maintenance inflow #
# convert to mt and only 50mm of asphalt is removed during maintenance #
p_asp_one_lane_i = ((m_one_lane_road_i.iloc[:,0] - p_one_lane_new).to_frame()) @ One_lane_road_MI.iloc[:,
                                                                        1].to_numpy() * (50 / 180)
p_asp_highway_i = ((m_highway_i.iloc[:,0] - p_highway_new).to_frame()) @ Highway_MI.iloc[:,
                                                                     1].to_numpy() * (50 / 180)
p_asp_two_i = ((m_two_i.iloc[:,0] - p_two_new).to_frame()) @ Two_lane_road_MI.iloc[:,
                                                                        1].to_numpy() * (50 / 180)
p_asp_total_i = p_asp_one_lane_i + p_asp_highway_i + p_asp_two_i
p_asp_total_cat_i = pd.concat([p_asp_one_lane_i, p_asp_highway_i, p_asp_two_i], axis=1)
p_asp_total_cat_i['3'] = 0
p_asp_total_cat_i.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road']

# Asphalt road inflow#
p_asp_real_i = p_asp_total_i + p_asp_total_new_i
p_asp_real_cat_i = p_asp_total_cat_i + p_asp_total_new_cat_i

# Asphalt outflow, only for maintenance #
p_asp_one_lane_oc = ((m_one_lane_road_oc.iloc[:,0] - p_one_lane_new).to_frame()) @ One_lane_road_MI.iloc[:,
                                                                          1].to_numpy() * (50 / 180)
p_asp_highway_oc = ((m_highway_oc.iloc[:,0] - p_highway_new).to_frame()) @ Highway_MI.iloc[:,
                                                                       1].to_numpy() * (50 / 180)
p_asp_two_oc = ((m_two_oc.iloc[:,0] - p_two_new).to_frame()) @ Two_lane_road_MI.iloc[:,
                                                                          1].to_numpy() * (50 / 180)
p_asp_total_oc = p_asp_one_lane_oc + p_asp_highway_oc + p_asp_two_oc
p_asp_total_cat_oc = pd.concat([p_asp_one_lane_oc, p_asp_highway_oc, p_asp_two_oc], axis=1)

# Asphalt road stock #
p_asp_one_lane_sc = m_one_lane_road_sc.iloc[:,0].to_frame() @ One_lane_road_MI.iloc[:, 1].to_numpy()
p_asp_highway_sc = m_highway_sc.iloc[:,0].to_frame() @ Highway_MI.iloc[:, 1].to_numpy()
p_asp_two_sc = m_two_sc.iloc[:,0].to_frame() @ Two_lane_road_MI.iloc[:, 1].to_numpy()
p_asp_total_sc = p_asp_one_lane_sc + p_asp_highway_sc + p_asp_two_sc
p_asp_total_cat_sc = pd.concat([p_asp_one_lane_sc, p_asp_highway_sc, p_asp_two_sc], axis=1)

# Asphalt new construction inflow #
k_asp_one_lane_new_i = k_one_lane_new.to_frame() @ One_lane_road_MI.iloc[:, 1].to_numpy() 
k_asp_highway_new_i = k_highway_new.to_frame() @ Highway_MI.iloc[:, 1].to_numpy()
k_asp_two_new_i = k_two_new.to_frame() @ Two_lane_road_MI.iloc[:, 1].to_numpy()
k_asp_meet_new_i = k_meet_new.to_frame() @ Meeting_free_road_MI.iloc[:, 1].to_numpy()
k_asp_total_new_i = k_asp_one_lane_new_i + k_asp_highway_new_i + k_asp_two_new_i + k_asp_meet_new_i
k_asp_total_new_cat_i = pd.concat([k_asp_one_lane_new_i, k_asp_highway_new_i, k_asp_two_new_i, k_asp_meet_new_i], axis=1)
k_asp_total_new_cat_i.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road']

# Asphalt maintenance inflow #
# convert to mt and only 50mm of asphalt is removed during maintenance #
k_asp_one_lane_i = ((m_one_lane_road_i.iloc[:,1] - k_one_lane_new).to_frame()) @ One_lane_road_MI.iloc[:,
                                                                        1].to_numpy() * (50 / 180)
k_asp_highway_i = ((m_highway_i.iloc[:,1] - k_highway_new).to_frame()) @ Highway_MI.iloc[:,
                                                                     1].to_numpy() * (50 / 180)
k_asp_two_i = ((m_two_i.iloc[:,1] - k_two_new).to_frame()) @ Two_lane_road_MI.iloc[:,
                                                                        1].to_numpy() * (50 / 180)
k_asp_meet_i = ((m_meet_i.iloc[:,0] - k_meet_new).to_frame()) @ Meeting_free_road_MI.iloc[:,
                                                            1].to_numpy() * (50 / 180)
k_asp_total_i = k_asp_one_lane_i + k_asp_highway_i + k_asp_two_i + k_asp_meet_i
k_asp_total_cat_i = pd.concat([k_asp_one_lane_i, k_asp_highway_i, k_asp_two_i, k_asp_meet_i], axis=1)
k_asp_total_cat_i.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road']

# Asphalt road inflow#
k_asp_real_i = k_asp_total_i + k_asp_total_new_i
k_asp_real_cat_i = k_asp_total_cat_i + k_asp_total_new_cat_i

# Asphalt outflow, only for maintenance #
k_asp_one_lane_oc = ((m_one_lane_road_oc.iloc[:,1] - k_one_lane_new).to_frame()) @ One_lane_road_MI.iloc[:, 1].to_numpy() * (50 / 180)
k_asp_highway_oc = ((m_highway_oc.iloc[:,1] - k_highway_new).to_frame()) @ Highway_MI.iloc[:, 1].to_numpy() * (50 / 180)
k_asp_two_oc = ((m_two_oc.iloc[:,1] - k_two_new).to_frame()) @ Two_lane_road_MI.iloc[:, 1].to_numpy() * (50 / 180)
k_asp_meet_oc = ((m_meet_oc.iloc[:,0] - k_meet_new).to_frame()) @ Meeting_free_road_MI.iloc[:,1].to_numpy() * (50 / 180)
k_asp_total_oc = k_asp_one_lane_oc + k_asp_highway_oc + k_asp_two_oc + k_asp_meet_oc
k_asp_total_cat_oc = pd.concat([k_asp_one_lane_oc, k_asp_highway_oc, k_asp_two_oc, k_asp_meet_oc], axis=1)

# Asphalt road stock #
k_asp_one_lane_sc = m_one_lane_road_sc.iloc[:,1].to_frame() @ One_lane_road_MI.iloc[:, 1].to_numpy()
k_asp_highway_sc = m_highway_sc.iloc[:,1].to_frame() @ Highway_MI.iloc[:, 1].to_numpy()
k_asp_two_sc = m_two_sc.iloc[:,1].to_frame() @ Two_lane_road_MI.iloc[:, 1].to_numpy()
k_asp_meet_sc = m_meet_sc.iloc[:,0].to_frame() @ Meeting_free_road_MI.iloc[:, 1].to_numpy()
k_asp_total_sc = k_asp_one_lane_sc + k_asp_highway_sc + k_asp_two_sc + k_asp_meet_sc
k_asp_total_cat_sc = pd.concat([k_asp_one_lane_sc, k_asp_highway_sc, k_asp_two_sc, k_asp_meet_sc], axis=1)

# Asphalt new construction inflow #
s_asp_one_lane_new_i = s_one_lane_new.to_frame() @ One_lane_road_MI.iloc[:, 1].to_numpy() 
s_asp_highway_new_i = s_highway_new.to_frame() @ Highway_MI.iloc[:, 1].to_numpy()
s_asp_two_new_i = s_two_new.to_frame() @ Two_lane_road_MI.iloc[:, 1].to_numpy()
s_asp_meet_new_i = s_meet_new.to_frame() @ Meeting_free_road_MI.iloc[:, 1].to_numpy()
s_asp_total_new_i = s_asp_one_lane_new_i + s_asp_highway_new_i + s_asp_two_new_i + s_asp_meet_new_i
s_asp_total_new_cat_i = pd.concat([s_asp_one_lane_new_i, s_asp_highway_new_i, s_asp_two_new_i, s_asp_meet_new_i], axis=1)
s_asp_total_new_cat_i.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road']

# Asphalt maintenance inflow #
# convert to mt and only 50mm of asphalt is removed during maintenance #
s_asp_one_lane_i = ((m_one_lane_road_i.iloc[:,2] - s_one_lane_new).to_frame()) @ One_lane_road_MI.iloc[:,
                                                                        1].to_numpy() * (50 / 180)
s_asp_highway_i = ((m_highway_i.iloc[:,2] - s_highway_new).to_frame()) @ Highway_MI.iloc[:,
                                                                     1].to_numpy() * (50 / 180)
s_asp_two_i = ((m_two_i.iloc[:,2] - s_two_new).to_frame()) @ Two_lane_road_MI.iloc[:,
                                                                        1].to_numpy() * (50 / 180)
s_asp_meet_i = ((m_meet_i.iloc[:,1] - s_meet_new).to_frame()) @ Meeting_free_road_MI.iloc[:,
                                                            1].to_numpy() * (50 / 180)
s_asp_total_i = s_asp_one_lane_i + s_asp_highway_i + s_asp_two_i + s_asp_meet_i
s_asp_total_cat_i = pd.concat([s_asp_one_lane_i, s_asp_highway_i, s_asp_two_i, s_asp_meet_i], axis=1)
s_asp_total_cat_i.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road']

# Asphalt road inflow#
s_asp_real_i = s_asp_total_i + s_asp_total_new_i
s_asp_real_cat_i = s_asp_total_cat_i + s_asp_total_new_cat_i

# Asphalt outflow, only for maintenance #
s_asp_one_lane_oc = ((m_one_lane_road_oc.iloc[:,2] - s_one_lane_new).to_frame()) @ One_lane_road_MI.iloc[:,
                                                                          1].to_numpy() * (50 / 180)
s_asp_highway_oc = ((m_highway_oc.iloc[:,2] - s_highway_new).to_frame()) @ Highway_MI.iloc[:,
                                                                       1].to_numpy() * (50 / 180)
s_asp_two_oc = ((m_two_oc.iloc[:,2] - s_two_new).to_frame()) @ Two_lane_road_MI.iloc[:,
                                                                          1].to_numpy() * (50 / 180)
s_asp_meet_oc = ((m_meet_oc.iloc[:,1] - s_meet_new).to_frame()) @ Meeting_free_road_MI.iloc[:,
                                                              1].to_numpy() * (50 / 180)
s_asp_total_oc = s_asp_one_lane_oc + s_asp_highway_oc + s_asp_two_oc + s_asp_meet_oc
s_asp_total_cat_oc = pd.concat([s_asp_one_lane_oc, s_asp_highway_oc, s_asp_two_oc, s_asp_meet_oc], axis=1)

# Asphalt road stock #
s_asp_one_lane_sc = m_one_lane_road_sc.iloc[:,2].to_frame() @ One_lane_road_MI.iloc[:, 1].to_numpy()
s_asp_highway_sc = m_highway_sc.iloc[:,2].to_frame() @ Highway_MI.iloc[:, 1].to_numpy()
s_asp_two_sc = m_two_sc.iloc[:,2].to_frame() @ Two_lane_road_MI.iloc[:, 1].to_numpy()
s_asp_meet_sc = m_meet_sc.iloc[:,1].to_frame() @ Meeting_free_road_MI.iloc[:, 1].to_numpy()
s_asp_total_sc = s_asp_one_lane_sc + s_asp_highway_sc + s_asp_two_sc + s_asp_meet_sc
s_asp_total_cat_sc = pd.concat([s_asp_one_lane_sc, s_asp_highway_sc, s_asp_two_sc, s_asp_meet_sc], axis=1)

# Summing up asphalt #
asp_total_i = p_asp_total_i + k_asp_total_i + s_asp_total_i
asp_total_cat_i = pd.concat([p_asp_total_i, k_asp_total_i, s_asp_total_i], axis=1)

asp_total_new_i = p_asp_total_new_i + k_asp_total_new_i + s_asp_total_new_i
asp_total_new_cat_i = pd.concat([p_asp_total_new_i, k_asp_total_new_i, s_asp_total_new_i], axis=1)
asp_real_i = asp_total_i + asp_total_new_i
asp_real_cat_i = asp_total_cat_i + asp_total_new_cat_i

asp_total_oc = p_asp_total_oc + k_asp_total_oc + s_asp_total_oc
asp_total_cat_oc = pd.concat([p_asp_total_oc, k_asp_total_oc, s_asp_total_oc], axis=1)

asp_total_sc = p_asp_total_sc + k_asp_total_sc + s_asp_total_sc
asp_total_cat_sc = pd.concat([p_asp_total_sc, k_asp_total_sc, s_asp_total_sc], axis=1)

# Gravel road inflow #
p_grv_one_lane_i = m_one_lane_road_i.iloc[:, 0].to_frame() @ One_lane_road_MI.iloc[:, 0].to_numpy()
p_grv_highway_i = m_highway_i.iloc[:, 0].to_frame() @ Highway_MI.iloc[:, 0].to_numpy()
p_grv_two_i = m_two_i.iloc[:, 0].to_frame() @ Two_lane_road_MI.iloc[:, 0].to_numpy()
p_grv_gravel_i = p_gravel_new.to_frame() @ Gravel_road_MI.iloc[:, 0].to_numpy()
p_grv_total_i = p_grv_one_lane_i + p_grv_highway_i + p_grv_two_i + p_grv_gravel_i
p_grv_total_cat_i = pd.concat([p_grv_one_lane_i, p_grv_highway_i, p_grv_two_i], axis=1)

# Gravel road outflow #
p_grv_one_lane_oc = m_one_lane_road_oc.iloc[:, 0].to_frame() @ One_lane_road_MI.iloc[:, 0].to_numpy()
p_grv_highway_oc = m_highway_oc.iloc[:, 0].to_frame() @ Highway_MI.iloc[:, 0].to_numpy()
p_grv_two_oc = m_two_oc.iloc[:, 0].to_frame() @ Two_lane_road_MI.iloc[:, 0].to_numpy()
p_grv_total_oc = p_grv_one_lane_oc + p_grv_highway_oc + p_grv_two_oc
p_grv_total_cat_oc = pd.concat([p_grv_one_lane_oc, p_grv_highway_oc, p_grv_two_oc], axis=1)

# Gravel road stock #
p_grv_one_lane_sc = m_one_lane_road_sc.iloc[:, 0].to_frame() @ One_lane_road_MI.iloc[:, 0].to_numpy()
p_grv_highway_sc = m_highway_sc.iloc[:, 0].to_frame() @ Highway_MI.iloc[:, 0].to_numpy()
p_grv_two_sc = m_two_sc.iloc[:, 0].to_frame() @ Two_lane_road_MI.iloc[:, 0].to_numpy()
p_grv_gravel_sc = m_gravel_sc.iloc[:, 0].to_frame() @ Gravel_road_MI.iloc[:, 0].to_numpy()
p_grv_total_sc = p_grv_one_lane_sc + p_grv_highway_sc + p_grv_two_sc + p_grv_gravel_sc
p_grv_total_cat_sc = pd.concat([p_grv_one_lane_sc, p_grv_highway_sc, p_grv_two_sc, p_grv_gravel_sc], axis=1)

# Gravel new construction #
# This is inflow of gravel if we assume that no gravel is replaced during maintenance #
p_grv_one_lane_new_i = p_one_lane_new.to_frame() @ One_lane_road_MI.iloc[:, 0].to_numpy()
p_grv_highway_new_i = p_highway_new.to_frame() @ Highway_MI.iloc[:, 0].to_numpy()
p_grv_two_new_i = p_two_new.to_frame() @ Two_lane_road_MI.iloc[:, 0].to_numpy()
p_grv_total_new_i = p_grv_one_lane_new_i + p_grv_highway_new_i + p_grv_two_new_i
p_grv_total_new_cat_i = pd.concat([p_grv_one_lane_new_i, p_grv_highway_new_i, p_grv_two_new_i], axis=1)

# Gravel road inflow #
k_grv_one_lane_i = m_one_lane_road_i.iloc[:, 1].to_frame() @ One_lane_road_MI.iloc[:, 0].to_numpy()
k_grv_highway_i = m_highway_i.iloc[:, 1].to_frame() @ Highway_MI.iloc[:, 0].to_numpy()
k_grv_two_i = m_two_i.iloc[:, 1].to_frame() @ Two_lane_road_MI.iloc[:, 0].to_numpy()
k_grv_meet_i = m_meet_i.iloc[:, 0].to_frame() @ Meeting_free_road_MI.iloc[:, 0].to_numpy()
k_grv_gravel_i = p_gravel_new.to_frame() @ Gravel_road_MI.iloc[:, 0].to_numpy()
k_grv_total_i = k_grv_one_lane_i + k_grv_highway_i + k_grv_two_i + k_grv_meet_i + k_grv_gravel_i
k_grv_total_cat_i = pd.concat([k_grv_one_lane_i, k_grv_highway_i, k_grv_two_i, k_grv_meet_i], axis=1)

# Gravel road outflow #
k_grv_one_lane_oc = m_one_lane_road_oc.iloc[:, 1].to_frame() @ One_lane_road_MI.iloc[:, 0].to_numpy()
k_grv_highway_oc = m_highway_oc.iloc[:, 1].to_frame() @ Highway_MI.iloc[:, 0].to_numpy()
k_grv_two_oc = m_two_oc.iloc[:, 1].to_frame() @ Two_lane_road_MI.iloc[:, 0].to_numpy()
k_grv_meet_oc = m_meet_oc.iloc[:, 0].to_frame() @ Meeting_free_road_MI.iloc[:, 0].to_numpy()
k_grv_total_oc = k_grv_one_lane_oc + k_grv_highway_oc + k_grv_two_oc + k_grv_meet_oc
k_grv_total_cat_oc = pd.concat([k_grv_one_lane_oc, k_grv_highway_oc, k_grv_two_oc, k_grv_meet_oc], axis=1)

# Gravel road stock #
k_grv_one_lane_sc = m_one_lane_road_sc.iloc[:, 1].to_frame() @ One_lane_road_MI.iloc[:, 0].to_numpy()
k_grv_highway_sc = m_highway_sc.iloc[:, 1].to_frame() @ Highway_MI.iloc[:, 0].to_numpy()
k_grv_two_sc = m_two_sc.iloc[:, 1].to_frame() @ Two_lane_road_MI.iloc[:, 0].to_numpy()
k_grv_meet_sc = m_meet_sc.iloc[:, 0].to_frame() @ Meeting_free_road_MI.iloc[:, 0].to_numpy()
k_grv_gravel_sc = m_gravel_sc.iloc[:, 1].to_frame() @ Gravel_road_MI.iloc[:, 0].to_numpy()
k_grv_total_sc = k_grv_one_lane_sc + k_grv_highway_sc + k_grv_two_sc + k_grv_meet_sc + k_grv_gravel_sc
k_grv_total_cat_sc = pd.concat([k_grv_one_lane_sc, k_grv_highway_sc, k_grv_two_sc, k_grv_meet_sc, k_grv_gravel_sc], axis=1)

# Gravel new construction #
# This is inflow of gravel if we assume that no gravel is replaced during maintenance #
k_grv_one_lane_new_i = k_one_lane_new.to_frame() @ One_lane_road_MI.iloc[:, 0].to_numpy()
k_grv_highway_new_i = k_highway_new.to_frame() @ Highway_MI.iloc[:, 0].to_numpy()
k_grv_two_new_i = k_two_new.to_frame() @ Two_lane_road_MI.iloc[:, 0].to_numpy()
k_grv_meet_new_i = k_meet_new.to_frame() @ Meeting_free_road_MI.iloc[:, 0].to_numpy()
k_grv_total_new_i = k_grv_one_lane_new_i + k_grv_highway_new_i + k_grv_two_new_i + k_grv_meet_new_i
k_grv_total_new_cat_i = pd.concat([k_grv_one_lane_new_i, k_grv_highway_new_i, k_grv_two_new_i, k_grv_meet_new_i], axis=1)

# Gravel road inflow #
s_grv_one_lane_i = m_one_lane_road_i.iloc[:, 2].to_frame() @ One_lane_road_MI.iloc[:, 0].to_numpy()
s_grv_highway_i = m_highway_i.iloc[:, 2].to_frame() @ Highway_MI.iloc[:, 0].to_numpy()
s_grv_two_i = m_two_i.iloc[:, 2].to_frame() @ Two_lane_road_MI.iloc[:, 0].to_numpy()
s_grv_meet_i = m_meet_i.iloc[:, 1].to_frame() @ Meeting_free_road_MI.iloc[:, 0].to_numpy()
s_grv_gravel_i = s_gravel_new.to_frame() @ Gravel_road_MI.iloc[:, 0].to_numpy()
s_grv_total_i = s_grv_one_lane_i + s_grv_highway_i + s_grv_two_i + s_grv_meet_i + s_grv_gravel_i
s_grv_total_cat_i = pd.concat([s_grv_one_lane_i, s_grv_highway_i, s_grv_two_i, s_grv_meet_i], axis=1)

# Gravel road outflow #
s_grv_one_lane_oc = m_one_lane_road_oc.iloc[:, 2].to_frame() @ One_lane_road_MI.iloc[:, 0].to_numpy()
s_grv_highway_oc = m_highway_oc.iloc[:, 2].to_frame() @ Highway_MI.iloc[:, 0].to_numpy()
s_grv_two_oc = m_two_oc.iloc[:, 2].to_frame() @ Two_lane_road_MI.iloc[:, 0].to_numpy()
s_grv_meet_oc = m_meet_oc.iloc[:, 1].to_frame() @ Meeting_free_road_MI.iloc[:, 0].to_numpy()
s_grv_total_oc = s_grv_one_lane_oc + s_grv_highway_oc + s_grv_two_oc + s_grv_meet_oc
s_grv_total_cat_oc = pd.concat([s_grv_one_lane_oc, s_grv_highway_oc, s_grv_two_oc, s_grv_meet_oc], axis=1)

# Gravel road stock #
s_grv_one_lane_sc = m_one_lane_road_sc.iloc[:, 2].to_frame() @ One_lane_road_MI.iloc[:, 0].to_numpy()
s_grv_highway_sc = m_highway_sc.iloc[:, 2].to_frame() @ Highway_MI.iloc[:, 0].to_numpy()
s_grv_two_sc = m_two_sc.iloc[:, 2].to_frame() @ Two_lane_road_MI.iloc[:, 0].to_numpy()
s_grv_meet_sc = m_meet_sc.iloc[:, 1].to_frame() @ Meeting_free_road_MI.iloc[:, 0].to_numpy()
s_grv_gravel_sc = m_gravel_sc.iloc[:, 2].to_frame() @ Gravel_road_MI.iloc[:, 0].to_numpy()
s_grv_total_sc = s_grv_one_lane_sc + s_grv_highway_sc + s_grv_two_sc + s_grv_meet_sc + s_grv_gravel_sc
s_grv_total_cat_sc = pd.concat([s_grv_one_lane_sc, s_grv_highway_sc, s_grv_two_sc, s_grv_meet_sc, s_grv_gravel_sc], axis=1)

# Gravel new construction #
# This is inflow of gravel if we assume that no gravel is replaced during maintenance #
s_grv_one_lane_new_i = s_one_lane_new.to_frame() @ One_lane_road_MI.iloc[:, 0].to_numpy()
s_grv_highway_new_i = s_highway_new.to_frame() @ Highway_MI.iloc[:, 0].to_numpy()
s_grv_two_new_i = s_two_new.to_frame() @ Two_lane_road_MI.iloc[:, 0].to_numpy()
s_grv_meet_new_i = s_meet_new.to_frame() @ Meeting_free_road_MI.iloc[:, 0].to_numpy()
s_grv_total_new_i = s_grv_one_lane_new_i + s_grv_highway_new_i + s_grv_two_new_i + s_grv_meet_new_i
s_grv_total_new_cat_i = pd.concat([s_grv_one_lane_new_i, s_grv_highway_new_i, s_grv_two_new_i, s_grv_meet_new_i], axis=1)

# Summing up gravel #
grv_total_i = p_grv_total_i + k_grv_total_i + s_grv_total_i
grv_total_cat_i = pd.concat([p_grv_total_i, k_grv_total_i, s_grv_total_i], axis=1)

grv_total_new_i = p_grv_total_new_i + k_grv_total_new_i + s_grv_total_new_i
grv_total_new_cat_i = pd.concat([p_grv_total_new_i, k_grv_total_new_i, s_grv_total_new_i], axis=1)

grv_total_oc = p_grv_total_oc + k_grv_total_oc + s_grv_total_oc
grv_total_cat_oc = pd.concat([p_grv_total_oc, k_grv_total_oc, s_grv_total_oc], axis=1)
grv_total_sc = p_grv_total_sc + k_grv_total_sc + s_grv_total_sc
grv_total_cat_sc = pd.concat([p_grv_total_sc, k_grv_total_sc, s_grv_total_sc], axis=1)

# Steel road inflow in kt #
p_steel_one_lane_i = m_one_lane_road_i.iloc[:, 0].to_frame() @ One_lane_road_MI.iloc[:, 2].to_numpy()
p_steel_highway_i = m_highway_i.iloc[:, 0].to_frame() @ Highway_MI.iloc[:, 2].to_numpy()
p_steel_two_i = m_two_i.iloc[:, 0].to_frame() @ Two_lane_road_MI.iloc[:, 2].to_numpy()
p_steel_total_i = p_steel_one_lane_i + p_steel_highway_i + p_steel_two_i
p_steel_total_cat_i = pd.concat([p_steel_one_lane_i, p_steel_highway_i, p_steel_two_i], axis=1)

# Steel road outflow in kt #
p_steel_one_lane_oc = m_one_lane_road_oc.iloc[:, 0].to_frame() @ One_lane_road_MI.iloc[:, 2].to_numpy()
p_steel_highway_oc = m_highway_oc.iloc[:, 0].to_frame() @ Highway_MI.iloc[:, 2].to_numpy()
p_steel_two_oc = m_two_oc.iloc[:, 0].to_frame() @ Two_lane_road_MI.iloc[:, 2].to_numpy()
p_steel_total_oc = p_steel_one_lane_oc + p_steel_highway_oc + p_steel_two_oc
p_steel_total_cat_oc = pd.concat([p_steel_one_lane_oc, p_steel_highway_oc, p_steel_two_oc], axis=1)

# Steel road stock in kt #
p_steel_one_lane_sc = m_one_lane_road_sc.iloc[:, 0].to_frame() @ One_lane_road_MI.iloc[:, 2].to_numpy()
p_steel_highway_sc = m_highway_sc.iloc[:, 0].to_frame() @ Highway_MI.iloc[:, 2].to_numpy()
p_steel_two_sc = m_two_sc.iloc[:, 0].to_frame() @ Two_lane_road_MI.iloc[:, 2].to_numpy()
p_steel_total_sc = p_steel_one_lane_sc + p_steel_highway_sc + p_steel_two_sc
p_steel_total_cat_sc = pd.concat([p_steel_one_lane_sc, p_steel_highway_sc, p_steel_two_sc], axis=1)

# Steel new construction in kt #ne_
p_steel_total_con = p_steel_total_i - p_steel_total_oc
p_steel_total_cat_con = p_steel_total_cat_i - p_steel_total_cat_oc

# Steel road inflow in kt #
k_steel_one_lane_i = m_one_lane_road_i.iloc[:, 1].to_frame() @ One_lane_road_MI.iloc[:, 2].to_numpy()
k_steel_highway_i = m_highway_i.iloc[:, 1].to_frame() @ Highway_MI.iloc[:, 2].to_numpy()
k_steel_two_i = m_two_i.iloc[:, 1].to_frame() @ Two_lane_road_MI.iloc[:, 2].to_numpy()
k_steel_meet_i = m_meet_i.iloc[:, 0].to_frame() @ Meeting_free_road_MI.iloc[:, 2].to_numpy()
k_steel_total_i = k_steel_one_lane_i + k_steel_highway_i + k_steel_two_i + k_steel_meet_i
k_steel_total_cat_i = pd.concat([k_steel_one_lane_i, k_steel_highway_i, k_steel_two_i, k_steel_meet_i], axis=1)

# Steel road outflow in kt #
k_steel_one_lane_oc = m_one_lane_road_oc.iloc[:, 1].to_frame() @ One_lane_road_MI.iloc[:, 2].to_numpy()
k_steel_highway_oc = m_highway_oc.iloc[:, 1].to_frame() @ Highway_MI.iloc[:, 2].to_numpy()
k_steel_two_oc = m_two_oc.iloc[:, 1].to_frame() @ Two_lane_road_MI.iloc[:, 2].to_numpy()
k_steel_meet_oc = m_meet_oc.iloc[:, 0].to_frame() @ Meeting_free_road_MI.iloc[:, 2].to_numpy()
k_steel_total_oc = k_steel_one_lane_oc + k_steel_highway_oc + k_steel_two_oc + k_steel_meet_oc
k_steel_total_cat_oc = pd.concat([k_steel_one_lane_oc, k_steel_highway_oc, k_steel_two_oc, k_steel_meet_oc], axis=1)

# Steel road stock in kt #
k_steel_one_lane_sc = m_one_lane_road_sc.iloc[:, 1].to_frame() @ One_lane_road_MI.iloc[:, 2].to_numpy()
k_steel_highway_sc = m_highway_sc.iloc[:, 1].to_frame() @ Highway_MI.iloc[:, 2].to_numpy()
k_steel_two_sc = m_two_sc.iloc[:, 1].to_frame() @ Two_lane_road_MI.iloc[:, 2].to_numpy()
k_steel_meet_sc = m_meet_sc.iloc[:, 0].to_frame() @ Meeting_free_road_MI.iloc[:, 2].to_numpy()
k_steel_total_sc = k_steel_one_lane_sc + k_steel_highway_sc + k_steel_two_sc + k_steel_meet_sc
k_steel_total_cat_sc = pd.concat([k_steel_one_lane_sc, k_steel_highway_sc, k_steel_two_sc, k_steel_meet_sc], axis=1)

# Steel new construction in kt #ne_
k_steel_total_con = k_steel_total_i - k_steel_total_oc
k_steel_total_cat_con = k_steel_total_cat_i - k_steel_total_cat_oc

# Steel road inflow in kt #
s_steel_one_lane_i = m_one_lane_road_i.iloc[:, 2].to_frame() @ One_lane_road_MI.iloc[:, 2].to_numpy()
s_steel_highway_i = m_highway_i.iloc[:, 2].to_frame() @ Highway_MI.iloc[:, 2].to_numpy()
s_steel_two_i = m_two_i.iloc[:, 2].to_frame() @ Two_lane_road_MI.iloc[:, 2].to_numpy()
s_steel_meet_i = m_meet_i.iloc[:, 1].to_frame() @ Meeting_free_road_MI.iloc[:, 2].to_numpy()
s_steel_total_i = s_steel_one_lane_i + s_steel_highway_i + s_steel_two_i + s_steel_meet_i
s_steel_total_cat_i = pd.concat([s_steel_one_lane_i, s_steel_highway_i, s_steel_two_i, s_steel_meet_i], axis=1)

# Steel road outflow in kt #
s_steel_one_lane_oc = m_one_lane_road_oc.iloc[:, 2].to_frame() @ One_lane_road_MI.iloc[:, 2].to_numpy()
s_steel_highway_oc = m_highway_oc.iloc[:, 2].to_frame() @ Highway_MI.iloc[:, 2].to_numpy()
s_steel_two_oc = m_two_oc.iloc[:, 2].to_frame() @ Two_lane_road_MI.iloc[:, 2].to_numpy()
s_steel_meet_oc = m_meet_oc.iloc[:, 1].to_frame() @ Meeting_free_road_MI.iloc[:, 2].to_numpy()
s_steel_total_oc = s_steel_one_lane_oc + s_steel_highway_oc + s_steel_two_oc + s_steel_meet_oc
s_steel_total_cat_oc = pd.concat([s_steel_one_lane_oc, s_steel_highway_oc, s_steel_two_oc, s_steel_meet_oc], axis=1)

# Steel road stock in kt #
s_steel_one_lane_sc = m_one_lane_road_sc.iloc[:, 2].to_frame() @ One_lane_road_MI.iloc[:, 2].to_numpy()
s_steel_highway_sc = m_highway_sc.iloc[:, 2].to_frame() @ Highway_MI.iloc[:, 2].to_numpy()
s_steel_two_sc = m_two_sc.iloc[:, 2].to_frame() @ Two_lane_road_MI.iloc[:, 2].to_numpy()
s_steel_meet_sc = m_meet_sc.iloc[:, 1].to_frame() @ Meeting_free_road_MI.iloc[:, 2].to_numpy()
s_steel_total_sc = s_steel_one_lane_sc + s_steel_highway_sc + s_steel_two_sc + s_steel_meet_sc
s_steel_total_cat_sc = pd.concat([s_steel_one_lane_sc, s_steel_highway_sc, s_steel_two_sc, s_steel_meet_sc], axis=1)

# Steel new construction in kt #ne_
s_steel_total_con = s_steel_total_i - s_steel_total_oc
s_steel_total_cat_con = s_steel_total_cat_i - s_steel_total_cat_oc

# Summing up steel #
steel_total_i = p_steel_total_i + k_steel_total_i + s_steel_total_i
steel_total_cat_i = pd.concat([p_steel_total_i,  k_steel_total_i, s_steel_total_i], axis=1)
steel_total_oc = p_steel_total_oc + k_steel_total_oc + s_steel_total_oc
steel_total_cat_oc = pd.concat([p_steel_total_oc,  k_steel_total_oc, s_steel_total_oc], axis=1)

steel_total_sc = p_steel_total_sc + k_steel_total_sc + s_steel_total_sc
steel_total_cat_sc = pd.concat([p_steel_total_sc,  k_steel_total_sc, s_steel_total_sc], axis=1)

steel_total_con = steel_total_i - steel_total_oc
steel_total_cat_con = steel_total_cat_i - steel_total_cat_oc

#road.groupby(['Vaghallartyp','MI Category'])['Length'].sum().unstack().plot(kind='bar', stacked =True, color=['#005F73', '#0A9396', '#94D2BD', '#E9D8A6', '#EE9B00'])
#print(test)

#test.plot(kind='bar', stacked =True)

#sns.barplot(data=test, x="Vaghallartyp", y="Length")

# Plotting #
cm = 1/2.54  # centimeters in inches

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(19*cm, 19*cm))
#fig.tight_layout()

road_plot = road
road_plot['Area'] = road_plot['Bredd'] * road_plot['Length']

road_plot['Area'] = road_plot['Area'] /1000000000
road_plot['Length'] = road_plot['Length'] /1000000000

road_plot.groupby(['Vaghallartyp','MI Category'])['Length'].sum().unstack().plot(ax=ax1,kind='bar', stacked =True, color=['#005F73', '#0A9396', '#94D2BD', '#E9D8A6', '#EE9B00'])
road_plot.groupby(['Vaghallartyp','MI Category'])['Area'].sum().unstack().plot(ax=ax2, kind='bar', stacked =True, color=['#005F73', '#0A9396', '#94D2BD', '#E9D8A6', '#EE9B00'])

plt.xticks(rotation=0)

test = pd.concat([grv_total_cat_sc.iloc[[18]],  asp_total_cat_sc.iloc[[18]], steel_total_cat_sc.iloc[[18]]], axis=0)
index = pd.Index(['Gravel', 'Asphalt', 'Steel'])
test = test.set_index(index)
test.columns = ['private', 'municipal', 'state']
test = test.T

municipal_steel = k_steel_total_cat_sc.iloc[[18]]
municipal_steel['4'] = 0
municipal_steel.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road', 'Gravel road']
municipal_gravel = k_grv_total_cat_sc.iloc[[18]]
municipal_gravel.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road', 'Gravel road']
municipal_asphalt = k_asp_total_cat_sc.iloc[[18]]
municipal_asphalt['4'] = 0
municipal_asphalt.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road', 'Gravel road']

municipal_stock = municipal_gravel + municipal_asphalt + municipal_steel
index = pd.Index(['municipal'])
municipal_stock = municipal_stock.set_index(index)

private_steel = p_steel_total_cat_sc.iloc[[18]]
private_steel['3'] = 0
private_steel['4'] = 0
private_steel.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road', 'Gravel road']
private_gravel = p_grv_total_cat_sc.iloc[[18]]
private_gravel.insert(3, '3' , 0)
private_gravel.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road', 'Gravel road']
private_asphalt = p_asp_total_cat_sc.iloc[[18]]
private_asphalt['3'] = 0
private_asphalt['4'] = 0
private_asphalt.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road', 'Gravel road']

private_stock = private_gravel + private_asphalt + private_steel
index = pd.Index(['private'])
private_stock = private_stock.set_index(index)

state_steel = s_steel_total_cat_sc.iloc[[18]]
state_steel['4'] = 0
state_steel.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road', 'Gravel road']
state_gravel = s_grv_total_cat_sc.iloc[[18]]
state_gravel.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road', 'Gravel road']
state_asphalt = s_asp_total_cat_sc.iloc[[18]]
state_asphalt['4'] = 0
state_asphalt.columns = ['One lane road', 'Highway', 'Two lane road', 'Meeting free road', 'Gravel road']

state_stock = state_gravel + state_asphalt + state_steel
index = pd.Index(['state'])
state_stock = state_stock.set_index(index)

stock_holder = pd.concat([private_stock, municipal_stock, state_stock], axis =0)
stock_holder = stock_holder/1000000000
stock_holder = stock_holder.reindex(columns=['Gravel road', 'Highway', 'Meeting free road', 'One lane road', 'Two lane road'])

test = test/1000000000
test.plot(ax=ax4, kind='bar', stacked =True, color=['#1D3557', '#457B9D', '#A8DADC'])

#(asp_total_cat_sc.iloc[[12]]).plot(kind='bar', color=['red', 'skyblue', 'green'])
stock_holder.plot(ax=ax3, kind='bar', stacked =True, color=['#005F73', '#0A9396', '#94D2BD', '#E9D8A6', '#EE9B00'])
#(asp_total_cat_sc.iloc[-21:]).plot(kind='bar', stacked=True, color=['red', 'skyblue', 'green'])

def format_func(N, tick_number):
    N
    if N == 0:
        return "0"
    else:
        return "{0:0.2}".format(N)

formatter = FuncFormatter(format_func)

labels = ['private', 'municipal', 'state']
ax1.set_xticklabels(labels)
ax2.set_xticklabels(labels)

ax1.legend(loc = "upper right",fontsize=9)
#ax1.legend().set_visible(False)
ax2.legend(loc = "upper right",fontsize=9)
#ax2.legend().set_visible(False)
ax3.legend(loc = "upper left",fontsize=9)
#ax3.legend().set_visible(False)
ax4.legend(loc = "upper left",fontsize=9)
#ax4.legend().set_visible(False)

ax1.tick_params(axis='x', rotation=0)
ax2.tick_params(axis='x', rotation=0)
ax3.tick_params(axis='x', rotation=0)
ax4.tick_params(axis='x', rotation=0)

ax1.set_title('Road Length')
ax2.set_title('Road Area')
ax3.set_title('Material stock')
ax4.set_title('Material stock')

ax1.yaxis.set_major_formatter(formatter)
ax2.yaxis.set_major_formatter(formatter)
ax3.yaxis.set_major_formatter(formatter)
ax4.yaxis.set_major_formatter(formatter)

ax1.set_xlabel(xlabel='Road ownership',fontsize=10)
ax2.set_xlabel(xlabel='Road ownership',fontsize=10)
ax3.set_xlabel(xlabel='Road ownership',fontsize=10)
ax4.set_xlabel(xlabel='Road ownership',fontsize=10)

ax1.set_ylabel(ylabel='Length [$10^{9}$ m]',fontsize=10)
ax2.set_ylabel(ylabel='Area [$10^{9}$ $m^{2}$]',fontsize=10)
ax3.set_ylabel(ylabel='Stock [$10^{9}$ ton]',fontsize=10)
ax4.set_ylabel(ylabel='Stock [$10^{9}$ ton]',fontsize=10)

fig.tight_layout(pad=2.0)
plt.savefig("stock.png", dpi=500)
plt.show()

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharey='row', figsize=(14*cm, 14*cm))

asp_real_i.iloc[-26:].plot(ax=ax1, kind='bar', color='#457B9D')
asp_total_oc.iloc[-26:].plot(ax=ax2, kind='bar', color='#457B9D')

steel_total_i.iloc[-26:].plot(ax=ax3, kind='bar', color='#A8DADC')
steel_total_oc.iloc[-26:].plot(ax=ax4, kind='bar', color='#A8DADC')

ax1.tick_params(axis='x', rotation=0)
ax2.tick_params(axis='x', rotation=0)
ax3.tick_params(axis='x', rotation=0)
ax4.tick_params(axis='x', rotation=0)

ax1.set_xlabel(xlabel='Years',fontsize=12,labelpad=5)
ax2.set_xlabel(xlabel='Years',fontsize=12,labelpad=5)
ax3.set_xlabel(xlabel='Years',fontsize=12,labelpad=5)
ax4.set_xlabel(xlabel='Years',fontsize=12,labelpad=5)

ax1.set_ylabel(ylabel='Asphalt [ton]',fontsize=12,labelpad=5)
ax3.set_ylabel(ylabel='Steel [ton]',fontsize=12,labelpad=5)

ax1.set_title('Inflow', fontweight="bold")
ax2.set_title('Outflow', fontweight="bold")
ax3.set_title('Inflow', fontweight="bold")
ax4.set_title('Outflow', fontweight="bold")

ax1.tick_params(axis='x', rotation=45)
ax2.tick_params(axis='x', rotation=45)
ax3.tick_params(axis='x', rotation=45)
ax4.tick_params(axis='x', rotation=45)

ax1.yaxis.set_major_formatter(formatter)
ax3.yaxis.set_major_formatter(formatter)

fig.tight_layout(pad=1.0)
plt.savefig("flows.png", dpi=500)
plt.show()

# Embodied Emissions#
asp_ef = pd.read_excel('Emission factors.xlsx', sheet_name='Asphalt', index_col=0, header=None)
steel_ef = pd.read_excel('Emission factors.xlsx', sheet_name='Steel', index_col=0, header=None)
grv_ef = pd.read_excel('Emission factors.xlsx', sheet_name='Gravel', index_col=0, header=None)

asp_ef_bau = asp_ef.iloc[:,0]
asp_ef_red = asp_ef.iloc[:,1]

steel_ef_bau = steel_ef.iloc[:,0]
steel_ef_red = steel_ef.iloc[:,1]

grv_ef_bau = grv_ef.iloc[:,0]
grv_ef_red = grv_ef.iloc[:,1]

p_asp_bau = asp_real_cat_i.iloc[:,0] * asp_ef_bau
k_asp_bau = asp_real_cat_i.iloc[:,1] * asp_ef_bau
s_asp_bau = asp_real_cat_i.iloc[:,2] * asp_ef_bau

p_steel_bau = steel_total_cat_i.iloc[:,0] * steel_ef_bau
k_steel_bau = steel_total_cat_i.iloc[:,1] * steel_ef_bau
s_steel_bau = steel_total_cat_i.iloc[:,2] * steel_ef_bau

p_grv_bau = grv_total_new_cat_i.iloc[:,0] * grv_ef_bau
k_grv_bau = grv_total_new_cat_i.iloc[:,1] * grv_ef_bau
s_grv_bau = grv_total_new_cat_i.iloc[:,2] * grv_ef_bau

p_emission_bau = p_asp_bau + p_steel_bau + p_grv_bau
k_emission_bau = k_asp_bau + k_steel_bau + k_grv_bau
s_emission_bau = s_asp_bau + s_steel_bau + s_grv_bau

p_asp_red = asp_real_cat_i.iloc[:,0] * asp_ef_red
k_asp_red = asp_real_cat_i.iloc[:,1] * asp_ef_red
s_asp_red = asp_real_cat_i.iloc[:,2] * asp_ef_red

p_steel_red = steel_total_cat_i.iloc[:,0] * steel_ef_red
k_steel_red = steel_total_cat_i.iloc[:,1] * steel_ef_red
s_steel_red = steel_total_cat_i.iloc[:,2] * steel_ef_red

p_grv_red = grv_total_new_cat_i.iloc[:,0] * grv_ef_red
k_grv_red = grv_total_new_cat_i.iloc[:,1] * grv_ef_red
s_grv_red = grv_total_new_cat_i.iloc[:,2] * grv_ef_red

p_emission_red = p_asp_red + p_steel_red + p_grv_red
k_emission_red = k_asp_red + k_steel_red + k_grv_red
s_emission_red = s_asp_red + s_steel_red + s_grv_red

p_n_asp_bau = asp_total_new_cat_i.iloc[:,0] * asp_ef_bau
k_n_asp_bau = asp_total_new_cat_i.iloc[:,1] * asp_ef_bau
s_n_asp_bau = asp_total_new_cat_i.iloc[:,2] * asp_ef_bau

p_n_steel_bau = steel_total_cat_con.iloc[:,0] * steel_ef_bau
k_n_steel_bau = steel_total_cat_con.iloc[:,1] * steel_ef_bau
s_n_steel_bau = steel_total_cat_con.iloc[:,2] * steel_ef_bau

p_n_asp_red = asp_total_new_cat_i.iloc[:,0] * asp_ef_red
k_n_asp_red = asp_total_new_cat_i.iloc[:,1] * asp_ef_red
s_n_asp_red = asp_total_new_cat_i.iloc[:,2] * asp_ef_red

p_n_steel_red = steel_total_cat_con.iloc[:,0] * steel_ef_red
k_n_steel_red = steel_total_cat_con.iloc[:,1] * steel_ef_red
s_n_steel_red = steel_total_cat_con.iloc[:,2] * steel_ef_red

p_m_asp_bau = asp_total_cat_i.iloc[:,0] * asp_ef_bau
k_m_asp_bau = asp_total_cat_i.iloc[:,1] * asp_ef_bau
s_m_asp_bau = asp_total_cat_i.iloc[:,2] * asp_ef_bau

p_m_steel_bau = steel_total_cat_oc.iloc[:,0] * steel_ef_bau
k_m_steel_bau = steel_total_cat_oc.iloc[:,1] * steel_ef_bau
s_m_steel_bau = steel_total_cat_oc.iloc[:,2] * steel_ef_bau

p_m_asp_red = asp_total_cat_i.iloc[:,0] * asp_ef_red
k_m_asp_red = asp_total_cat_i.iloc[:,1] * asp_ef_red
s_m_asp_red = asp_total_cat_i.iloc[:,2] * asp_ef_red

p_m_steel_red = steel_total_cat_oc.iloc[:,0] * steel_ef_red
k_m_steel_red = steel_total_cat_oc.iloc[:,1] * steel_ef_red
s_m_steel_red = steel_total_cat_oc.iloc[:,2] * steel_ef_red

n_emissions_bau = p_n_asp_bau + k_n_asp_bau + s_n_asp_bau + p_n_steel_bau + k_n_steel_bau + s_n_steel_bau  + p_grv_bau + k_grv_bau + s_grv_bau
m_emissions_bau = p_m_asp_bau + k_m_asp_bau + s_m_asp_bau + p_m_steel_bau + k_m_steel_bau + s_m_steel_bau  + p_grv_bau + k_grv_bau + s_grv_bau

n_emissions_red = p_n_asp_red + k_n_asp_red + s_n_asp_red + p_n_steel_red + k_n_steel_red + s_n_steel_red  + p_grv_red + k_grv_red + s_grv_red
m_emissions_red = p_m_asp_red + k_m_asp_red + s_m_asp_red + p_m_steel_red + k_m_steel_red + s_m_steel_red  + p_grv_red + k_grv_red + s_grv_red

emission_red_c = pd.concat([m_emissions_red , n_emissions_red], axis = 1)
emission_red_c.columns = ['Maintenance', 'New construction']

emission_bau_c = pd.concat([m_emissions_bau , n_emissions_bau], axis = 1)
emission_bau_c.columns = ['Maintenance', 'New construction']

emission_red_c = emission_red_c /1000000 # convert to mt
emission_bau_c = emission_bau_c /1000000 # convert to mt

fig, ((ax1, ax2)) = plt.subplots(1, 2, sharey='row', figsize=(14*cm, 14*cm))
emission_bau_c.iloc[-26:].plot(ax=ax1, kind='area', stacked='True', color=['#E29578', '#FFDDD2'])
emission_red_c.iloc[-26:].plot(ax=ax2, kind='area', stacked='True', color=['#E29578', '#FFDDD2'])



ax1.set_xlabel(xlabel='Years',fontsize=10,labelpad=0)
ax2.set_xlabel(xlabel='Years',fontsize=10,labelpad=0)

ax1.set_ylabel(ylabel='Embodied emissions [Mton]',fontsize=10,labelpad=0)
ax2.set_ylabel(ylabel='Embodied emissions [Mton]',fontsize=10,labelpad=0)

ax1.set_title('Business as usual')
ax2.set_title('Emission reduction')

ax1.set_box_aspect(1)
ax2.set_box_aspect(1)

tick_spacing = 5

ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
ax2.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

ax1.legend(fontsize="9", loc = "upper right")
ax1.legend().set_visible(False)
ax2.legend(fontsize="8", loc = "upper right")

ax1.yaxis.set_major_formatter(formatter)
ax2.yaxis.set_major_formatter(formatter)

fig.tight_layout(pad=1.0)
plt.savefig("scenario.png", dpi=500)
plt.show()

asp_emission_bau = p_asp_bau + k_asp_bau + s_asp_bau 
steel_emission_bau = p_steel_bau + k_steel_bau + s_steel_bau 
grv_emission_bau = p_grv_bau + k_grv_bau + s_grv_bau

asp_emission_red = p_asp_red + k_asp_red + s_asp_red 
steel_emission_red = p_steel_red + k_steel_red + s_steel_red 
grv_emission_red = p_grv_red + k_grv_red + s_grv_red 

emission_red = pd.concat([asp_emission_red, steel_emission_red, grv_emission_red], axis = 1)
emission_red = emission_red /1000000 # convert to mt
emission_red.columns = ['Asphalt','Steel', 'Aggregates']

emission_bau = pd.concat([asp_emission_bau, steel_emission_bau, grv_emission_bau], axis = 1)
emission_bau = emission_bau /1000000 # convert to mt
emission_bau.columns = ['Asphalt','Steel', 'Aggregates']

emission_bau_h = pd.concat([s_emission_bau, k_emission_bau, p_emission_bau], axis = 1)
emission_bau_h = emission_bau_h /1000000 # convert to mt
emission_bau_h.columns = ['State', 'Municipal', 'Private']

emission_red_h = pd.concat([s_emission_red, k_emission_red, p_emission_red], axis = 1)
emission_red_h = emission_red_h /1000000 # convert to mt
emission_red_h.columns = ['State', 'Municipal', 'Private']

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharey='row', figsize=(14*cm, 14*cm))

emission_bau.iloc[-26:].plot(ax= ax1, kind='area', stacked='True', color=['#1D3557','#A8DADC', '#457B9D'])
emission_red.iloc[-26:].plot(ax= ax2, kind='area', stacked='True', color=['#1D3557','#A8DADC', '#457B9D'])
emission_bau_h.iloc[-26:].plot(ax= ax3, kind='area', stacked='True', color=['#00A896', '#02C39A', '#F0F3BD'])
emission_red_h.iloc[-26:].plot(ax= ax4, kind='area', stacked='True', color=['#00A896', '#02C39A', '#F0F3BD'])

tick_spacing = 5

ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
ax2.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
ax3.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
ax4.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

ax1.set_xlabel(xlabel='Years',fontsize=10,labelpad=0)
ax2.set_xlabel(xlabel='Years',fontsize=10,labelpad=0)
ax3.set_xlabel(xlabel='Years',fontsize=10,labelpad=0)
ax4.set_xlabel(xlabel='Years',fontsize=10,labelpad=0)

ax1.set_ylabel(ylabel='Embodied emissions [Mton]',fontsize=10,labelpad=0)
ax3.set_ylabel(ylabel='Embodied emissions [Mton]',fontsize=10,labelpad=0)

ax1.set_title('Business as usual',fontsize=11)
ax2.set_title('Emission reduction',fontsize=11)
ax3.set_title('Business as usual',fontsize=11)
ax4.set_title('Emission reduction',fontsize=11)

ax1.yaxis.set_major_formatter(formatter)
ax3.yaxis.set_major_formatter(formatter)

ax1.legend(fontsize=9, loc = "upper right")
ax1.legend().set_visible(False)
ax2.legend(fontsize=9, loc = "upper right")
ax3.legend(fontsize=9, loc = "upper right")
ax3.legend().set_visible(False)
ax4.legend(fontsize=9, loc = "upper right")

fig.tight_layout(pad=0.5)
plt.savefig("emissions.png", dpi=500)
plt.show()