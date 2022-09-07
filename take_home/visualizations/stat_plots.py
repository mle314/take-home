"""
Useful plot functions for statistical analysis.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def cross_tab_prop_plot(df, col1, col2):
    """Displays a pandas crosstab object as a proportion graph.

    :param df: A pandas dataframe
    :param col1: Values to group by in the rows
    :param col2: Values to group by in the columns
    """
    cross_tab_prop = pd.crosstab(index=df[col1], columns=df[col2], normalize="index")

    cross_tab_prop.plot(
        kind="barh",
        stacked=True,
        color=["#1f77b4", "#ff7f0e"],
        figsize=(10, 6),
        edgecolor="black",
        alpha=0.8,
    )

    plt.legend(loc="lower left", ncol=2)
    plt.ylabel(f"{col1}")
    plt.xlabel("Proportion")

    for n, x in enumerate([*cross_tab_prop.index.values]):
        for (proportion, count, y_loc) in zip(
            cross_tab_prop.loc[x], cross_tab_prop.loc[x], cross_tab_prop.loc[x].cumsum()
        ):
            plt.text(
                x=(y_loc - proportion) + (proportion / 2),
                y=n - 0.2,
                s=f"{np.round(proportion * 100, 1)}%",
                color="black",
                fontsize=11,
                fontweight="bold",
            )

    plt.show()
