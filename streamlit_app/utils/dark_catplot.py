from dataclasses import dataclass
from typing import List

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


@dataclass
class DarkCatplotTheme:
    fig_facecolor: str = "#000000"
    ax_facecolor: str = "#000000"
    grid_color: str = "#444444"
    grid_linewidth: float = 1
    text_color: str = "white"
    palette: str = "Blues"

    def salary_catplot(
        self,
        df: pd.DataFrame,
        order: List[str],          # 👈 list[str] instead of Sequence[str]
        height: float,
        top_n: int,
        x_col: str = "average_salary",
        y_col: str = "primary_category",
#        title: str = "Salary Distribution by Category",
    ):
        sns.set_theme(style="whitegrid")

        # ensure we have a proper Index for reindex()
        order_index = pd.Index(order)

        g = sns.catplot(
            data=df,
            kind="box",
            y=y_col,
            x=x_col,
            order=order,          # seaborn is fine with list[str]
            height=height,
            aspect=2.5,
            palette=self.palette,
            fliersize=2,
            linewidth=0.5,
            boxprops=dict(edgecolor=self.text_color, linewidth=0.1),
            medianprops=dict(color="#000000", linewidth=1.0),
            whiskerprops=dict(color=self.text_color, linewidth=0.4),
            capprops=dict(color=self.text_color, linewidth=0.4),
            flierprops=dict(
                marker=".",
                markerfacecolor="#888888",
                markeredgecolor="#888888",
                markersize=2,
                alpha=0.4,
            ),
        )

        ax = g.ax
        fig = g.fig

        # backgrounds
        ax.set_facecolor(self.ax_facecolor)
        fig.patch.set_facecolor(self.fig_facecolor)

        # grid (thin, subtle)
        ax.grid(True, axis="x", color=self.grid_color, linewidth=self.grid_linewidth)
        ax.grid(False, axis="y")

        # remove outer borders
        for spine in ax.spines.values():
            spine.set_visible(False)

        # medians as white dots – use numpy array to keep type checker happy
        medians = (
            df.groupby(y_col)[x_col]
            .median()
            .reindex(order_index)
            .to_numpy(dtype="float64")
        )
        y_pos = np.arange(len(medians), dtype="float64")

        ax.scatter(medians, y_pos, color=self.text_color, s=14, zorder=3)

        # labels / ticks
        ax.set_xlabel("Average Salary (SGD)", fontsize=13, color=self.text_color)
        ax.set_ylabel("")
        ax.tick_params(axis="y", labelsize=11, colors=self.text_color)
        ax.tick_params(axis="x", labelsize=11, colors=self.text_color)

        legend = ax.get_legend()
        if legend is not None:
            legend.remove()
    
        fig.tight_layout()
        return fig, ax
