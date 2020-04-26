#!/usr/local/bin/python3

# sompe imports
import argparse
import sys
from datetime import datetime
import os
import pandas as pd

# from argparse import RawDescriptionHelpFormatter


# my own imports
import covars as vars
import coplotter as coplotter
import codataframes as codf

"""
# mandatory input variables
plot_type = ""  # mandatory, the plot
country = ""  # mandatory the country
"""

"""
Parse the input parameters.
"""


def argparser(routine):
    # optional input list variables
    regs = []  # list of region
    e_regs = []  # list of excluded regions
    example_text_0 = """For complex strategy: usage example:

    python3 {} -p SIR -c US
    python3 {} -p SIR -c Italy -n -r Toscana, Piemonte
    python3 {} -p SIR -c Italy -n -ne Lombardia, Veneto""".format(
        routine, routine, routine
    )

    example_text_1 = """Attention:  if NO -n flag is provided, -r and -ne are ignored: usage example:

    python3 {} -p SIR -c US
    python3 {} -p SIR -c Italy  -r Toscana, Piemonte
    python3 {} -p SIR -c Italy  -ne Lombardia, Veneto""".format(
        routine, routine, routine
    )
    usage_text = example_text_0 + "\n\n" + example_text_1
    parser = argparse.ArgumentParser(
        prog=routine,
        description="Manage covid data and plot some graphs. The same script can be used to manage global data as well as national (Italian)  and/or regional level. There two one mandatory arguments, plot_type and country. plot_type is one in SIR, SIRS, standard, predicted.\n\tSIR plots SIR graphs;\n\tSIRS plots SIRS graphs;\n\tstandard plots the behaviour of data as thet are collected;\n\tpredicted extracts data at given time points (usually the ones which correspond to lockdown) and plots data as they are frozen between intervals. Usually the time slot is 14 days\nIf country is Italy you can provide the -n optional flag to load national data instead that global one. With Italy you can add the -r optional flag to pass a list of regions and/or the -ne optional parameter to exclude a list of regions from national data.",
        epilog=usage_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # mandatory arguments
    parser.add_argument(
        "plot_type",
        action="store",
        # dest='plot_type',
        help="Select a Plot Type",
        metavar="PLOT_TYPE",
        type=str,
        choices=["standard", "predicted", "SIR", "SIRS"],
        default="",
    )
    parser.add_argument(
        "country",
        action="store",
        # dest='plot_type',
        help="Provide a country. If Italy is provided, do you want to provide -r and -ne parameyters as well?",
        metavar="COUNTRY",
        type=str,
        default="",
    )

    # optional arguments
    parser.add_argument(
        "-n",
        "--national",
        action="store_true",
        required=False,
        dest="national",
        help='If Italy is provided, you can add this flag to load national data instead global one. Default=False"',
        default=False,
    )
    parser.add_argument(
        "-r",
        "--regions",
        required=False,
        dest="regions",
        help="List of regions, separated by comma: Toscana,Lombardia. Do not provide this parameter to manage ONLY national data. If -n flag is not provided, this parameter will be ignored",
        metavar="REGS",
        type=str,
        default=[],
    )

    parser.add_argument(
        "-ne",
        "--excluded_regions",
        required=False,
        dest="excluded_regions",
        help="List of regions, separated by comma that you want to filter out from national data: Toscana,Lombardia. Do not provide this parameter to manage ONLY FULL national data. If -n flag is not provided, this parameter will be ignored",
        metavar="EX_REGS",
        type=str,
        default=[],
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        required=False,
        dest="verbose",
        help='Print verbose information. Default=False"',
        default=False,
    )

    parser.add_argument(
        "-i",
        "--inc",
        required=False,
        dest="inc",
        type=int,
        metavar="INC",
        help="The span days to plot graphs. If inc=10 is provided, the time span is grouped in 10-days samples. Default -1 days which means no increment",
        default=7,
    )

    parser.add_argument(
        "-e",
        "--extend_range",
        required=False,
        dest="extend_range",
        help="Use to predict plots in the future, after the last analyzed day. Defaults to 150",
        metavar="EXTEND_RANGE",
        type=int,
        default=150,
    )

    args = parser.parse_args()
    # get the values

    plot_type = args.plot_type
    country = args.country
    national = args.national
    if args.regions:
        regs = [r.strip().lower() for r in args.regions.split(",")]
    if args.excluded_regions:
        e_regs = [r.strip().lower() for r in args.excluded_regions.split(",")]
    inc = args.inc
    extend_range = args.extend_range
    verbose = args.verbose

    return plot_type, country, national, regs, e_regs, inc, extend_range, verbose


"""
Get data from URLs. It acts according to the national flag. If -n is provided, national data
are collected. If -r and -ne are also provided, then extract regional data, aggregates and excluded data

Parameters:
codata the class
national either True or False
verbose True to print more information
"""


def get_data_according_to_national_flag_and_save_to_files(
    codata, national, country, verbose
):
    routine = "get_data_according_to_national_flag_and_save_to_files"
    print(f"\tRoutine {routine}")
    df = pd.DataFrame()
    myreg = ""
    myereg = ""
    dict = {}
    files = []
    if not national:
        dict["national"] = national
        # confirmed
        url = vars._CONFIRMED_GLOBAL_CSV_
        f = vars._FLD_IN_ + "/" + vars._CONFIRMED_GLOBAL_FILE_NAME_
        if verbose:
            print(
                f"\t\tRoutine {routine}. Getting CSV data from {url} and saving into {f}. Country is {country}"
            )

        df = codata.get_original_data(url)
        df.to_csv(f)
        files.append(f)

        # recovered
        url = vars._RECOVERED_GLOBAL_CSV_
        f = vars._FLD_IN_ + "/" + vars._RECOVERED_GLOBAL_FILE_NAME_
        if verbose:
            print(
                f"\t\tRoutine {routine}. Getting CSV data from {url} and saving into {f}"
            )

        df = codata.get_original_data(url)
        df.to_csv(f)
        files.append(f)

        # death
        url = vars._DEATH_GLOBAL_CSV_
        f = vars._FLD_IN_ + "/" + vars._DEATH_GLOBAL_FILE_NAME_
        if verbose:
            print(
                f"\t\tRoutine {routine}. Getting CSV data from {url} and saving into {f}"
            )

        df = codata.get_original_data(url)
        df.to_csv(f)
        files.append(f)
        dict[country] = files
    else:  # -n is provided
        dict = codata.adds
        url = vars._DATA_ITA_

        f = vars._FLD_IN_ + "/" + vars._NAZ_CSV_FILE_NAME_
        if verbose:
            print(
                f"\t\tRoutine {routine}. Getting CSV data from {url} and saving into {f}"
            )

        df = codata.get_original_data(url)
        df.to_csv(f)
        dict[country] = f
        regs = codata.adds["regs"]
        e_regs = codata.adds["e_regs"]
        if len(regs) > 0:
            if (len(regs)) == 1:
                myreg = "-reg"
            else:
                myreg = "-regs"

            url = vars._DATA_REG_
            f = vars._FLD_IN_ + "/" + vars._REG_CSV_FILE_NAME_
            if verbose:
                print(
                    f"\t\tRoutine {routine}. Getting CSV data from {url} and saving into {f}"
                )

            df = codata.get_original_data(url)
            df.to_csv(f)
            for r in regs:
                # extract data for regions
                f = (
                    vars._FLD_IN_
                    + "/"
                    + vars._REG_CSV_FILE_NAME_BASE_
                    + r
                    + vars._REG_CSV_FILE_NAME_BASE_SUFFIX_
                )
                if verbose:
                    print(
                        f"\t\tRoutine {routine}. Getting CSV data for {r} from {url} and saving into {f}"
                    )
                df = codata.get_original_data_for_region(url, r)
                df.to_csv(f)
                dict[r] = f
            # extract aggregate for all regions in regs

            f = (
                vars._FLD_IN_
                + "/"
                + vars._REG_CSV_FILE_NAME_AGGR_
                + str(len(regs))
                + myreg
                + vars._REG_CSV_FILE_NAME_AGGR_SUFFIX_
            )
            if verbose:
                print(
                    f"\t\tRoutine {routine}. Getting CSV data for {regs} from {url} and saving into {f}"
                )
            df = codata.get_original_data_for_regional_aggregate(url, regs)
            df.to_csv(f)

            dict["aggregates"] = f
        if len(e_regs) > 0:
            if (len(e_regs)) == 1:
                myereg = "-reg"
            else:
                myereg = "-regs"
            # extract national data w/o e_regs
            url = vars._DATA_REG_
            f = (
                vars._FLD_IN_
                + "/"
                + vars._NAZ_CSV_FILE_NAME_EXCL_
                + str(len(e_regs))
                + myereg
                + vars._NAZ_CSV_FILE_NAME_EXCL_SUFFIX_
            )
            if verbose:
                print(
                    f"\t\tRoutine {routine}. Getting CSV data for {e_regs} from {url} and saving into {f}"
                )
            df = codata.get_original_data_for_national_excluded(url, e_regs)
            df.to_csv(f)
            dict["excluded"] = f
    return dict


def main():

    routine = sys.argv[0]
    (
        plot_type,
        country,
        national,
        regs,
        e_regs,
        inc,
        extend_range,
        verbose,
    ) = argparser(routine)

    # adds dictionary for other parameters
    adds = {}

    # add a plot dict: key=reg value=df

    # if country is NOT Italy, then national is False
    if country != "Italy":
        national = False
    # reset regs and e_regs if national is False
    if not national:
        regs = []
        e_regs = []
    else:
        adds["national"] = national
        adds["regs"] = regs
        adds["e_regs"] = e_regs
    print("Print parameters")
    print("\tMandatory arguments:")
    print(f"\t\tplot-types {plot_type}")
    print(f"\t\tcountry {country}")
    print("\n\toptional arguments:")
    print(f"\t\tnational {national}")
    print(f"\t\tregions {regs}")
    print(f"\t\texcluded regions {e_regs}")
    print(f"\t\tincrement {inc}")
    print(f"\t\textended range {extend_range}")
    print(f"\t\tverbose {verbose}")

    start_date = datetime.now()

    date_ts = start_date.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    print(f"Starting {routine} at {date_ts}")
    if verbose:
        print(f"\tRoutine {routine}. Create folders")
    # create folders
    if not os.path.exists(vars._FLD_IN_):
        os.makedirs(vars._FLD_IN_)

    if not os.path.exists(vars._FLD_OUT_):
        os.makedirs(vars._FLD_OUT_)

    if not os.path.exists(vars._FLD_FIG_):
        os.makedirs(vars._FLD_FIG_)

    # step 1 initialize classes plotter and codataframes
    mydate = datetime.now()
    date_ts = mydate.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    print(f"Routine {routine}. Creating folders at {date_ts}")

    if not national:
        codata = codf.Codf(verbose)

    else:
        codata = codf.Codf(verbose, **adds)

    # step 2 get the data
    mydate = datetime.now()
    date_ts = mydate.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    print(f"Routine {routine}. Getting data  at {date_ts}")
    x = get_data_according_to_national_flag_and_save_to_files(
        codata, national, country, verbose
    )
    print(f"X is {x}")
    plotter = coplotter.Plotter(plot_type, country, inc, extend_range, verbose, x)
    plotter.preparedata()


main()
