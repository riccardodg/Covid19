#!/usr/local/bin/python3

# some imports
import argparse

# some variables for global graphs
confirmed_global = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

recovered_global = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

death_global = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

# some variables for national plots
data_ita = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"

data_reg = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"


def argparser():
    print("STOCA")
    parser = argparse.ArgumentParser(
        description="Manage covid data and plot some graphs. The same script can be used to manage global data as well as national (Italian)  and/or regional level. There two one mandatory arguments, plot_type and country.\nplot_type is SIR, SIRS, standard, predicted.\n\tSIR plots SIR graphs;\n\tSIRS plots SIRS graphs;\n\tstandard plots the behaviour of data as thet are collected;\n\tpredicted extracts data at given time points (usually the ones which correspond to lockdown) and plots data as they are frozen between intervals. Usually the time slot is 14 days\nIf country is Italy you can provide the -n optional flag to load national data instead that global one. With Italy you can add the -r optional flag to pass a list of regions and/or the -ne optional parameter to exclude a list of regions from national data."
    )
    parser.add_argument(
        "plot_type",
        action="store",
        # dest='plot_type',
        help="Select a Plot Type",
        metavar="PLOT_TYPE",
        type=str,
        choices=["standard", "predicted", "SIR", "SIRS", "norm_tc", "norm_tp"],
        default="",
    )
    parser.add_argument(
			"country",
			action="store",
			# dest='plot_type',
			help="Provide a country. If Italy is provided, do you want to provide -r and -ne parameyters as well",
			metavar="COUNTRY",
			type=str,
			default="",
	)
	"""
	parser.add_argument(
			 'plot',
			 action='store',
			 #dest='plot',
			 help='Plot different measures',
			 metavar='PLOT',
			 type=str,
			 choices=['ricoverati_con_sintomi','terapia_intensiva','totale_ospedalizzati','isolamento_domiciliare','totale_positivi','nuovi_positivi','dimessi_guariti','deceduti',
			 'totale_casi','tamponi','tamponi-totale_positivi','totale_casi-deceduti','totale_casi-dimessi_guariti',
			 'totale_casi-dimessi_guariti','totale_attualmente_positivi-dimessi_guariti','tamponi-totale_casi','positivi_incp',
			 'dimessi_guariti_incp','deceduti_incp','totale_casi_incp','tamponi_incp','tamponi_vs_totale_casi_incp','SIR','SIRS'],
			 default='')
	"""
	parser.add_argument(
			"-r",
			"--regions",
			required=False,
			dest="regions",
			help="List of regions, separated by comma: Toscana,Lombardia. Do not provide this parameter to manage ONLY national data",
			metavar="REGS",
			type=str,
			default=[],
		)

	parser.add_argument(
			"-i",
			"--inc",
			required=False,
			dest="inc",
			type=int,
			metavar="INC",
			help="The span days to plot graphs. If inc=10 is provided, the time span is grouped in 10 samples. Default -1 days which means no increment",
			default=-1,
		)

	parser.add_argument(
			"-s",
			"--samefigure",
			action="store_true",
			required=False,
			dest="samefigure",
			help="True to plot different figures for different regions in the same figure. Default=False",
			default=False,
		)

	parser.add_argument(
			"-c",
			"--check_vs_nation",
			action="store_true",
			required=False,
			dest="check_vs_nation",
			help='Plot the figures and adds the national graph. Default=False"',
			default=False,
		)

	parser.add_argument(
			"-v",
			"--verbose",
			action="store_true",
			required=False,
			dest="verbose",
			help='rint verbose information. Default=False"',
			default=False,
		)

	parser.add_argument(
			"-e",
			"--extend_range",
			required=False,
			dest="extend_range",
			help="Used only for SIR and SIRS plots. Days in the future. Defaults to 150",
			metavar="EXTEND_RANGE",
			type=int,
			default=150,
		)

	"""
	 
	args = parser.parse_args()
	self.plot_type=args.plot_type
	self.plot=args.plot
	self.inc=args.inc
	self.samefigure=args.samefigure
	self.check_vs_nation=args.check_vs_nation
	self.verbose=args.verbose
	self.extend_range=args.extend_range
	 
	if (args.regions):
		self.regs=args.regions.split(",")
	return
		(self.plot_type,self.plot,self.regs,self.inc,self.samefigure,self.check_vs_nation,self.verbose,self.extend_range)
		"""
	


    args = parser.parse_args()
    return args


def main():
    print("OK")
    x = argparser()
    print(x)


main()
