#!/usr/local/bin/python3

# sompe imports
import argparse
import sys

# from argparse import RawDescriptionHelpFormatter


# my own imports
import covars as vars


def argparser(routine):
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
    usage_text = example_text_0 + "\n\n"+example_text_1
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
        "-n",
        "--national",
        action="store_true",
        required=False,
        dest="national",
        help='If Italy is provided, you can add this flag to load national data instead global one. Default=False"',
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
        default=-1,
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
    return args()


def main():
    routine = sys.argv[0]
    argparser(routine)


main()
