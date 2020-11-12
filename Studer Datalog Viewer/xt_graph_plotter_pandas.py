# -*- coding: utf-8 -*-
"""
#  Version  2.3  nov 2020
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


#colorset
PINK_COLOR="#FFB2C7"
RED_COLOR="#CC0000"
WHITE_COLOR="#FFFFFF"
LIGHT_GREEN_COLOR="#eafff5"

A_RED_COLOR="#9A031E"
A_YELLOW_COLOR="#F7B53B"
A_BLUE_COLOR="#2E5266"
A_RAISINBLACK_COLOR="#272838"
A_BLUEGREY_COLOR="#7E7F9A"
A_GREY_COLOR="#6E8898"
A_GREY_COLOR2="#9FB1BC"
A_GREY_COLOR3="#F9F8F8"



NX_LIGHT_BLUE="#F0F6F8"
NX_BLUE="#6BA3B8"
NX_BROWN="#A2A569"
NX_LIGHT_BROWN="#E3E4D2"
NX_PINK="#B06B96"
NX_GREEN="#78BE20"




#CHOICES:
FIGURE_FACECOLOR=NX_LIGHT_BROWN
AXE_FACECOLOR=WHITE_COLOR
SOLAR_COLOR=A_YELLOW_COLOR
LOAD_COLOR=A_RED_COLOR
GENSET_COLOR=A_BLUE_COLOR


#figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT)
FIGSIZE_WIDTH=15
FIGSIZE_HEIGHT=6
#figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT)






def build_sys_power_figure(total_datalog_df, quarters_mean_df):
    all_channels_labels = list(total_datalog_df.columns)
    
    channels_number_Pin_actif = [i for i, elem in enumerate(all_channels_labels) if "Pin a" in elem]
    channels_number_Pout_actif = [i for i, elem in enumerate(all_channels_labels) if "Pout a" in elem]    
    channels_number_PsolarTot = [i for i, elem in enumerate(all_channels_labels) if 'Solar power (ALL) [kW]' in elem]
    
    
    #TODO: faire les sommes quand il y a plusieurs appareils
    chanel_label_Pout_actif_tot=all_channels_labels[channels_number_Pout_actif[0]]
    chanel_label_Pin_actif_tot=all_channels_labels[channels_number_Pin_actif[0]]
    chanel_label_Psolar_tot=all_channels_labels[channels_number_PsolarTot[0]]
    
    
    #create object figure
    fig_pow, axes_pow = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    #fig_pow.set_facecolor(FIGURE_FACECOLOR)
    
    #total_datalog_df.plot(y=total_datalog_df.columns[channels_number_Pactif],
    #                      ax=axes_pow[0])
    
    total_datalog_df.plot(y=chanel_label_Psolar_tot,                     
                          ax=axes_pow,
                          color=SOLAR_COLOR,
                          legend="Solar")
    
    total_datalog_df.plot(y=chanel_label_Pin_actif_tot,
                          ax=axes_pow,
                          color=GENSET_COLOR,
                          legend="Grid/Genset")
    
    total_datalog_df.plot(y=chanel_label_Pout_actif_tot,
                          ax=axes_pow,
                          color=LOAD_COLOR,
                          legend="Loads")
    
    
    
    axes_pow.set_ylabel('Power activ [kW]', fontsize=12)
    axes_pow.set_title('System Powers', fontsize=12, weight="bold")
    axes_pow.grid(True)
    #axes_pow.set_facecolor(AXE_FACECOLOR)

    return fig_pow






def build_power_histogram_figure(total_datalog_df, quarters_mean_df):
    all_channels_labels = list(total_datalog_df.columns)
    quarters_channels_labels=list(quarters_mean_df.columns)
    channels_number_Pin_actif = [i for i, elem in enumerate(all_channels_labels) if "Pin a" in elem]
    channels_number_Pout_actif = [i for i, elem in enumerate(all_channels_labels) if "Pout a" in elem]


    #take out the 0kW power (when genset/grid is not connected):    
    #chanel_number=channels_number_Pin_actif[0]


    channel_number=channels_number_Pin_actif[0]
    values_for_hist=quarters_mean_df.iloc[:,channel_number]
    values_for_hist2=values_for_hist[values_for_hist > 0.1]
    
    temp=quarters_mean_df.iloc[:,channel_number]
    #values_for_hist[values_for_hist > 0.1]
    values_for_Pin_hist=temp[temp > 0.1]

    
    channel_number=channels_number_Pout_actif[0]
    values_for_Pout_hist=quarters_mean_df.iloc[:,channel_number]

    fig_hist, axes_hist = plt.subplots(figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    
    values_for_Pout_hist.hist( bins=50, alpha=0.5, label="Pout",density=True)
    values_for_Pin_hist.hist( bins=50, alpha=0.5, label="Pin", density=True)
    plt.axvline(quarters_mean_df[quarters_channels_labels[channel_number]].mean(), color='k', linestyle='dashed', linewidth=2)

    axes_hist.set_title("Histogram of Powers (without 0 kW for Pin)", fontsize=12, weight="bold")
    axes_hist.set_xlabel("Power [kW]", fontsize=12)
    axes_hist.set_ylabel("Frequency density", fontsize=12)
    axes_hist.legend(loc='upper right')


    axes_hist.grid(True)

    return fig_hist





def build_total_battery_voltages_currents_figure(total_datalog_df):
    all_channels_labels = list(total_datalog_df.columns)

    ################################
    # plot all the channels with battery voltage and current:
    channels_number_ubat = [i for i, elem in enumerate(all_channels_labels) if "Ubat" in elem]
    channels_number_ibat = [i for i, elem in enumerate(all_channels_labels) if "Ibat" in elem]

    # fig_bat=plt.figure()
    fig_batt, (axes_bat_u, axes_bat_i) = plt.subplots(nrows=2, ncols=1)

    total_datalog_df.plot(
        y=total_datalog_df.columns[channels_number_ubat],
        grid=True,
        figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT),
        sharex=True,
        ax=axes_bat_u,
    )

    axes_bat_u.set_ylabel("Voltage [V]", fontsize=12)
    axes_bat_u.set_title("All Battery Voltages", fontsize=12, weight="bold")
    axes_bat_u.grid(True)

    total_datalog_df.plot(
        y=total_datalog_df.columns[channels_number_ibat],
        figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT),
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
    channels_number_ubat = [i for i, elem in enumerate(all_channels_labels) if "Ubat" in elem]
    chanel_number=channels_number_ubat[1]
    
    fig_batt_hist, axes_bat_u_hist = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

    quarters_mean_df.plot(
        y=quarters_mean_df.columns[channels_number_ubat[1]],
        kind="hist",
        bins=80,
        ax=axes_bat_u_hist,
    )
    all_channels_labels
    #print(all_channels_labels[channels_number_ubat[1]])
    
    plt.axvline(quarters_mean_df[quarters_channels_labels[chanel_number]].mean(), color='k', linestyle='dashed', linewidth=2)

    axes_bat_u_hist.set_xlabel("Voltage [V]", fontsize=12)
    axes_bat_u_hist.set_ylabel("occurence", fontsize=12)
    axes_bat_u_hist.set_title("Battery Voltage Histogram", fontsize=12, weight="bold")
    axes_bat_u_hist.grid(True)
    return fig_batt_hist



def build_battery_chargedischarge_histogram_figure(total_datalog_df, quarters_mean_df):
    all_channels_labels = list(total_datalog_df.columns)
    
    channel_number_ubatbsp = [i for i, elem in enumerate(all_channels_labels) if 'BSP-Ubat' in elem]
    channels_number_ibatbsp = [i for i, elem in enumerate(all_channels_labels) if 'BSP-Ibat' in elem]
    
    #check if there is an BSP or not, else we take the battery voltage from the Xtender
    if total_datalog_df[all_channels_labels[channel_number_ubatbsp[0]]].sum()==0:
        channel_number_ubatbsp = [i for i, elem in enumerate(all_channels_labels) if 'XT-Ubat [Vdc]' in elem]
    
    channel_number_ubat_ref=channel_number_ubatbsp
        
    
    
    battery_power=total_datalog_df.values[:,channel_number_ubatbsp]*total_datalog_df.values[:,channels_number_ibatbsp]/1000
    
    #battery_power_df=pd.DataFrame({"Battery Power [kW]": battery_power,
    #                               "Battery Charge Power [kW]": battery_power,
    #                               "Battery Discharge Power [kW]": battery_power},
    #                                index=total_datalog_df.index)
                   
    
    
    #take out the points with negative current only:
    channel_number=channels_number_ibatbsp[0]
    
    #copy only voltage and current
    voltage_current_only_df=total_datalog_df[[all_channels_labels[channel_number_ubatbsp[0]],
                                             all_channels_labels[channels_number_ibatbsp[0]]]]
    
    #keep rows with negativ current:
    voltage_neg_current_only_df=voltage_current_only_df[voltage_current_only_df[all_channels_labels[channels_number_ibatbsp[0]]]<0.0]
    
    #keep rows with positiv current:
    voltage_pos_current_only_df=voltage_current_only_df[voltage_current_only_df[all_channels_labels[channels_number_ibatbsp[0]]]>=0.0]


    fig_batt_discharge_hist, axes_batt_discharge_hist = plt.subplots(nrows=1, ncols=1)
    
    
    
    
    
    axes_batt_discharge_hist.hist(voltage_neg_current_only_df.values[:,0], 
             bins=50, 
             alpha=0.5, 
             label='Discharge', 
             density=1)
    
    plt.axvline(voltage_neg_current_only_df.values[:,0].mean(), color='k', linestyle='dashed', linewidth=2)
    
    axes_batt_discharge_hist.hist(voltage_pos_current_only_df.values[:,0], 
             bins=50, 
             alpha=0.5, 
             label='Charge', 
             density=1)
    
    axes_batt_discharge_hist.set_ylabel('Frenquency density', fontsize=12)
    axes_batt_discharge_hist.set_xlabel('Voltage [V]', fontsize=12)
    axes_batt_discharge_hist.set_title('Discharge/Charge voltage histograms', fontsize=12, weight="bold")
    axes_batt_discharge_hist.grid(True) 
    axes_batt_discharge_hist.legend(loc='upper right')

    return fig_batt_discharge_hist



def build_ac_power_figure(total_datalog_df, quarters_mean_df):
    all_channels_labels = list(total_datalog_df.columns)
    channels_number_Pactif = [i for i, elem in enumerate(all_channels_labels) if "[kW]" in elem]
    channels_number_Papparent = [i for i, elem in enumerate(all_channels_labels) if "[kVA]" in elem]
    fig_pow, axes_pow = plt.subplots(nrows=1, ncols=2, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

    total_datalog_df.plot(
        y=total_datalog_df.columns[channels_number_Pactif],
        ax=axes_pow[0],
    )

    axes_pow[0].set_ylabel("Power activ/reactiv [kW/kVA]", fontsize=12)
    axes_pow[0].set_title("All AC-out Powers", fontsize=12, weight="bold")
    axes_pow[0].grid(True)

    total_datalog_df.plot(
        y=total_datalog_df.columns[channels_number_Papparent],
        marker="+",
        ax=axes_pow[1],
    )
    quarters_mean_df.plot(
        y=quarters_mean_df.columns[channels_number_Papparent], marker="o", ax=axes_pow[1]
    )
    axes_pow[1].set_ylabel("Power apparent [kVA]", fontsize=12)
    axes_pow[1].set_title("1min and 15min AC-out Power", fontsize=12, weight="bold")
    axes_pow[1].grid(True)
    return fig_pow





def build_voltage_versus_current_figure(total_datalog_df):
    all_channels_labels = list(total_datalog_df.columns)
    channels_number_ubatbsp = [i for i, elem in enumerate(all_channels_labels) if "BSP-Ubat" in elem]
    channels_number_ibatbsp = [i for i, elem in enumerate(all_channels_labels) if "BSP-Ibat" in elem]
    

    #take out the points with negative current only:
    channel_number=channels_number_ibatbsp[0]
    
    #copy only voltage and current
    voltage_current_only_df=total_datalog_df[[all_channels_labels[channels_number_ubatbsp[0]],
                                             all_channels_labels[channels_number_ibatbsp[0]]]]
    
    #keep rows with negativ current:
    voltage_neg_current_only_df=voltage_current_only_df[voltage_current_only_df[all_channels_labels[channels_number_ibatbsp[0]]]<0.0]
    
    #keep rows with positiv current:
    voltage_pos_current_only_df=voltage_current_only_df[voltage_current_only_df[all_channels_labels[channels_number_ibatbsp[0]]]>=0.0]


    fig_batt, axes_batt = plt.subplots(nrows=1, ncols=1,figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    
    #    axes_batt.scatter(
    #        total_datalog_df.values[:, channels_number_ubatbsp],
    #        total_datalog_df.values[:, channels_number_ibatbsp],
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

    fig_solar, axes_solar = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

    total_datalog_df.plot(
        y=total_datalog_df.columns[chanel_number_for_solar],
        ax=axes_solar,
        color=SOLAR_COLOR
    )
    
    axes_solar.set_ylabel("Power [kW]", fontsize=12)
    axes_solar.set_title("Solar Production", fontsize=12, weight="bold")
    axes_solar.grid(True)
    return fig_solar



def build_solar_pv_voltage_figure(total_datalog_df):
    all_channels_labels = list(total_datalog_df.columns)
    chanel_number_for_solar = [
        i for i, elem in enumerate(all_channels_labels) if "Upv [Vdc]" in elem
    ]

    fig_solar, axes_solar = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

    total_datalog_df.plot(
        y=total_datalog_df.columns[chanel_number_for_solar],
        ax=axes_solar,
    )
    axes_solar.set_ylabel("Voltage [Vdc]", fontsize=12)
    axes_solar.set_title("PV input voltage", fontsize=12, weight="bold")
    axes_solar.grid(True)
    return fig_solar


def build_solar_energy_prod_figure(total_datalog_df):

    all_channels_labels = list(total_datalog_df.columns)
    chanel_number_for_solar = [i for i, elem in enumerate(all_channels_labels) if "Solar power (ALL) [kW]" in elem]
    day_kwh_df = total_datalog_df.resample("1d").sum() / 60
    month_kwh_df = total_datalog_df.resample("1M").sum() / 60
    
    
    fig_solar, axes_solar = plt.subplots(nrows=2, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    
    day_kwh_df[day_kwh_df.columns[chanel_number_for_solar]].plot(ax=axes_solar[0],
              kind='line',
              marker='o',
              color=SOLAR_COLOR)
    
    axes_solar[0].set_ylabel("Energy [kWh/day]", fontsize=12)
    axes_solar[0].set_title("PV production per day and per month", fontsize=12, weight="bold")
    axes_solar[0].legend(["Day production"])
    axes_solar[0].grid(True)
    
    
    
    month_kwh_df[month_kwh_df.columns[chanel_number_for_solar]].plot.bar(ax=axes_solar[1],
                          use_index=True)
    
    axes_solar[1].set_ylabel("Energy [kWh/month]", fontsize=12)
    #axes_solar[1].set_title("PV production per month", fontsize=12, weight="bold")
    axes_solar[1].legend(["Month production"])
    axes_solar[1].grid(True)
    
    #replace labels with the month name:
    loc, label= plt.xticks()
    plt.xticks(loc,labels=list(month_kwh_df.index.month_name()) )
    
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
        "On grid/genset: " + str(round(minutes_with_transfer / 60, 1)) + " hours",
        "On inverter: " + str(round(minutes_without_transfer / 60, 1)) + " hours",
    ]
    fig_transfer = plt.figure()
    ax_transfer = fig_transfer.add_subplot(111)
    ax_transfer.pie(
        [minutes_with_transfer, minutes_without_transfer],
        labels=labels,
        shadow=True,
        startangle=90,
        autopct="%1.1f%%",
        colors=[NX_PINK,NX_BLUE],
        explode=(0.1,0.1)
    )
    return fig_transfer


def build_all_battery_voltages_figure(total_datalog_df, month_mean_df):
    all_channels_labels = list(total_datalog_df.columns)
    channels_number_ubat = [i for i, elem in enumerate(all_channels_labels) if "Ubat" in elem]
    fig_batt_anlys, axes_batt_anlys = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    # axes4_2 = axes4.twinx()

    total_datalog_df.plot(
        y=total_datalog_df.columns[channels_number_ubat],
        grid=True,
        title="All Battery Voltages",
        ax=axes_batt_anlys,
    )

    month_mean_df.plot(
        y=month_mean_df.columns[channels_number_ubat[1]], color="r", ax=axes_batt_anlys
    )

    axes_batt_anlys.set_ylabel("Voltage [V]", fontsize=12)
    axes_batt_anlys.set_title("All Battery Voltages", fontsize=12, weight="bold")
    axes_batt_anlys.grid(True)
    return fig_batt_anlys


def build_mean_battery_voltage_figure(month_mean_df,day_mean_df):
    all_channels_labels = list(month_mean_df.columns)
    channels_number_ubatbsp = [i for i, elem in enumerate(all_channels_labels) if "BSP-Ubat" in elem]
    
    #TODO: case sans BSP
    channel_number_ubat_ref= channels_number_ubatbsp[0]
    
    fig_battmeans, axes_battmeans = plt.subplots(nrows=1, ncols=1,figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))   
    
    day_mean_df.plot(y=day_mean_df.columns[channel_number_ubat_ref], 
                     color='r',
                     marker='o',
                     linestyle ='None',
                     grid=True,
                     ax=axes_battmeans,
                     alpha=0.25)
    
    month_mean_df.plot(y=month_mean_df.columns[channel_number_ubat_ref],
                          color='b',
                          ax=axes_battmeans)
    
    axes_battmeans.set_ylabel('Voltage [V]', fontsize=12)
    axes_battmeans.set_title('Monthly and daily mean battery voltages', fontsize=12, weight="bold")
    axes_battmeans.legend(["Day Mean", "Month Mean"])  
    axes_battmeans.grid(True) 
    
    return fig_battmeans




def build_monthly_energies_figure(month_kwh_df):
    #month_kwh_df = total_datalog_df.resample("1M").sum() / 60
    fig_ener, axes_ener = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

    # month_kwh_df['XT-Pout a [kW] I3101 L1-1'].plot(grid=True,
    #                      kind='line',
    #                      marker='o',
    #                      color='red',
    #                      ax=axes_ener)
    
    #normalized energy production
    normed_solar=month_kwh_df["Solar power (ALL) [kW] I17999 ALL"]/(month_kwh_df["Solar power (ALL) [kW] I17999 ALL"]+month_kwh_df["XT-Pin a [kW] I3119 L1-1"])*100
    normed_grid=month_kwh_df["XT-Pin a [kW] I3119 L1-1"]/(month_kwh_df["Solar power (ALL) [kW] I17999 ALL"]+month_kwh_df["XT-Pin a [kW] I3119 L1-1"])*100
    
    #axes_ener.plot.bar
    #plt.bar(normed_solar, color='#b5ffb9', edgecolor='white', width=barWidth, label="group A")
    #plt.bar(normed_grid, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth)
    
    normed_solar.plot.bar(grid=True, stacked=False, ax=axes_ener, color=[SOLAR_COLOR, GENSET_COLOR, LOAD_COLOR])
    normed_grid.plot.bar(grid=True, stacked=False, ax=axes_ener, color=[SOLAR_COLOR, GENSET_COLOR, LOAD_COLOR])

#    month_kwh_df[
#        [
#            "Solar power (ALL) [kW] I17999 ALL",
#            "XT-Pin a [kW] I3119 L1-1"
#        ]
#    ].plot.bar(grid=True, stacked=False, ax=axes_ener, color=[SOLAR_COLOR, GENSET_COLOR, LOAD_COLOR])
#        
    # replace labels with the month name:
    loc, label = plt.xticks()
    plt.xticks(loc, labels=list(month_kwh_df.index.month_name()))        

    axes_ener.set_ylabel("Energy fraction [%]", fontsize=12)
    axes_ener.set_title("Monthly Energy sources shares", fontsize=12, weight="bold")
    axes_ener.legend(["Solar", "Grid/Genset"]);
    axes_ener.grid(True)
    return fig_ener


def build_daily_energies_figure(day_kwh_df):
    fig_ener, axes_ener = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

    # month_kwh_df['XT-Pout a [kW] I3101 L1-1'].plot(grid=True,
    #                      kind='line',
    #                      marker='o',
    #                      color='red',
    #                      ax=axes_ener)

    day_kwh_df[
        [
            "Solar power (ALL) [kW] I17999 ALL",
            "XT-Pin a [kW] I3119 L1-1",
            "XT-Pout a [kW] I3101 L1-1",
        ]
    ].plot( grid=True, 
                stacked=False, 
                ax=axes_ener, 
                color=[SOLAR_COLOR, GENSET_COLOR, LOAD_COLOR],
                marker="o",
                linestyle="None"
                )
        
      

    axes_ener.set_ylabel("Energy [kWh]", fontsize=12)
    axes_ener.set_title("Daily Energies", fontsize=12, weight="bold")
    axes_ener.legend(["Solar", "Grid/Genset","Loads"]);
    axes_ener.grid(True)
    return fig_ener



def build_monthly_energies_figure2(month_kwh_df):
    #month_kwh_df = total_datalog_df.resample("1M").sum() / 60
    fig_ener2, axes_ener2 = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
    
    month_kwh_df[["Solar power (ALL) [kW] I17999 ALL", "XT-Pin a [kW] I3119 L1-1"]].plot.bar(
        stacked=True, 
        ax=axes_ener2, 
        use_index=False, 
        align="edge", 
        width=0.5,
        color=[SOLAR_COLOR, GENSET_COLOR],
    )



    month_kwh_df["XT-Pout a [kW] I3101 L1-1"].plot(
        kind="bar",
        align="center",
        width=0.5,
        ax=axes_ener2,
        use_index=False,
        color=LOAD_COLOR,
        alpha=0.5,
    )

    month_kwh_df["XT-Pout a [kW] I3101 L1-1"].plot(
        kind="line", 
        marker="o", 
        color="red", 
        ax=axes_ener2, 
        use_index=False
    )

    axes_ener2.set_ylabel("Energy [kWh]", fontsize=12)

    # replace labels with the month name:
    loc, label = plt.xticks()
    plt.xticks(loc, labels=list(month_kwh_df.index.month_name()))

    axes_ener2.set_title("Monthly Energies", fontsize=12, weight="bold")
    axes_ener2.legend(["Loads", "Solar", "Grid/Genset"]);
    axes_ener2.grid(True)
    return fig_ener2


#
#def build_monthly_energies_polar_figure(total_datalog_df,month_kwh_df):
#    #month_kwh_df = total_datalog_df.resample("1M").sum() / 60
#    fig_ener2, axes_ener2 = plt.subplots(nrows=1, ncols=1, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
#    
#    month_kwh_df[["Solar power (ALL) [kW] I17999 ALL", "XT-Pin a [kW] I3119 L1-1"]].plot.polar(
#        stacked=True, 
#        ax=axes_ener2, 
#        use_index=False, 
#        align="edge", 
#        width=0.5,
#        color=[SOLAR_COLOR, GENSET_COLOR],
#        legend=['Solar', 'Grid/Genset']
#    )
#
#
#
#    axes_ener2.set_ylabel("Energy [kWh]", fontsize=12)
#
#    # replace labels with the month name:
#    loc, label = plt.xticks()
#    plt.xticks(loc, labels=list(month_kwh_df.index.month_name()))
#
#    axes_ener2.set_title("Monthly Energies", fontsize=12, weight="bold")
#    axes_ener2.legend()
#    axes_ener2.grid(True)
#    return fig_ener2



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
    channels_number_ubat = [i for i, elem in enumerate(all_channels_labels) if "Ubat" in elem]


    ######################################
    # System Power
    ###########################
    # fig100=plt.figure(100)
    build_sys_power_figure(total_datalog_df,quarters_mean_df)
    build_power_histogram_figure(total_datalog_df,quarters_mean_df)


    ######################################
    # AC-details
    ###########################
    build_ac_power_figure(total_datalog_df, quarters_mean_df)


    ######################
    # Battery analysis
    ######
    build_total_battery_voltages_currents_figure(total_datalog_df)
    build_battery_voltage_histogram_figure(total_datalog_df, quarters_mean_df)
    build_battery_chargedischarge_histogram_figure(total_datalog_df, quarters_mean_df)
    
    build_voltage_versus_current_figure(total_datalog_df)
    build_mean_battery_voltage_figure(month_mean_df, day_mean_df)
    build_all_battery_voltages_figure(total_datalog_df, month_mean_df)



    #######
    ## Charge /discharge power
    ########
    #    channels_number_ubatbsp = [i for i, elem in enumerate(all_channels_labels) if "BSP-Ubat" in elem]
    #    channels_number_ibatbsp = [i for i, elem in enumerate(all_channels_labels) if "BSP-Ibat" in elem]
    #    battery_power = (
    #        total_datalog_df.values[:, channels_number_ubatbsp]
    #        * total_datalog_df.values[:, channels_number_ibatbsp]
    #        / 1000
    #    )

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
    build_solar_pv_voltage_figure(total_datalog_df)
    build_solar_energy_prod_figure(total_datalog_df)
    ##########
    # Time on the genset:
    ############
    build_genset_time_figure(total_datalog_df)
    # plt.show()

    # Analyse Batterie

    # axes4.bar(x=month_mean_df.index,
    #        y=total_datalog_df.columns[channels_number_ubat],
    #        color='r',
    #        ax=axes4_2)
    #
    # axes4.plot(x=total_datalog_df.index,
    #         y=total_datalog_df.columns[channels_number_ubat],
    #         grid=True,
    #         title='All Battery Voltages',
    #         ax=axes4)
    
    
    ############
    # Bar Monthly and Daily Energies:
    #################3
    
    # month_kwh_df['XT-Pout a [kW] I3101 L1-1']
    build_monthly_energies_figure(month_kwh_df)
    build_monthly_energies_figure2(month_kwh_df)
    build_daily_energies_figure(day_kwh_df)
    
    #build_monthly_energies_polar_figure(total_datalog_df,month_kwh_df)
    
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
