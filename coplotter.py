import pandas as pd

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
            print(
                f"\t\tRoutine {routine}. Getting CSV data from {url}"
            )
        df = pd.read_csv(url)
        return df
