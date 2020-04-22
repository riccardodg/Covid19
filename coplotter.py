import pandas as pd
import datetime

classname = "Plotter"
"""
This class plots different graphs for country.
Additional paramemeters can be suppied with **adds
"""


class Plotter(object):
    def __init__(self, plot_type, country, inc, extend_range, verbose, **adds):
        routine = classname + ": " + "__init__"
        self.plot_type = plot_type
        self.country = country
        self.inc = inc
        self.extend_range = extend_range
        self.verbose = verbose
        self.adds = adds
        if self.verbose:
            print(f"\tRoutine {routine} instantiated with the following parameters")
            print("\t\tMandatory arguments:")
            print(f"\t\t\tplot-types {plot_type}")
            print(f"\t\t\tcountry {country}")
            print("\n\t\toptional arguments:")
            print(f"\t\t\tincrement {inc}")
            print(f"\t\t\textended range {extend_range}")
            print(f"\t\t\tverbose {verbose}")

            if len(adds) > 0:
                print(f"\t\t\tadds {adds}")
                for k, v in adds.items():
                    print(f"\t\t\t\tKey {k} with Value {v}")

            """
            print(f"\t\t\tnational {national}")
            print(f"\t\t\tregions {regs}")
            print(f"\t\t\texcluded regions {e_regs}")
            """

    """
    get data from url
    
    parameters
    url the url
    
    return the dataframe with the data
    """

    def get_original_data(self, url):
        routine = classname + ": " + "get_original_data"
        if self.verbose:
            print(f"\t\tRoutine {routine}. Getting CSV data from {url}")
        df = pd.read_csv(url)
        df["data"] = df.data.apply(
            lambda x: datetime.datetime.strptime(x[0:10], "%Y-%m-%d").strftime(
                "%m/%d/%Y"
            )
        )
        return df

    """
    get data from regional url
    
    parameters
    url the regional url
    r the region
    return the dataframe with the data for region r
    """

    def get_original_data_for_region(self, url, r):
        routine = classname + ": " + "get_original_data_for_region"
        if self.verbose:
            print(f"\t\tRoutine {routine}. Getting CSV data for {r} from {url}")
        df = pd.read_csv(url)
        df["data"] = df.data.apply(
            lambda x: datetime.datetime.strptime(x[0:10], "%Y-%m-%d").strftime(
                "%m/%d/%Y"
            )
        )

        df_r = df.loc[df["denominazione_regione"].str.lower() == r]
        # df_r=df.loc[df['denominazione_regione'].str.lower() == r]

        return df_r

    """
    get data from regional url
    
    parameters
    url the regional url
    regs list of regions
    return the dataframe with the aggregate data for regions in regs
    
    """

    def get_original_data_for_regional_aggregate(self, url, regs):
        routine = classname + ": " + "get_original_data_for_regional_aggregate"
        if self.verbose:
            print(
                f"\t\tRoutine {routine}. Getting CSV data for aggregating {regs} from {url}"
            )
        df = pd.read_csv(url)
        df["data"] = df.data.apply(
            lambda x: datetime.datetime.strptime(x[0:10], "%Y-%m-%d").strftime(
                "%m/%d/%Y"
            )
        )
        df_r = (
            df.loc[df["denominazione_regione"].str.lower().isin(regs)]
            .groupby(["data"])
            .sum()
        )
        # df_r=df.loc[df['denominazione_regione'].str.lower() == r]

        return df_r

    """
       get data from regional url
       
       parameters
       url the regional url
       regs list of regions to exclude
       return the dataframe with the aggregate data for regions which are not in regs
       
       """

    def get_original_data_for_national_excluded(self, url, regs):
        routine = classname + ": " + "get_original_data_for_national_excluded"
        if self.verbose:
            print(
                f"\t\tRoutine {routine}. Getting CSV data for excluding {regs} from {url}"
            )
        df = pd.read_csv(url)
        df["data"] = df.data.apply(
            lambda x: datetime.datetime.strptime(x[0:10], "%Y-%m-%d").strftime(
                "%m/%d/%Y"
            )
        )
        df_r = (
            df.loc[~df["denominazione_regione"].str.lower().isin(regs)]
            .groupby(["data"])
            .sum()
        )
        # df_r=df.loc[df['denominazione_regione'].str.lower() == r]

        return df_r
