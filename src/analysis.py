# import libraries
from os.path import join
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

# load configurations from config file
from helpers.config import configurations

#--------------------------------------------------
# definition of global variables

# globals for paths
drive = "H"
project_name = "predictive_modelling_agriculture"

# plot resolution
owndpi = 400

# output path
output_path = configurations(
    drive = drive,
    project_name = project_name
).get("output_path")

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
        output_path,
        "descriptive_stats.xlsx"
    )    
)

# for markdown rendering
html_table = descriptives.to_html()

# Save the markdown table to a file
with open(join(output_path, "descriptive_stats.html"), "w") as file:
    file.write(html_table)

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
            output_path,
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
            output_path,
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
        output_path,
        "concentrations_correlations.xlsx"
    )
)

# for markdown rendering
html_table = pairwise_correlations.to_html()

# Save the markdown table to a file
with open(join(output_path, "pairwise_correlations.html"), "w") as file:
    file.write(html_table)
    
#--------------------------------------------------
# split data

y = soils["crop"]
X = soils.drop(columns = "crop")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size = 0.3,
    random_state = 43,
    stratify = y
)

#--------------------------------------------------
# perform logistic regression for each feature
# to find the feature that predicts best the crop

# empty dictionary for storing the performance of each predictor
feature_performance = {}

# list of features
features = [feat for feat in list(soils.columns) if feat != "crop"]

# loop through all features and calculate the F1 score
for feature in features:
    # instantiate the model
    # NOTE: multinomial logistic regression because target variable (crop) has
    # more than two categories (and there is no given order between them)
    logreg = LogisticRegression(max_iter = 10000, multi_class = "multinomial")
    
    # fit the model and predict the target values
    logreg.fit(X_train[[feature]], y_train)
    y_pred = logreg.predict(X_test[[feature]])
    
    # calculate F1 score as performance metric
    score = f1_score(y_test, y_pred, average = "weighted")
    feature_performance[feature] = score
    
# extract the best predictive feature (i.e. the one with the highest F1 score)
best_predictive_feature = {key: value for key, value in [max(feature_performance.items(), key = lambda x: x[1])]}

# print result
print(f"The best predictive feature is {list(best_predictive_feature.keys())[0]} with a F1 score of {list(best_predictive_feature.values())[0].round(2)}!")

#--------------------------------------------------
# export the findings

# for exporting transform the dictionary into a data frame
feature_performance_df = pd.DataFrame.from_dict(feature_performance, orient = "index").reset_index()
feature_performance_df.rename(columns = {"index": "concentration", 0: "F1 score"}, inplace = True)

html_table = feature_performance_df.to_html(index = False)

# Save the markdown table to a file
with open(join(output_path, "scores_features.html"), "w") as file:
    file.write(html_table)