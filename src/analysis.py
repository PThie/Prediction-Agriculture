# import libraries
from os.path import join
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# load configurations from config file
from helpers.config import configurations

#--------------------------------------------------
# definition of global variables

# globals for paths
drive = "H"
project_name = "predictive_modelling_agriculture"

# plot resolution
owndpi = 400

#--------------------------------------------------
# Load data

soils = pd.read_csv(
    join(
        configurations(
            drive = drive,
            project_name = project_name
        ).get("data_path"),
        "soil_measure.csv"
    )
)

# Preview the data
soils.head()
soils.shape
soils["crop"].unique()

#--------------------------------------------------
# cleaning

# give columns more meaningful names
soils.rename(
    columns = {
        "N": "nitrogen_concentration",
        "P": "phosphorous_concentration",
        "K": "potassium_concentration"
    },
    inplace = True
)

#--------------------------------------------------
# descriptives

# descriptives on the soil characteristics
descriptives = soils.drop(columns = ["crop"]).describe().round(1)

descriptives.to_excel(
    join(
        configurations(
            drive = drive,
            project_name = project_name
        ).get("output_path"),
        "descriptive_stats.xlsx"
    )    
)

# calculate the number of missings
# NOTE: no missings in the features; no missing handling needed
print(soils.drop(columns = ["crop"]).isna().sum())

#--------------------------------------------------
# generate boxplots for concentrations

# reshape data for plotting
soils_long = soils.drop(columns = ["crop"]).melt(
    var_name = "stats",
    value_name = "concentration"
)

# set plotting style
sns.set(style = "whitegrid")

def plotting_boxplot_concentration(ph_plot: bool):
    """
    Generating boxplots for the concentration types

    Parameters
    ----------
    ph_plot : bool
        Indicates whether the plot should be generated for PH value (True) or
        the other concentration types (False).

    Returns
    -------
    None. Outputs figures.

    """
    if ph_plot is True:
        plot_data = soils_long[soils_long["stats"] == "ph"]
        ynames = ["PH value"]
        plot_name = "ph_boxplots"
    else:
        plot_data = soils_long[soils_long["stats"] != "ph"]
        ynames = ["Nitrogen", "Phosphorous", "Potassium"]
        plot_name = "concentration_boxplots"
    
    # create boxplot
    boxplot = sns.boxplot(
        x = "concentration",
        y = "stats",
        notch = True,
        data = plot_data
    )

    # define labels
    boxplot.set(
        xlabel = "Concentration",
        ylabel = ""
    )

    # set y-axis text
    boxplot.set_yticklabels(ynames)

    # export
    boxplot.get_figure().savefig(
        join(
            configurations(
                drive = drive,
                project_name = project_name
            ).get("output_path"),
            plot_name + ".png"
        ),
        dpi = owndpi,
        bbox_inches = "tight"
    )
    
    return(None)

for case in [True, False]:
    plotting_boxplot_concentration(ph_plot = case)

#--------------------------------------------------
# create scatter plot by crop

# function to generate plots
def plotting_scatter_concentration(
        concentration_col: str,
        dot_color: str,
        xname: str
    ):
    """
    Creating scatter plots for different soil concentration types

    Parameters
    ----------
    concentration_col : str
        Concentration to be plotted.
    
    dot_color : str
        Color for the dots
        
    xname : str
        Label for the x-axis

    Returns
    -------
    None. Outputs figures

    """
    # create a new figure
    plt.figure()
    
    # calculate the median concentration
    median_concentration = soils.groupby("crop")[concentration_col].median().reset_index()
    
    # base scatter plot
    scatters = sns.scatterplot(
        x = concentration_col,
        y = "crop",
        color = dot_color,
        alpha = 0.1,
        data = soils
    )

    # add mean concentration
    plt.scatter(
        x = median_concentration[concentration_col],
        y = median_concentration["crop"],
        color = "black",
        alpha = 0.5,
        label = "Median"    
    )

    plt.legend()

    # define labels
    scatters.set(
        xlabel = xname,
        ylabel = "Crop"
    )

    # capitalize the y-axis text
    current_labels = scatters.get_yticklabels()
    new_labels = [label.get_text().capitalize() for label in current_labels]
    scatters.set_yticklabels(new_labels)

    # export figure
    scatters.get_figure().savefig(
        join(
            configurations(
                drive = drive,
                project_name = project_name
            ).get("output_path"),
            "scatters_" + concentration_col + ".png"
        ),
        dpi = owndpi,
        bbox_inches = "tight"
    )
    
    # Close the current figure
    plt.close()
    
    return(None)
    
plotting_scatter_concentration(
    concentration_col = "nitrogen_concentration",
    dot_color = "blue",
    xname = "Nitrogen Concentration"
)

plotting_scatter_concentration(
    concentration_col = "phosphorous_concentration",
    dot_color = "red",
    xname = "Phosphorous Concentration"
)

plotting_scatter_concentration(
    concentration_col = "potassium_concentration",
    dot_color = "green",
    xname = "Potassium Concentration"
)

plotting_scatter_concentration(
    concentration_col = "ph",
    dot_color = "orange",
    xname = "PH value"
)

#--------------------------------------------------
# pairwise correlation between the different concentrations

pairwise_correlations = soils.drop(columns = "crop").corr("pearson").round(2)

pairwise_correlations.to_excel(
    join(
        configurations(
            drive = drive,
            project_name = project_name
        ).get("output_path"),
        "concentrations_correlations.xlsx"
    )
)