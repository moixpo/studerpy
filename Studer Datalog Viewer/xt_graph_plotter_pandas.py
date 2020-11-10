# -*- coding: utf-8 -*-
"""
#  Version  2.2  sept 2020
#  Moix P-O
#  Albedo-Engineering WWW.ALBEDO-ENGINEERING.COM
#  WWW.OFFGRID.CH
#  License GPL-3.0-only ou GPL-3.0-or-later

xt_graph_plotter_pandas.py
"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import xt_all_csv_pandas_import


def build_total_battery_voltages_currents_figure(total_datalog_df):
    all_channels_labels = list(total_datalog_df.columns)

    ################################
    # plot all the channels with battery voltage and current:
    chanels_number_ubat = [i for i, elem in enumerate(all_channels_labels) if "Ubat" in elem]
    chanels_number_ibat = [i for i, elem in enumerate(all_channels_labels) if "Ibat" in elem]

    # fig_bat=plt.figure()
    fig_batt, (axes_bat_u, axes_bat_i) = plt.subplots(nrows=2, ncols=1)

    total_datalog_df.plot(
        y=total_datalog_df.columns[chanels_number_ubat],
        grid=True,
        figsize=(15, 5),
        sharex=True,
        ax=axes_bat_u,
    )

    axes_bat_u.set_ylabel("Voltage [V]", fontsize=12)
    axes_bat_u.set_title("All Battery Voltages", fontsize=12, weight="bold")
    axes_bat_u.grid(True)

    total_datalog_df.plot(
        y=total_datalog_df.columns[chanels_number_ibat],
        figsize=(15, 5),
        grid=True,
        sharex=True,
        ax=axes_bat_i,
    )

    axes_bat_i.set_ylabel("Amperes [A]", fontsize=12)
    axes_bat_i.set_title("All Battery Currents", fontsize=12, weight="bold")
    axes_bat_i.grid(True)
    return fig_batt



def build_battery_voltage_histogram_figure(total_datalog_df, quarters_mean_df):
    all_channels_labels = list(total_datalog_df.columns)
    quarters_channels_labels=list(quarters_mean_df.columns)
    chanels_number_ubat = [i for i, elem in enumerate(all_channels_labels) if "Ubat" in elem]
    chanel_number=chanels_number_ubat[1]
    
    fig_batt_hist, axes_bat_u_hist = plt.subplots(nrows=1, ncols=1)

    quarters_mean_df.plot(
        y=quarters_mean_df.columns[chanels_number_ubat[1]],
        figsize=(12, 6),
        kind="hist",
        bins=40,
        ax=axes_bat_u_hist,
    )
    all_channels_labels
    print(all_channels_labels[chanels_number_ubat[1]])
    
    plt.axvline(quarters_mean_df[quarters_channels_labels[chanel_number]].mean(), color='k', linestyle='dashed', linewidth=2)

    axes_bat_u_hist.set_xlabel("Voltage [V]", fontsize=12)
    axes_bat_u_hist.set_ylabel("occurence", fontsize=12)
    axes_bat_u_hist.set_title("Battery Voltage Histogram", fontsize=12, weight="bold")
    axes_bat_u_hist.grid(True)
    return fig_batt_hist




def build_ac_power_figure(total_datalog_df, quarters_mean_df):
    all_channels_labels = list(total_datalog_df.columns)
    chanels_number_Pactif = [i for i, elem in enumerate(all_channels_labels) if "[kW]" in elem]
    chanels_number_Papparent = [i for i, elem in enumerate(all_channels_labels) if "[kVA]" in elem]
    fig_pow, axes_pow = plt.subplots(nrows=1, ncols=2)

    total_datalog_df.plot(
        y=total_datalog_df.columns[chanels_number_Pactif],
        figsize=(12, 6),
        ax=axes_pow[0],
    )

    axes_pow[0].set_ylabel("Power activ/reactiv [kW/kVA]", fontsize=12)
    axes_pow[0].set_title("All AC-out Powers", fontsize=12, weight="bold")
    axes_pow[0].grid(True)

    total_datalog_df.plot(
        y=total_datalog_df.columns[chanels_number_Papparent],
        marker="+",
        figsize=(12, 6),
        ax=axes_pow[1],
    )
    quarters_mean_df.plot(
        y=quarters_mean_df.columns[chanels_number_Papparent], marker="o", ax=axes_pow[1]
    )
    axes_pow[1].set_ylabel("Power apparent [kVA]", fontsize=12)
    axes_pow[1].set_title("1min and 15min AC-out Power", fontsize=12, weight="bold")
    axes_pow[1].grid(True)
    return fig_pow



def build_power_histogram_figure(quarters_mean_df, total_datalog_df):
    all_channels_labels = list(total_datalog_df.columns)
    quarters_channels_labels=list(quarters_mean_df.columns)
    chanels_number_Pin_actif = [i for i, elem in enumerate(all_channels_labels) if "Pin a" in elem]
    chanels_number_Pout_actif = [i for i, elem in enumerate(all_channels_labels) if "Pout a" in elem]


    #take out the 0kW power (when genset/grid is not connected):    
    #chanel_number=chanels_number_Pin_actif[0]


    channel_number=chanels_number_Pin_actif[0]
    values_for_hist=quarters_mean_df.iloc[:,channel_number]
    values_for_hist2=values_for_hist[values_for_hist > 0.1]
    
    temp=quarters_mean_df.iloc[:,channel_number]
    #values_for_hist[values_for_hist > 0.1]
    values_for_Pin_hist=temp[temp > 0.1]

    
    channel_number=chanels_number_Pout_actif[0]
    values_for_Pout_hist=quarters_mean_df.iloc[:,channel_number]



    fig_hist, axes_hist = plt.subplots()
    
    #    values_for_hist2.plot(
    #        y=values_for_hist,
    #        figsize=(12, 6),
    #        kind="hist",
    #        bins=20,
    #        ax=axes_hist,
    #        density=True
    #    )
    #    quarters_mean_df.plot(
    #        y=quarters_mean_df.columns[chanels_number_Pin_actif[0]],
    #        figsize=(12, 6),
    #        kind="hist",
    #        bins=20,
    #        ax=axes_hist,
    #        density=True
    #    )
    #    quarters_mean_df.plot(
    #        y=quarters_mean_df.columns[chanels_number_Pout_actif[0]],
    #        figsize=(12, 6),
    #        kind="hist",
    #        bins=20,
    #        ax=axes_hist,
    #        density=True,
    #        alpha=0.5
    #    )
    
    values_for_Pout_hist.hist( bins=50, alpha=0.5, label="Pout",density=True)
    values_for_Pin_hist.hist( bins=50, alpha=0.5, label="Pin", density=True)
    plt.axvline(quarters_mean_df[quarters_channels_labels[channel_number]].mean(), color='k', linestyle='dashed', linewidth=2)

    axes_hist.set_title("Histogram of Powers (without 0 kW for Pin)", fontsize=12, weight="bold")
    axes_hist.set_xlabel("Power [kW]", fontsize=12)
    axes_hist.set_ylabel("Frequency density", fontsize=12)
    axes_hist.legend(loc='upper right')


    axes_hist.grid(True)
    
    



    return fig_hist


def build_voltage_versus_current_figure(total_datalog_df):
    all_channels_labels = list(total_datalog_df.columns)
    chanels_number_ubatbsp = [i for i, elem in enumerate(all_channels_labels) if "BSP-Ubat" in elem]
    chanels_number_ibatbsp = [i for i, elem in enumerate(all_channels_labels) if "BSP-Ibat" in elem]
    

    #take out the points with negative current only:
    channel_number=chanels_number_ibatbsp[0]
    
    #copy only voltage and current
    voltage_current_only_df=total_datalog_df[[all_channels_labels[chanels_number_ubatbsp[0]],
                                             all_channels_labels[chanels_number_ibatbsp[0]]]]
    
    #keep rows with negativ current:
    voltage_neg_current_only_df=voltage_current_only_df[voltage_current_only_df[all_channels_labels[chanels_number_ibatbsp[0]]]<0.0]
    
    #keep rows with positiv current:
    voltage_pos_current_only_df=voltage_current_only_df[voltage_current_only_df[all_channels_labels[chanels_number_ibatbsp[0]]]>=0.0]


    fig_batt, axes_batt = plt.subplots(nrows=1, ncols=1)
    
    #    axes_batt.scatter(
    #        total_datalog_df.values[:, chanels_number_ubatbsp],
    #        total_datalog_df.values[:, chanels_number_ibatbsp],
    #        alpha=0.25
    #    )
    axes_batt.scatter(voltage_neg_current_only_df.values[:,0],
                      voltage_neg_current_only_df.values[:,1], 
                      alpha=0.25)
    
    
    axes_batt.scatter(voltage_pos_current_only_df.values[:,0],
                      voltage_pos_current_only_df.values[:,1], 
                      alpha=0.25)

    axes_batt.set_ylabel("Amperes [A]", fontsize=12)
    axes_batt.set_xlabel("Voltage [V]", fontsize=12)
    axes_batt.set_title("Voltage VS Currents measured by BSP", fontsize=12, weight="bold")
    axes_batt.grid(True)
    
    



    return fig_batt


def build_solar_production_figure(total_datalog_df):
    all_channels_labels = list(total_datalog_df.columns)
    chanel_number_for_solar = [
        i for i, elem in enumerate(all_channels_labels) if "Solar power (ALL) [kW]" in elem
    ]

    fig_solar, axes_solar = plt.subplots(nrows=1, ncols=1, figsize=(15, 5))

    total_datalog_df.plot(
        y=total_datalog_df.columns[chanel_number_for_solar],
        figsize=(12, 6),
        ax=axes_solar,
    )
    axes_solar.set_ylabel("Power [kW]", fontsize=12)
    axes_solar.set_title("Solar Production", fontsize=12, weight="bold")
    axes_solar.grid(True)
    return fig_solar


def build_genset_time_figure(total_datalog_df):
    all_channels_labels = list(total_datalog_df.columns)
    chanel_number_for_transfer = [
        i for i, elem in enumerate(all_channels_labels) if "XT-Transfert" in elem
    ]
    minutes_without_transfer = np.count_nonzero(
        total_datalog_df.values[:, chanel_number_for_transfer] == 0.0
    )
    minutes_with_transfer = np.count_nonzero(
        total_datalog_df.values[:, chanel_number_for_transfer] == 1.0
    )

    len(total_datalog_df.values[:, chanel_number_for_transfer])

    labels = [
        "on grid/genset: " + str(round(minutes_with_transfer / 60, 1)) + " hours",
        "on inverter: " + str(round(minutes_without_transfer / 60, 1)) + " hours",
    ]
    fig_transfer = plt.figure()
    ax_transfer = fig_transfer.add_subplot(111)
    ax_transfer.pie(
        [minutes_with_transfer, minutes_without_transfer],
        labels=labels,
        shadow=True,
        startangle=90,
        autopct="%1.1f%%",
    )
    return fig_transfer


def build_all_battery_voltages_figure(total_datalog_df, month_mean_df):
    all_channels_labels = list(total_datalog_df.columns)
    chanels_number_ubat = [i for i, elem in enumerate(all_channels_labels) if "Ubat" in elem]
    fig_batt_anlys, axes_batt_anlys = plt.subplots(nrows=1, ncols=1, figsize=(15, 5))
    # axes4_2 = axes4.twinx()

    total_datalog_df.plot(
        y=total_datalog_df.columns[chanels_number_ubat],
        figsize=(15, 5),
        grid=True,
        title="All Battery Voltages",
        ax=axes_batt_anlys,
    )

    month_mean_df.plot(
        y=month_mean_df.columns[chanels_number_ubat[1]], color="r", ax=axes_batt_anlys
    )

    axes_batt_anlys.set_ylabel("Voltage [V]", fontsize=12)
    axes_batt_anlys.set_title("All Battery Voltages", fontsize=12, weight="bold")
    axes_batt_anlys.grid(True)
    return fig_batt_anlys


def build_montly_energies_figure(total_datalog_df):
    month_kwh_df = total_datalog_df.resample("1M").sum() / 60
    fig_ener, axes_ener = plt.subplots(nrows=1, ncols=1, figsize=(15, 5))

    # month_kwh_df['XT-Pout a [kW] I3101 L1-1'].plot(grid=True,
    #                      kind='line',
    #                      marker='o',
    #                      color='red',
    #                      ax=axes_ener)

    month_kwh_df[
        [
            "Solar power (ALL) [kW] I17999 ALL",
            "XT-Pin a [kW] I3119 L1-1",
            "XT-Pout a [kW] I3101 L1-1",
        ]
    ].plot.bar(grid=True, stacked=False, ax=axes_ener)

    axes_ener.set_ylabel("Energy [kWh]", fontsize=12)
    axes_ener.set_title("Monthly Energies", fontsize=12, weight="bold")
    axes_ener.grid(True)
    return fig_ener


def build_montly_energies_figure2(total_datalog_df):
    month_kwh_df = total_datalog_df.resample("1M").sum() / 60
    fig_ener2, axes_ener2 = plt.subplots(nrows=1, ncols=1, figsize=(9, 9))
    month_kwh_df[["Solar power (ALL) [kW] I17999 ALL", "XT-Pin a [kW] I3119 L1-1"]].plot.bar(
        stacked=True, 
        ax=axes_ener2, 
        use_index=False, 
        align="edge", 
        width=0.5
    )

    month_kwh_df["XT-Pout a [kW] I3101 L1-1"].plot(
        kind="bar",
        color="red",
        align="center",
        width=0.5,
        ax=axes_ener2,
        use_index=False,
        alpha=0.5
    )

    month_kwh_df["XT-Pout a [kW] I3101 L1-1"].plot(
        kind="line", marker="o", color="red", ax=axes_ener2, use_index=False
    )

    axes_ener2.set_ylabel("Energy [kWh]", fontsize=12)

    # replace labels with the month name:
    loc, label = plt.xticks()
    plt.xticks(loc, labels=list(month_kwh_df.index.month_name()))

    axes_ener2.set_title("Monthly Energies", fontsize=12, weight="bold")
    axes_ener2.grid(True)
    return fig_ener2


def main():
    total_datalog_df = pd.read_pickle(xt_all_csv_pandas_import.MIN_DATAFRAME_NAME)
    quarters_mean_df = pd.read_pickle(xt_all_csv_pandas_import.QUARTERS_DATAFRAME_NAME)
    day_mean_df = pd.read_pickle(xt_all_csv_pandas_import.DAY_DATAFRAME_NAME)
    month_mean_df = pd.read_pickle(xt_all_csv_pandas_import.MONTH_DATAFRAME_NAME)
    year_mean_df = pd.read_pickle(xt_all_csv_pandas_import.YEAR_DATAFRAME_NAME)

    #%***************************************
    #% task: compute kWh
    # WARNING: it make sense only for P in KW
    # TODO: make a dataframe for energies
    #%****************************************

    # min to day: *60*24/1000
    # day to month: *60*24/1000

    day_kwh_df = total_datalog_df.resample("1d").sum() / 60
    month_kwh_df = total_datalog_df.resample("1M").sum() / 60
    year_kWh_df = total_datalog_df.resample("1Y").sum() / 60

    # close all existing figures at start
    plt.close("all")

    print(" ")
    print(" __________ GRAPH DISPLAY  _______________ ")
    print(" \n \n \n ")

    all_channels_labels = list(total_datalog_df.columns)
    chanels_number_ubat = [i for i, elem in enumerate(all_channels_labels) if "Ubat" in elem]

    build_total_battery_voltages_currents_figure(total_datalog_df)
    build_battery_voltage_histogram_figure(total_datalog_df, quarters_mean_df)

    ######################################
    # plot all the channels with Power
    # fig100=plt.figure(100)
    build_ac_power_figure(total_datalog_df, quarters_mean_df)
    build_power_histogram_figure(quarters_mean_df, total_datalog_df)

    ######################
    # Battery analysis
    ######
    build_voltage_versus_current_figure(total_datalog_df)

    #######
    ## Charge /discharge power
    ########
    chanels_number_ubatbsp = [i for i, elem in enumerate(all_channels_labels) if "BSP-Ubat" in elem]
    chanels_number_ibatbsp = [i for i, elem in enumerate(all_channels_labels) if "BSP-Ibat" in elem]
    battery_power = (
        total_datalog_df.values[:, chanels_number_ubatbsp]
        * total_datalog_df.values[:, chanels_number_ibatbsp]
        / 1000
    )

    # battery_power_df=pd.DataFrame({"Battery Power [kW]": battery_power,
    #                               "Battery Charge Power [kW]": battery_power,
    #                               "Battery Discharge Power [kW]": battery_power},
    #                                index=total_datalog_df.index)
    #
    #

    # plt.show

    ##########
    # Solar Power:
    ############
    build_solar_production_figure(total_datalog_df)

    ##########
    # Time on the genset:
    ############
    build_genset_time_figure(total_datalog_df)
    # plt.show()

    # Analyse Batterie
    build_all_battery_voltages_figure(total_datalog_df, month_mean_df)

    # axes4.bar(x=month_mean_df.index,
    #        y=total_datalog_df.columns[chanels_number_ubat],
    #        color='r',
    #        ax=axes4_2)
    #
    # axes4.plot(x=total_datalog_df.index,
    #         y=total_datalog_df.columns[chanels_number_ubat],
    #         grid=True,
    #         title='All Battery Voltages',
    #         ax=axes4)

    # Energies Mensuelles:

    # month_kwh_df['XT-Pout a [kW] I3101 L1-1']
    build_montly_energies_figure(total_datalog_df)
    build_montly_energies_figure2(total_datalog_df)
    plt.show()


#######
## HEAT MAPS:  TODO  for the daily consumption
########
# https://scipython.com/book/chapter-7-matplotlib/examples/a-heatmap-of-boston-temperatures/
# https://vietle.info/post/calendarheatmap-python/


##minimal battery voltage
# chanel_number=single_days['channels_label'].index('XT-Ubat- (MIN) [Vdc]')
# XT_batt_valmin=total_datalog_value[:,chanel_number]
#
##battery voltage
# chanel_number=single_days['channels_label'].index('XT-Ubat [Vdc]')
# XT_batt_val=total_datalog_value[:,chanel_number]
#
#
# chanel_number=single_days['channels_label'].index('BSP-Ubat [Vdc]')
# BSP_batt_val=total_datalog_value[:,chanel_number]
#
# chanel_number=single_days['channels_label'].index('BSP-Ibat [Adc]')
# BSP_I_batt_val=total_datalog_value[:,chanel_number]
#
##'BSP-Ubat [Vdc]',
## 'BSP-Ibat [Adc]',
## 'BSP-SOC [%]',
## 'BSP-Tbat [°C]',
#
#
#
# chanel_number=single_days['channels_label'].index('XT-Pin a [kW]')
# grid_power=total_datalog_value[:,chanel_number]
#
#
# print(" ************* ")
# print("BEWARE: for 3-phased systems, the sum of the three inverters")
# grid_power=total_datalog_value[:,chanel_number]+total_datalog_value[:,chanel_number+1]+total_datalog_value[:,chanel_number+2]
# print(" comment this line if not the case ")
# print(" ************* ")
# print("  ")
# minutes_of_the_day=total_time_vectors
#
#
#
#
# fig1=plt.figure(1)
# plt.clf()
# plt.plot(minutes_of_the_day/60/24, XT_batt_val, 'b')
# plt.plot(minutes_of_the_day/60/24, BSP_batt_val, 'g')
# plt.plot(minutes_of_the_day/60/24, XT_batt_valmin,'y+-')
#
# plt.xlabel('Time (days)', fontsize=12)
# plt.ylabel('Voltage [V]', fontsize=12)
# plt.title('Battery Voltage', fontsize=18, weight="bold")
#
# plt.ax = fig1.gca()
# plt.ax.grid(True)
#
# plt.show()
# fig1.legend(['mesure XT', 'mesure BSP', 'xt min'])
#
#
# fig2=plt.figure(2)
# plt.clf()
# plt.hist(BSP_batt_val, 25, facecolor='r', alpha=0.75)
#
# plt.xlabel('Voltage [V]')
# plt.ylabel('Occurence')
# plt.title('Histogram of Battery Voltage')
#
##plt.text(52, 25, r'$\mu=100,\ \sigma=15$')
##plt.axis([40, 60, 0, 0.03])
# plt.grid(True)
# plt.show()
#
# plt.ax = fig2.gca()
# plt.ax.grid(True)
#
#
#


if __name__ == "__main__":
    main()
