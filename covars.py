import datetime

# VARIABLES AND VARIABLES AND VARIABLES AGAIN

# DATE
the_date = datetime.date.today().strftime("%Y-%m-%d")

# INPUT
# some variables for global graphs
_CONFIRMED_GLOBAL_CSV_ = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"  # total cases from global data

_RECOVERED_GLOBAL_CSV_ = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"  # recovered cases from global data

_DEATH_GLOBAL_CSV_ = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"  # death toll from global data

# some variables for national plots
_DATA_ITA_ = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"  # DPC github url for national data

_DATA_REG_ = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"  # DPC github url for regional data

# OUTPUT
# global files
_CONFIRMED_GLOBAL_FILE_NAME_ = (
    "confirmed_global_" + the_date + ".csv"
)  # global confirmed
_RECOVERED_GLOBAL_FILE_NAME_ = (
    "recovered_global_" + the_date + ".csv"
)  # global recovered
_DEATH_GLOBAL_FILE_NAME_ = "death_global_" + the_date + ".csv"  # global death

# global files by country
_CONFIRMED_GLOBAL_FILE_NAME_BASE = (
    "confirmed_global_"  # prefix for country confirmed data
)
_RECOVERED_GLOBAL_FILE_NAME_BASE = (
    "recovered_global_"  # prefix for country recovered data
)
_DEATH_GLOBAL_FILE_NAME_BASE = "death_global_"  # prefix for country death data

_GLOBAL_SUFFIX_ = "_" + the_date + ".csv"  # global suffix. The same for each file

# file names used when -n flag is provided
_REG_CSV_FILE_NAME_ = "dpc-covid19-ita-regioni_" + the_date + ".csv"  # file for regions
_NAZ_CSV_FILE_NAME_ = (
    "dpc-covid19-ita-andamento-nazionale_" + the_date + ".csv"
)  # file for italy

# REGIONAL
_REG_CSV_FILE_NAME_BASE_ = "dpc-covid19-ita-"  # prefix for regional data
_REG_CSV_FILE_NAME_BASE_SUFFIX_ = "_" + the_date + ".csv"  # suffix for regional data

_REG_CSV_FILE_NAME_AGGR_ = "dpc-covid19-ita-aggregates_"  # prefix for regional data
_REG_CSV_FILE_NAME_AGGR_SUFFIX_ = "_" + the_date + ".csv"  # suffix for regional data


_REG_CSV_FILE_ADD_NAME_BASE_ = (
    "dpc-covid19-ita-"  # prefix for regional incremented data
)
_REG_CSV_FILE_ADD_NAME_INC_SUFFIX_ = (
    "_" + the_date + "_incp.csv"
)  # suffix for regional incremented data


# NATIONAL
_NAZ_CSV_FILE_ADD_NAME_ = (
    "dpc-covid19-ita-andamento-nazionale_incp_" + the_date + ".csv"
)  # incremented national file
_NAZ_CSV_FILE_ADD_NAME_INC_SUFFIX_ = (
    "_" + the_date + "_incp.csv"
)  # suffix for national incremented data

_NAZ_CSV_FILE_NAME_EXCL_ = (
    "dpc-covid19-ita-andamento-nazionale_excluded_"  # prefix for regional data
)
_NAZ_CSV_FILE_NAME_EXCL_SUFFIX_ = "_" + the_date + ".csv"  # suffix for regional data

# folders
_FLD_IN_ = "data_in"  # where data are saved
_FLD_OUT_ = "data_out"  # where elaborated files are saved
_FLD_FIG_ = "figs"  # folder containing graphs
