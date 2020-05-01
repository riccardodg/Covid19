import pandas as pd
import datetime

import matplotlib.pyplot as plt
import matplotlib._color_data as mcd
from datetime import timedelta, datetime

classname = "Plotter"
"""
This class plots different graphs for country.
Additional paramemeters can be suppied with **adds
"""


class Plotter(object):
    def __init__(self, plot_type, country, inc, extend_range, verbose, dict):
        routine = classname + ": " + "__init__"
        self.plot_type = plot_type
        self.country = country
        self.inc = inc
        self.extend_range = extend_range
        self.verbose = verbose
        self.dict = dict
        if self.verbose:
            print(f"\tRoutine {routine} instantiated with the following parameters")
            print("\t\tMandatory arguments:")
            print(f"\t\t\tplot-types {plot_type}")
            print(f"\t\t\tcountry {country}")
            print("\n\t\toptional arguments:")
            print(f"\t\t\tincrement {inc}")
            print(f"\t\t\textended range {extend_range}")
            print(f"\t\t\tverbose {verbose}")

            if len(dict) > 0:
                print(f"\t\t\tdict {dict}")
                for k, v in dict.items():
                    print(f"\t\t\t\tKey {k} with Value {v}")

    
    """
    return the colors to plot
    """
    def get_colors(self):
        overlap = {name for name in mcd.CSS4_COLORS
                    if "xkcd:" + name in mcd.XKCD_COLORS}
        colors=[]
        i =0
        for j, n in enumerate(sorted(overlap, reverse=True)):
            #print(j,n)
            weight = None
            cn = mcd.CSS4_COLORS[n]
            xkcd = mcd.XKCD_COLORS["xkcd:" + n].upper()
            if cn == xkcd:
                weight = 'bold'
            colors.append(cn)
        return colors
    
    
    def predict(self):
        return None

    def plot(self):
        return None

    """
    prepare data
    """

    def preparedata(self):
        routine = classname + ": " + "preparedata"
        total_rows = 0
        slices_num = 0
        if self.verbose:
            print(f"\n\tRoutine {routine}")
        # start from national
        national = self.dict["national"]
        if national:
            # prepare data for country, regions and excluded regions
            regs = self.dict["regs"]
            if (len(regs)>1):
                regs.append("aggregate for "+str(regs))
            regs.append(self.country)
            regs.append(self.country+" w/o "+str(self.dict["e_regs"]))
            
            
            for r in regs:
                # csv file
                f = self.dict[r]
                if self.verbose:
                    print(
                        f"\tRoutine {routine}. Preparing data for {r} from {f}. National is {national}"
                    )

                df = pd.read_csv(f)
                total_rows = df.count()[0]
                slices_num = total_rows // self.inc + 1
                if self.verbose:
                    print(
                        f"\tRoutine {routine}. Slicing data. Rows {total_rows} sliced into {slices_num} groups "
                    )
                for i in range(slices_num):
                    first=i * self.inc
                    if i==slices_num-1:
                        last=total_rows
                    else:
                        last=(i + 1) * self.inc
                    df_sliced = df[first : last]
                    #print(first, last)
                    self.plotsliceddata(r, df_sliced,first,last)
                # lastly plots all the data
                if self.verbose:
                    print(
                        f"\tRoutine {routine}. Plotting all data. Rows {total_rows}"
                    )
                first=0
                last=total_rows
                self.plotsliceddata(r, df,first,last)
                # print(df)
        else:
            print(False)

    def plotsliceddata(self, r, df, first,last):
        df_perc=pd.DataFrame()
        routine = classname + ": " + "plotsliceddata"
        standards = ["totale_positivi", "dimessi_guariti", "deceduti", "totale_casi",
        "ricoverati_con_sintomi" ,
        "terapia_intensiva",
        "totale_ospedalizzati",
        "isolamento_domiciliare"]
        incp = ["variazione_totale_positivi_perc", "nuovi_positivi_perc"]
        df_perc['data']=df['data']
        df_perc['variazione_totale_positivi_perc']=(df['variazione_totale_positivi']/(df['totale_positivi']-df['variazione_totale_positivi'])*100)
        df_perc['nuovi_positivi_perc']=(df['nuovi_positivi']/(df['totale_casi']-df['nuovi_positivi'])*100)
        #df_perc=df[['data','variazione_totale_positivi_perc','nuovi_positivi_perc']]
        #slice = self.inc
        #print(df_perc)
        # plot data as they are
        self.__plot__(df,r,standards,first,last-1)
        self.__plot_perc__(df_perc,r,incp,first,last-1)
        if self.verbose:
            print(
                f"\t\tRoutine {routine}. Plotting data for {r} with slice of {slice} and plot_type {self.plot_type}"
            )
        """
        if self.plot_type == "standard":
            # plot exponential, logistic, logistic4p fits.
            
            #first plots data as they are:
            self.__plot__(df,r,standards,first,last-1)
            
            start_date=df['data'][first]
            idoy=datetime.strptime(start_date,'%m/%d/%Y').timetuple().tm_yday
            print(start_date,idoy)
           
        """

    def __plot__(self,df, r,measures,first,last):
        colors=self.get_colors()
       
        f, ax = plt.subplots(1,1,figsize=(20,8))
        title=f"Data as they are for {r.title()} from {df['data'][first]} to {df['data'][last]}"
        ax.set_title(title)
        
        
        for m in measures:
            ax.set_ylabel('# of occurrences')
            ax.plot(df['data'], df[m],  alpha=0.7, linewidth=2, label=m)
            
        ax.set_xlabel('Dates')
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(True)
        plt.xticks(rotation='vertical')
        plt.show();
        
        
    def __plot_perc__(self,df, r,measures,first,last):
        colors=self.get_colors()
        len_m=len(measures)
        f, axes = plt.subplots(1,len_m,figsize=(20,8))
        #title=f"Increments % for {r.title()} from {df['data'][first]} to {df['data'][last]}"
        xlabels=[first,last]
         
         
        for m in measures:
            title=f"Increments % of {m} for {r.title()}\nfrom {df['data'][first]} to {df['data'][last]}"
            axes[measures.index(m)].set_title(title)
            axes[measures.index(m)].set_ylabel(f'% of increments for {m}')
            axes[measures.index(m)].plot(df['data'], df[m],  alpha=0.7, linewidth=2, label=m)
            axes[measures.index(m)].set_xlabel('Dates')
            axes[measures.index(m)].yaxis.set_tick_params(length=0)
            axes[measures.index(m)].xaxis.set_tick_params(length=0)
            #axes[measures.index(m)].set_xticks(rotation='vertical')
            axes[measures.index(m)].set_xticklabels([], rotation='vertical')
            axes[measures.index(m)].grid(b=True, which='major', c='w', lw=2, ls='-')
            legend = axes[measures.index(m)].legend()
            legend.get_frame().set_alpha(0.5)
             
        
        for spine in ('top', 'right', 'bottom', 'left'):
            for ax in axes:
                axes[measures.index(m)].spines[spine].set_visible(True)
        #plt.xticks(rotation='vertical')
        plt.show();
