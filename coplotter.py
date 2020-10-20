import pandas as pd
import datetime
import os

import covars as covars


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

    def preparedata(self, plot_type):
        routine = classname + ": " + "preparedata"
        total_rows = 0
        slices_num = 0
        slices=[]
        fs=[]
        ls=[]
        savefile=""
        if self.verbose:
            print(f"\n\tRoutine {routine} for {plot_type}")
        # start from national
        national = self.dict["national"]
        if national:
            # prepare data for country, regions and excluded regions
            regs = self.dict["regs"]
            if (len(regs)>1):
                regs.append("aggregate for "+str(regs))
            regs.append(self.country)
            if len(self.dict["e_regs"])>0:
                regs.append(self.country+"\nw/o\n"+str(self.dict["e_regs"]))
            
            
            for r in regs:
                # csv file
                f = self.dict[r]
                if self.verbose:
                    print(
                        f"\tRoutine {routine}. Preparing data for {r} from {f}. National is {national}"
                    )
                savefile=os.path.splitext(f)[0]
                df = pd.read_csv(f)
                total_rows = df.count()[0]
                # create slices only if inc not -1
                if (self.inc != -1):
                    
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
                        
                        slices.append(df_sliced)
                        fs.append(first)
                        ls.append(last)
                    # lastly plots all the data
                    if self.verbose:
                        print(
                        f"\tRoutine {routine}. Plotting { len(slices) } sliced data for {r}"
                        )
                    if (plot_type=='standard'):
                        for x in range(len(slices)):
                            self.plotsliceddata(r, slices[x],fs[x],ls[x],0,savefile)
                    if (plot_type=='perc'):
                        for x in range(len(slices)):
                            self.plotsliceddata(r, slices[x],fs[x],ls[x],1,savefile)
                    if (plot_type=='norm_tc'):
                        for x in range(len(slices)):
                            self.plotsliceddata(r, slices[x],fs[x],ls[x],2,savefile)
                    if (plot_type=='norm_tp'):
                        for x in range(len(slices)):
                            self.plotsliceddata(r, slices[x],fs[x],ls[x],3,savefile)
                    if (plot_type=='norm_tc_perc'):
                        for x in range(len(slices)):
                            self.plotsliceddata(r, slices[x],fs[x],ls[x],4,savefile)
                    if (plot_type=='norm_tp_perc'):
                        for x in range(len(slices)):
                            self.plotsliceddata(r, slices[x],fs[x],ls[x],5,savefile)
                else:
                    if self.verbose:
                        print(
                            f"\tRoutine {routine}. Plotting all data. Rows {total_rows}"
                        )
                    first=0
                    last=total_rows
                    if (plot_type=='standard'):
                        self.plotsliceddata(r, df,first,last,0,savefile)
                    if (plot_type=='perc'):
                        self.plotsliceddata(r, df,first,last,1,savefile)
                    if (plot_type=='norm_tc'):
                        self.plotsliceddata(r, df,first,last,2,savefile)
                    if (plot_type=='norm_tp'):
                        self.plotsliceddata(r, df,first,last,3,savefile)
                    if (plot_type=='norm_tc_perc'):
                        self.plotsliceddata(r, df,first,last,4,savefile)
                    if (plot_type=='norm_tp_perc'):
                        self.plotsliceddata(r, df,first,last,5,savefile)
            # print(df)
        else:
            print(False)

    def plotsliceddata(self, r, df, first,last, switch, savefile):
        df_perc=pd.DataFrame()
        df_norm_tc=pd.DataFrame()
        df_norm_tp=pd.DataFrame()
        df_norm_tc_perc=pd.DataFrame()
        df_norm_tp_perc=pd.DataFrame()
        routine = classname + ": " + "plotsliceddata"

        #measures for standard plot
        standards = ["totale_positivi", "dimessi_guariti", "deceduti", "totale_casi",
        "ricoverati_con_sintomi" ,
        "terapia_intensiva",
        "totale_ospedalizzati",
        "isolamento_domiciliare"]
        
        #measure for perc plot
        incp = ["variazione_totale_positivi_perc", "nuovi_positivi_perc","variazione_deceduti_perc"]
        #populate df
        df_perc['data']=df['data']
        df_perc['variazione_totale_positivi_perc']=(df['variazione_totale_positivi']/(df['totale_positivi']-df['variazione_totale_positivi'])*100)
        df_perc['nuovi_positivi_perc']=(df['nuovi_positivi']/(df['totale_casi']-df['nuovi_positivi'])*100)
        df_perc['variazione_deceduti_perc']=((df['deceduti']-df['deceduti'].shift())/(df['deceduti'].shift())*100)
        
        #measures for norm_tc plot
        norm_tc = ["totale_positivi_n", "dimessi_guariti_n", "deceduti_n", "totale_casi_n",
        "ricoverati_con_sintomi_n" ,
        "terapia_intensiva_n",
        "totale_ospedalizzati_n",
        "isolamento_domiciliare_n"]
        
        
        #populate df
        df_norm_tc['data']=df['data']
        df_norm_tc['totale_positivi_n']=(df['totale_positivi']/df['totale_casi'])*100
        df_norm_tc['dimessi_guariti_n']=(df['dimessi_guariti']/df['totale_casi'])*100
        df_norm_tc['deceduti_n']=(df['deceduti']/df['totale_casi'])*100
        df_norm_tc['totale_casi_n']=(df['totale_casi']/df['totale_casi'])*100
        df_norm_tc['ricoverati_con_sintomi_n']=(df['ricoverati_con_sintomi']/df['totale_casi'])*100
        df_norm_tc['terapia_intensiva_n']=(df['terapia_intensiva']/df['totale_casi'])*100
        df_norm_tc['totale_ospedalizzati_n']=(df['totale_ospedalizzati']/df['totale_casi'])*100
        df_norm_tc['isolamento_domiciliare_n']=(df['isolamento_domiciliare']/df['totale_casi'])*100
        
        
        #measures for norm_tp plot
        norm_tp = ["totale_positivi_n", "dimessi_guariti_n", "deceduti_n", "totale_casi_n",
        "ricoverati_con_sintomi_n" ,
        "terapia_intensiva_n",
        "totale_ospedalizzati_n",
        "isolamento_domiciliare_n"]
        
        
        #populate df
        df_norm_tp['data']=df['data']
        df_norm_tp['totale_positivi_n']=(df['totale_positivi']/df['totale_positivi'])*100
        df_norm_tp['dimessi_guariti_n']=(df['dimessi_guariti']/df['totale_positivi'])*100
        df_norm_tp['deceduti_n']=(df['deceduti']/df['totale_positivi'])*100
        df_norm_tp['totale_casi_n']=(df['totale_casi']/df['totale_positivi'])*100
        df_norm_tp['ricoverati_con_sintomi_n']=(df['ricoverati_con_sintomi']/df['totale_positivi'])*100
        df_norm_tp['terapia_intensiva_n']=(df['terapia_intensiva']/df['totale_positivi'])*100
        df_norm_tp['totale_ospedalizzati_n']=(df['totale_ospedalizzati']/df['totale_positivi'])*100
        df_norm_tp['isolamento_domiciliare_n']=(df['isolamento_domiciliare']/df['totale_positivi'])*100
        
        
        #measures for norm_tc_perc plot
        norm_tc_perc = ["totale_positivi_perc", "dimessi_guariti_perc", "deceduti_perc", "totale_casi_perc",
        "ricoverati_con_sintomi_perc" ,
        "terapia_intensiva_perc",
        "totale_ospedalizzati_perc",
        "isolamento_domiciliare_perc"]
        
        
        
        
        #populate df
        df_norm_tc_perc['data']=df['data']
        df_norm_tc_perc['totale_casi_shifted']=df['totale_casi']-df['totale_casi'].shift(periods=covars._PERIODS_)
        df_norm_tc_perc['totale_casi_inc']=df['totale_casi']-df['totale_casi'].shift()
        
        df_norm_tc_perc['totale_positivi_perc']=((df['totale_positivi']-df['totale_positivi'].shift())/df_norm_tc_perc['totale_casi_shifted'])*100
        df_norm_tc_perc['dimessi_guariti_perc']=((df['dimessi_guariti']-df['dimessi_guariti'].shift())/df_norm_tc_perc['totale_casi_shifted'])*100
        df_norm_tc_perc['deceduti_perc']=((df['deceduti']-df['deceduti'].shift())/df_norm_tc_perc['totale_casi_shifted'])*100
        df_norm_tc_perc['totale_casi_perc']=(df_norm_tc_perc['totale_casi_shifted']/df_norm_tc_perc['totale_casi_shifted'])*100
        df_norm_tc_perc['ricoverati_con_sintomi_perc']=((df['ricoverati_con_sintomi']-df['ricoverati_con_sintomi'].shift())/df_norm_tc_perc['totale_casi_shifted'])*100
        df_norm_tc_perc['terapia_intensiva_perc']=((df['terapia_intensiva']-df['terapia_intensiva'].shift())/df_norm_tc_perc['totale_casi_shifted'])*100
        df_norm_tc_perc['totale_ospedalizzati_perc']=((df['totale_ospedalizzati']-df['totale_ospedalizzati'].shift())/df_norm_tc_perc['totale_casi_shifted'])*100
        df_norm_tc_perc['isolamento_domiciliare_perc']=((df['isolamento_domiciliare']-df['isolamento_domiciliare'].shift())/df_norm_tc_perc['totale_casi_shifted'])*100
        
        #measures for norm_tp_perc plot
        norm_tp_perc = ["totale_positivi_perc", "dimessi_guariti_perc", "deceduti_perc",
        "ricoverati_con_sintomi_perc" ,
        "terapia_intensiva_perc",
        "totale_ospedalizzati_perc",
        "isolamento_domiciliare_perc"]
        
        
        
        
        #populate df
        df_norm_tp_perc['data']=df['data']
        df_norm_tp_perc['totale_positivi_shifted']=df['totale_positivi']-df['totale_positivi'].shift(periods=covars._PERIODS_)
        
        df_norm_tp_perc['totale_positivi_perc']=((df['totale_positivi']-df['totale_positivi'].shift())/df_norm_tp_perc['totale_positivi_shifted'])*100
        df_norm_tp_perc['dimessi_guariti_perc']=((df['dimessi_guariti']-df['dimessi_guariti'].shift())/df_norm_tp_perc['totale_positivi_shifted'])*100
        df_norm_tp_perc['deceduti_perc']=((df['deceduti']-df['deceduti'].shift())/df_norm_tp_perc['totale_positivi_shifted'])*100
        df_norm_tp_perc['totale_positivi_perc']=(df_norm_tp_perc['totale_positivi_shifted']/df_norm_tp_perc['totale_positivi_shifted'])*100
        df_norm_tp_perc['ricoverati_con_sintomi_perc']=((df['ricoverati_con_sintomi']-df['ricoverati_con_sintomi'].shift())/df_norm_tp_perc['totale_positivi_shifted'])*100
        df_norm_tp_perc['terapia_intensiva_perc']=((df['terapia_intensiva']-df['terapia_intensiva'].shift())/df_norm_tp_perc['totale_positivi_shifted'])*100
        df_norm_tp_perc['totale_ospedalizzati_perc']=((df['totale_ospedalizzati']-df['totale_ospedalizzati'].shift())/df_norm_tp_perc['totale_positivi_shifted'])*100
        df_norm_tp_perc['isolamento_domiciliare_perc']=((df['isolamento_domiciliare']-df['isolamento_domiciliare'].shift())/df_norm_tp_perc['totale_positivi_shifted'])*100
        
        #df_perc=df[['data','variazione_totale_positivi_perc','nuovi_positivi_perc']]
        #slice = self.inc
        #print(df_perc)
        # plot data as they are
        if switch==0:
            self.__plot__(df,r,standards,first,last-1,savefile)
        elif switch ==1:
            self.__plot_perc__(df_perc,r,incp,first,last-1,savefile)
        elif switch ==2:
            self.__plot_norm_tc__(df_norm_tc,r,norm_tc,first,last-1,savefile)
        elif switch ==3:
            self.__plot_norm_tp__(df_norm_tp,r,norm_tp,first,last-1,savefile)
        elif switch ==4:
            self.__plot_norm_tc_perc__(df_norm_tc_perc,r,norm_tc_perc,first,last-1,savefile)
        elif switch ==5:
            self.__plot_norm_tp_perc__(df_norm_tp_perc,r,norm_tp_perc,first,last-1,savefile)
            """
        """
        if self.verbose:
            print(
                f"\t\tRoutine {routine}. Plotting data for {r} with slice of {slice} and plot_type {self.plot_type}"
            )
        
        if self.plot_type == "standard":
            # plot exponential, logistic, logistic4p fits.
            
            #first plots data as they are:
            self.__plot__(df,r,standards,first,last-1)
            
            start_date=df['data'][first]
            idoy=datetime.strptime(start_date,'%m/%d/%Y').timetuple().tm_yday
            print(start_date,idoy)
           
        

    def __plot__(self,df, r,measures,first,last,savefile):
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
        if(self.dict['save']):
            figfile=self.dict['fig_dir']+"/"+savefile.replace("data_in","")+"_from_"+df['data'][first].replace("/","-")+"_to_"+df['data'][last].replace("/","-")
            #plt.save("{figfile}.png")
            plt.savefig(f"{figfile}_{self.plot_type}.png")
        else:
            plt.show();
        
   
    def __plot_norm_tc__(self,df, r,measures,first,last,savefile):
         colors=self.get_colors()
       
         f, ax = plt.subplots(1,1,figsize=(20,8))
         title=f"Data Normalized on totale_casi for {r.title()} from {df['data'][first]} to {df['data'][last]}"
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
         if(self.dict['save']):
             figfile=self.dict['fig_dir']+"/"+savefile.replace("data_in","")+"_from_"+df['data'][first].replace("/","-")+"_to_"+df['data'][last].replace("/","-")
            #plt.save("{figfile}.png")
             plt.savefig(f"{figfile}_{self.plot_type}.png")
         else:
             plt.show();
             
                  
             
    def __plot_norm_tc_perc__(self,df, r,measures,first,last,savefile):
         colors=self.get_colors()
                 
         f, ax = plt.subplots(1,1,figsize=(20,8))
         title=f"Data Normalized on totale_casi_shifted by {covars._PERIODS_} days for {r.title()} from {df['data'][first]} to {df['data'][last]}"
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
         if(self.dict['save']):
             figfile=self.dict['fig_dir']+"/"+savefile.replace("data_in","")+"_from_"+df['data'][first].replace("/","-")+"_to_"+df['data'][last].replace("/","-")
             #plt.save("{figfile}.png")
             plt.savefig(f"{figfile}_{self.plot_type}.png")
         else:
             plt.show();
                       
               
             
    def __plot_norm_tp_perc__(self,df, r,measures,first,last,savefile):
         colors=self.get_colors()
                     
         f, ax = plt.subplots(1,1,figsize=(20,8))
         title=f"Data Normalized on totale_positivi_shifted by {covars._PERIODS_} days for {r.title()} from {df['data'][first]} to {df['data'][last]}"
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
         if(self.dict['save']):
             figfile=self.dict['fig_dir']+"/"+savefile.replace("data_in","")+"_from_"+df['data'][first].replace("/","-")+"_to_"+df['data'][last].replace("/","-")
             #plt.save("{figfile}.png")
             plt.savefig(f"{figfile}_{self.plot_type}.png")
         else:
             plt.show();
                           
        
    def __plot_norm_tp__(self,df, r,measures,first,last,savefile):
        colors=self.get_colors()
            
        f, ax = plt.subplots(1,1,figsize=(20,8))
        title=f"Data Normalized on totale_positivi for {r.title()} from {df['data'][first]} to {df['data'][last]}"
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
        if(self.dict['save']):
            figfile=self.dict['fig_dir']+"/"+savefile.replace("data_in","")+"_from_"+df['data'][first].replace("/","-")+"_to_"+df['data'][last].replace("/","-")
                 #plt.save("{figfile}.png")
            plt.savefig(f"{figfile}_{self.plot_type}.png")
        else:
            plt.show();
                  
              
    def __plot_perc__(self,df, r,measures,first,last,savefile):
        colors=self.get_colors()
        len_m=len(measures)
        f, axes = plt.subplots(1,len_m,figsize=(20,8))
        #title=f"Increments % for {r.title()} from {df['data'][first]} to {df['data'][last]}"
        xlabels=[first,last]
         
         
        for m in measures:
            title=f"Incremental % of {m} for {r.title()}\nfrom {df['data'][first]} to {df['data'][last]}"
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
        if(self.dict['save']):
            figfile=self.dict['fig_dir']+"/"+savefile.replace("data_in","")+"_from_"+df['data'][first].replace("/","-")+"_to_"+df['data'][last].replace("/","-")
            #plt.save("{figfile}.png")
            plt.savefig(f"{figfile}_{self.plot_type}.png")
        else:
            plt.show();
