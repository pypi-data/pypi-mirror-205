"""
Infer the DFE from the SFS using discretized DFE.
"""

__author__ = "Janek Sendrowski"
__contact__ = "sendrowski.janek@gmail.com"
__date__ = "2023-02-26"

import functools
import logging
from typing import Callable, List, Literal, Dict

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import colors
from matplotlib.colors import LogNorm
from matplotlib.container import BarContainer
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
from tqdm import tqdm

from . import Parametrization
from .bootstrap import Bootstrap
from .spectrum import Spectrum

# get logger
logger = logging.getLogger('fastdfe')


class Visualization:
    """
    Visualization class.
    """

    # configure color map
    # plt.rcParams['axes.prop_cycle'] = cycler('color', plt.get_cmap('Set2').colors)

    @classmethod
    def change_default_figsize(cls, factor: float | np.ndarray):
        """
        Scale default figure size.

        :return: Factor to scale default figure size by
        """
        plt.rcParams["figure.figsize"] = list(factor * np.array(plt.rcParams["figure.figsize"]))

    @staticmethod
    def clear_show_save(func: Callable) -> Callable:
        """
        Decorator for clearing current figure in the beginning
        and showing or saving produced plot subsequently.

        :param func: Function to decorate
        :return: Wrapper function
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> plt.axis:
            """
            Wrapper function.

            :param args: Positional arguments
            :param kwargs: Keyword arguments
            :return: Axis
            """
            # clear current figure
            plt.clf()

            # execute function
            func(*args, **kwargs)

            # show or save
            # show by default here
            return Visualization.show_and_save(
                file=kwargs['file'] if 'file' in kwargs else None,
                show=kwargs['show'] if 'show' in kwargs else True
            )

        return wrapper

    @staticmethod
    def show_and_save(file: str = None, show=True) -> plt.axis:
        """
        Show and save plot.

        :param file: File path to save plot to
        :param show: Whether to show plot
        :return: Axis

        """
        # save figure if file path given
        if file is not None:
            plt.savefig(file, dpi=200, bbox_inches='tight', pad_inches=0.1)

        # show figure if specified and if not in interactive mode
        if show and not plt.isinteractive():
            plt.show()

        # return axis
        return plt.gca()

    @staticmethod
    def interval_to_string(left: float, right: float) -> str:
        """
        Get string representation for given interval.

        :param left: Right interval boundary
        :param right: Left interval boundary
        :return: String representation of interval

        """
        # left interval is closed by default
        bracket_left = '[' if left != -np.inf else '('
        bracket_right = ')'

        def format_number(n: float) -> str:
            """
            Format number, allowing for np.inf.

            :param n: Number to format
            :return: Formatted number
            """
            if np.abs(n) != np.inf:
                return '{:0.0f}'.format(n)

            return str(np.inf)

        return bracket_left + format_number(left) + ', ' + format_number(right) + bracket_right

    @staticmethod
    @clear_show_save
    def plot_discretized(
            values: list | np.ndarray,
            errors: list | np.ndarray = None,
            labels: list | np.ndarray = None,
            file: str = None,
            show: bool = True,
            intervals: np.ndarray = np.array([-np.inf, -100, -10, -1, 0, 1, np.inf]),
            title: str = 'discretized DFE',
            interval_labels: List[str] = None

    ) -> plt.axis:
        """
        Plot discretized DFEs using a bar plot.

        :param interval_labels: Labels for the intervals
        :param labels: Labels for the DFEs
        :param title: Title of the plot
        :param values: Array of values of size ``intervals.shape[0] - 1``
        :param errors: Array of errors of size ``intervals.shape[0] - 1``
        :param file: File path to save plot to
        :param show: Whether to show plot
        :param intervals: Array of interval boundaries yielding ``intervals.shape[0] - 1`` bars.
        :return: Axis
        """
        # number of intervals
        n_intervals = len(intervals) - 1
        n_dfes = len(values)

        width_total = 0.9
        width = width_total / n_dfes

        for i in range(n_dfes):
            x = np.arange(n_intervals) + i * width

            # plot discretized DFE
            bars = plt.bar(
                x=x,
                height=values[i],
                width=width,
                yerr=errors[i],
                error_kw=dict(
                    capsize=width * 7
                ),
                label=labels[i] if labels is not None else None,
                linewidth=0,
                hatch=Visualization.get_hatch(i, labels),
                color=Visualization.get_color(labels[i], labels) if labels is not None else None
            )

            Visualization.darken_edge_colors(bars)

        ax = plt.gca()
        ax.set(xlabel='S', ylabel='fraction')

        # determine x-labels
        if interval_labels is None:
            xlabels = [Visualization.interval_to_string(intervals[i - 1], intervals[i]) for
                       i in range(1, n_intervals + 1)]
        else:
            xlabels = interval_labels

        # customize x-ticks
        x = np.arange(n_intervals)
        ax.set_xticks([i + (width_total - width) / 2 for i in x], x)
        ax.set_xticklabels(xlabels)

        # set title
        ax.set_title(title)

        # show legend if labels were given
        if labels is not None:
            plt.legend(prop=dict(size=8))

        # remove x-margins
        ax.autoscale(tight=True, axis='x')

    @staticmethod
    @clear_show_save
    def plot_continuous(
            bins: np.ndarray,
            values: list | np.ndarray,
            errors: list | np.ndarray = None,
            labels: list | np.ndarray = None,
            file: str = None,
            show: bool = True,
            title: str = 'continuous DFE',
            scale: Literal['log', 'linear'] = 'lin',
            ylim: float = 1e-2,
            scale_density: bool = False,
            **kwargs
    ) -> plt.axis:
        """
        Plot DFEs using a line plot.
        By default, the PDF is plotted as is. Due to the logarithmic scale on
        the x-axis, we may get a wrong intuition on how the mass is distributed,
        however. To get a better intuition, we can optionally scale the density
        by the x-axis interval size using ``scale_density = True``. This has the
        disadvantage that the density now changes for x, so that even a constant
        density will look warped.

        :param ylim: y-axis limit
        :param scale: Scale of y-axis
        :param bins: Array of bin boundaries
        :param title: Title of the plot
        :param labels: Labels for the DFEs
        :param errors: Array of errors
        :param values: Array of values
        :param file: File path to save plot to
        :param show: Whether to show plot
        :param scale_density: Whether to scale the density by the bin size
        :return: Axis
        """
        from fastdfe.discretization import get_midpoints_and_spacing

        n_bins = len(bins) - 1
        n_dfes = len(values)

        # get interval sizes
        _, interval_sizes = get_midpoints_and_spacing(bins)

        fig, ax = plt.subplots()

        for i in range(n_dfes):
            x = np.arange(n_bins)

            # plot DFE
            ax.plot(x,
                    values[i] if scale_density else values[i] / interval_sizes,
                    label=labels[i] if labels is not None else None)

            # plot error bars
            if errors is not None and errors[i] is not None:
                ax.fill_between(
                    x=x,
                    y1=(values[i] - errors[i][0]) if scale_density else (values[i] - errors[i][0]) / interval_sizes,
                    y2=(values[i] + errors[i][1]) if scale_density else (values[i] + errors[i][1]) / interval_sizes,
                    alpha=0.2
                )

        # customize x-ticks
        Visualization.adjust_ticks_show_s(bins)

        # use log scale if specified
        if scale == 'log':
            ax.set_yscale('log')
            ax.set_ylim(bottom=ylim)

        # show legend if labels were given
        if labels is not None:
            plt.legend(prop=dict(size=8))

        # remove x-margins
        ax.set_xmargin(0)

        ax.set_title(title)

    @staticmethod
    def adjust_ticks_show_s(s: np.ndarray):
        """
        Adjust x-ticks to show bin values.

        :return: Array of selection coefficients
        """

        n_bins = len(s) - 1
        ax = plt.gca()

        ticks = ax.get_xticks()
        ticks_new = ["{:.0e}".format(s[int(l)]) if 0 <= int(l) < n_bins else None for l in ticks]

        ax.set_xticks(ticks)
        ax.set_xticklabels(ticks_new)

    @staticmethod
    @clear_show_save
    def plot_sfs_comparison(
            spectra: List[Spectrum] | np.ndarray,
            labels: List[str] = [],
            file: str = None,
            show: bool = True,
            title: str = 'SFS comparison',
            use_subplots: bool = False,
            show_monomorphic: bool = False,
    ) -> plt.axis:
        """
        Plot SFS comparison.

        :param use_subplots: Whether to use subplots
        :param show_monomorphic: Whether to show monomorphic counts
        :param title: Title of the plot
        :param labels: Labels for the SFSs
        :param spectra: List of spectrum objects in the same order as the labels or a 2D array
        :param file: File path to save plot to
        :param show: Whether to show plot
        :return: Axis
        """
        # plot modelled vs observed non-neutral SFS
        Visualization.plot_spectra(
            spectra=spectra,
            labels=labels,
            use_subplots=use_subplots,
            show_monomorphic=show_monomorphic
        )

        # set title
        plt.title(title)

    @staticmethod
    @clear_show_save
    def plot_inferred_parameters(
            params: List[dict],
            bootstraps: List[pd.DataFrame],
            file: str = None,
            show: bool = True,
            confidence_intervals: bool = True,
            bootstrap_type: Literal['percentile', 'bca'] = 'percentile',
            ci_level: float = 0.05,
            title: str = 'parameter estimates',
            scale: Literal['lin', 'log'] = 'log',
            labels: List[str] = None,
            **kwargs
    ) -> plt.axis:
        """
        Visualize the inferred parameters and their confidence intervals.
        using a bar plot.

        :param labels: Labels for the parameters
        :param scale: Whether to use a linear or log scale
        :param title: Title of the plot
        :param ci_level: Confidence level
        :param bootstrap_type: Type of bootstrap to use
        :param confidence_intervals: Whether to show confidence intervals
        :param params: List of parameter dictionaries in the same order as the labels
        :param bootstraps: List of dataframes containing bootstrapped parameter values in the same order as the labels
        :param file: File path to save plot to
        :param show: Whether to show plot
        :return: Axis
        """
        # get current axes
        fig, ax = plt.subplots()

        n_types = len(params)

        width_total = 0.9
        width = width_total / n_types

        # get keys of first element which we use to order the rest
        keys = sorted(list(params[0].keys()))
        n_values = len(keys)

        # iterate over types
        for i, param, bs in zip(range(n_types), params, bootstraps):

            values = list(param[k] for k in keys)

            # determine confidence interval if bootstraps were given
            if confidence_intervals and bs is not None:
                errors, _ = Bootstrap.get_errors(
                    values=np.abs(values),
                    bs=np.abs(bs[keys].to_numpy()),
                    bootstrap_type=bootstrap_type,
                    ci_level=ci_level
                )
            else:
                errors = None

            # whether to use the mean of all bootstraps instead of the original values
            use_means = confidence_intervals and bs is not None and bootstrap_type == 'percentile'

            x = np.arange(n_values) + i * width
            y = np.abs(bs[keys].mean().to_list() if use_means else values)

            def name_to_label(key: str) -> str:
                """
                Add parameter name to label.

                :param key: Parameter name
                :return: Label
                """
                # define new names for some parameters
                label_mapping = dict(
                    alpha='α',
                    eps='ε'
                )

                # map to new name
                label = label_mapping[key] if key in label_mapping else key

                # check parameter value and add minus sign if negative
                if param[key] >= 0:
                    return '$' + label + '$'

                return '$-' + key + '$'

            # append a minus sign to negative parameters values
            xlabels = np.array([name_to_label(key) for key in keys])

            bars = plt.bar(
                x=x,
                height=y,
                yerr=errors,
                error_kw=dict(
                    capsize=width * 7
                ),
                label=labels[i] if labels is not None else None,
                width=width,
                linewidth=0,
                hatch=Visualization.get_hatch(i, labels),
                color=Visualization.get_color(labels[i], labels) if labels is not None else None
            )

            Visualization.darken_edge_colors(bars)

            # customize x-ticks
            x = np.arange(n_values)
            ax.set_xticks([i + (width_total - width) / 2 for i in x], x)
            ax.set_xticklabels(xlabels)

        # show legend if specified
        if labels is not None:
            plt.legend(prop=dict(size=8), loc='upper right')

        # set title
        ax.set_title(title)

        # change to log-scale if specified
        if scale == 'log':
            ax.set_yscale('symlog', linthresh=1e-3)

        # remove x-margins
        ax.autoscale(tight=True, axis='x')

    @staticmethod
    def get_color(
            label: str,
            labels: List[str],
            get_group: Callable = lambda x: x.split('.')[-1]
    ) -> str:
        """
        Get color for specified label.

        :param label: Label to get color for
        :param labels: List of labels
        :param get_group: Function to get group from label
        :return: Color string
        """
        # determine unique groups
        groups = np.unique(np.array([get_group(l) for l in labels]))

        # determine group of current label
        group = get_group(label)

        # determine index of group
        i = np.where(groups == group)[0][0] if sum(groups == group) > 0 else 0

        # return color
        return f'C{i}'

    @staticmethod
    def get_hatch(i: int, labels: List[str] = None) -> str | None:
        """
        Get hatch style for specified index i.

        :param labels: List of labels
        :param i: Index
        :return: Hatch style
        """

        # determine whether hatch style should be used
        if labels is None or len(labels) < 1 or '.' not in labels[i]:
            return None

        # determine unique prefixes
        prefixes = set([label.split('.')[0] for label in labels if '.' in label])
        hatch_styles = ['/////', '\\\\\\\\\\', '***', 'ooo', 'xxx', '...']

        prefix = labels[i].split('.')[0]
        prefix_index = list(prefixes).index(prefix)

        return hatch_styles[prefix_index % len(hatch_styles)]

    @staticmethod
    def plot_spectra(
            spectra: List[Spectrum],
            labels: List[str] = [],
            log_scale: bool = False,
            use_subplots: bool = False,
            show_monomorphic: bool = False,
            ax=None,
            n_ticks=10
    ) -> plt.axis:
        """
        Plot the given 1D spectra.

        :param show_monomorphic: Whether to show monomorphic site counts
        :param n_ticks: Number of x-ticks to use
        :param ax: Axis to plot on
        :param use_subplots: Whether to use subplots
        :param spectra: List of spectra to plot
        :param labels: List of labels for each spectrum
        :param log_scale: Whether to use logarithmic y-scale
        :return: Axis
        """
        if use_subplots:
            n_plots = len(spectra)
            n_rows = int(np.ceil(np.sqrt(n_plots)))
            n_cols = int(np.ceil(np.sqrt(n_plots)))
            fig = plt.figure(figsize=(6.4 * n_cols ** (1 / 3), 4.8 * n_rows ** (1 / 3)))
            axes = fig.subplots(ncols=n_cols, nrows=n_rows, squeeze=False).flatten()

            # plot spectra individually
            for i in tqdm(range(n_plots)):
                Visualization.plot_spectra(
                    spectra=[spectra[i]],
                    labels=[labels[i]] if len(labels) else [],
                    ax=axes[i],
                    n_ticks=15 // min(2, n_cols),
                    log_scale=log_scale,
                    show_monomorphic=show_monomorphic
                )

            # make empty plots invisible
            [ax.set_visible(False) for ax in axes[n_plots:]]

            plt.tight_layout()

            return

        # determine sample size and width
        n = spectra[0].n
        width_total = 0.9
        width = width_total / len(spectra)

        x = np.arange(n + 1) if show_monomorphic else np.arange(1, n)

        # create axis if not specified
        if ax is None:
            _, ax = plt.subplots()

        # iterator over spectra and draw bars
        for i, sfs in enumerate(spectra):
            indices = x + i * width
            heights = sfs.to_list() if show_monomorphic else sfs.to_list()[1:-1]

            bars = ax.bar(
                x=indices,
                height=heights,
                width=width,
                label=labels[i] if len(labels) else None,
                linewidth=0,
                hatch=Visualization.get_hatch(i, labels)
            )

            Visualization.darken_edge_colors(bars)

        # adjust ticks
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        indices_ticks = x

        # filter ticks
        if n > n_ticks:
            indices_ticks = indices_ticks[indices_ticks % max(int(np.ceil(n / n_ticks)), 1) == 1]

        ax.set_xticks([i + (width_total - width) / 2 for i in indices_ticks], indices_ticks)

        ax.set_xlabel('allele count')

        # remove x-margins
        ax.autoscale(tight=True, axis='x')

        if log_scale:
            ax.set_yscale('log')

        if len(labels) == 1:
            ax.set_title(labels[0])
        elif len(labels) > 1:
            plt.legend(prop=dict(size=8))

        return ax

    @staticmethod
    def darken_edge_colors(bars: BarContainer):
        """
        Darken the edge color of the given bars.

        :param bars: Bars to darken
        """
        for bar in bars:
            color = bar.get_facecolor()
            edge_color = Visualization.darken_color(color, amount=0.75)
            bar.set_edgecolor(edge_color)

    @staticmethod
    def darken_color(color, amount=0.5) -> tuple:
        """
        Darken a color.

        :param color: Color to darken
        :param amount: Amount to darken
        :return: Darkened color as tuple
        """
        c = mcolors.to_rgba(color)

        return c[0] * amount, c[1] * amount, c[2] * amount, c[3]

    @staticmethod
    @clear_show_save
    def plot_pdf(
            model: Parametrization,
            params: dict,
            s: np.array,
            file: str = None,
            show: bool = True
    ) -> plt.axis:
        """
        Plot PDF of given parametrization.

        :param model: DFE parametrization
        :param params: Parameters to be used for parametrization
        :param s: Selection coefficients
        :param file: File to save plot to
        :param show: Whether to show plot
        :return: Axis
        """
        plt.plot(np.arange(len(s)), model.get_pdf(**params)(s))

        # customize x-ticks
        Visualization.adjust_ticks_show_s(s)

        # remove x-margins
        plt.margins(x=0)

    @staticmethod
    @clear_show_save
    def plot_cdf(
            model: Parametrization,
            params: dict,
            s: np.array,
            file: str = None,
            show: bool = True
    ) -> plt.axis:
        """
        Plot CDF of given parametrization.

        :param model: DFE parametrization
        :param params: Parameters to be used for parametrization
        :param s: Selection coefficients
        :param file: File to save plot to
        :param show: Whether to show plot
        :return: Axis
        """
        plt.plot(np.arange(len(s)), model.get_cdf(**params)(s))

        # customize x-ticks
        Visualization.adjust_ticks_show_s(s)

        # remove x-margins
        plt.margins(x=0)

    @staticmethod
    @clear_show_save
    def plot_likelihoods(
            likelihoods: list | np.ndarray,
            file: str, show: bool,
            title: str,
            scale: Literal['lin', 'log'] = 'lin'
    ) -> plt.axis:
        """
        A scatter plot of the likelihoods specified.

        :param scale: Scale of y-axis
        :param likelihoods: Likelihoods to plot
        :param file: File to save plot to
        :param show: Whether to show plot
        :param title: Title of plot
        :return: Axis
        """
        # plot
        plt.scatter(np.arange(len(likelihoods)), likelihoods)

        # get axis
        ax = plt.gca()

        # set title
        ax.set_title(title)

        # use integer ticks
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        # set labels
        ax.set_xlabel('iteration')
        ax.set_ylabel('lnl')

        if scale == 'log':
            ax.set_yscale('symlog')

    @staticmethod
    @clear_show_save
    def plot_buckets_sizes(
            n_intervals: int,
            bins: list | np.ndarray,
            sizes: list | np.ndarray,
            title: str,
            file: str,
            show: bool
    ) -> plt.axis:
        """
        A line plot of the bucket sizes.

        :param bins: Bins of the histogram
        :param n_intervals: Number of intervals
        :param sizes: Sizes of the buckets
        :param title: Title of plot
        :param file: File to save plot to
        :param show: Whether to show plot
        :return: Axis
        """
        # plot line
        plt.plot(np.arange(n_intervals), sizes)

        ax = plt.gca()

        # use log scale
        ax.set_yscale('log')
        ax.set_title(title)

        # customize x-ticks
        Visualization.adjust_ticks_show_s(bins)

        # remove x-margins
        ax.set_xmargin(0)

    @staticmethod
    @clear_show_save
    def plot_nested_likelihoods(
            P: np.ndarray,
            labels_x: list,
            labels_y: list,
            file: str = None,
            show: bool = True,
            cmap: str = None,
            title: str = None
    ) -> plt.axis:
        """
        Plot p-values of nested likelihoods.

        :param P: Matrix of p-values
        :param labels_x: Labels for x-axis
        :param labels_y: Labels for y-axis
        :param file: File to save plot to
        :param show: Whether to show plot
        :param cmap: Colormap to use
        :param title: Title of plot
        :return: Axis
        """

        def format_number(x: float | int | None) -> float | int | str:
            """
            Format number to be displayed.
            """
            if x == 0 or x is None:
                return 0

            if x < 0.0001:
                return "{:.1e}".format(x)

            return np.round(x, 4)

        # determine values to display
        annot = np.vectorize(lambda x: str(format_number(x)))(P)
        annot[np.equal(P, None)] = '-'

        # change to 1 to get a nicer color
        P[np.equal(P, None)] = 1

        fig, ax = plt.subplots()

        # make the cbar have the same height as the heatmap
        cbar_ax = make_axes_locatable(ax).new_horizontal(size="4%", pad=0.15)
        fig.add_axes(cbar_ax)

        # default color map
        if cmap is None:
            cmap = colors.LinearSegmentedColormap.from_list('_', plt.get_cmap('inferno')(np.linspace(0.3, 1, 100)))

        # plot heatmap
        sns.heatmap(
            P.astype(float),
            ax=ax,
            cbar_ax=cbar_ax,
            cmap=cmap,
            norm=LogNorm(
                vmin=1e-10,
                vmax=1
            ),
            annot=annot,
            fmt="",
            square=True,
            linewidths=0.5,
            linecolor='#cccccc',
            cbar_kws=dict(
                label='p-value'
            )
        )

        # adjust tick labels
        ax.set_xticklabels([l.replace('_', ' ') for l in labels_x], rotation=45)
        ax.set_yticklabels([l.replace('_', ' ') for l in labels_y], rotation=0)

        # set title
        ax.set_title(title)

    @staticmethod
    @clear_show_save
    def plot_covariates(
            covariates: Dict[str, 'Covariate'],
            params_marginal: Dict[str, Dict[str, float]],
            params_joint: Dict[str, Dict[str, float]],
            scale: Literal['lin', 'log'] = 'log',
            file: str = None,
            show: bool = True
    ) -> plt.axis:
        """
        Plot covariates.

        :param params_joint: Unpacked joint parameters indexed by type
        :param params_marginal: Marginal parameters indexed by type
        :param scale: Scale of y-axis
        :param covariates: Covariates to plot
        :param file: File to save plot to
        :param show: Whether to show plot
        :return: Axis
        """
        if len(covariates) == 0:
            return logger.info("There are no covariates to be plotted.")

        types = list(params_joint.keys())

        num_covariates = len(covariates)

        n_cols = min(3, num_covariates)
        n_rows = int(np.ceil(num_covariates / n_cols))
        fig, axs = plt.subplots(n_rows, n_cols, figsize=(6.4 * n_cols, 4.8 * n_rows), squeeze=False)

        n_intervals = len(types)
        width_total = 0.9
        width = width_total / 2

        for i, (p, cov) in enumerate(covariates.items()):
            ax = axs[i // n_cols, i % n_cols]

            x = np.arange(n_intervals)

            y1 = np.abs([params_marginal[t][cov.param] for t in types])
            y2 = np.abs([params_joint[t][cov.param] for t in types])

            # plot bars for marginal inference
            ax.bar(
                x=x,
                height=y1,
                width=width,
                label='marginal'
            )

            # plot bars for joint inference
            ax.bar(
                x=x + width,
                height=y2,
                width=width,
                label='joint'
            )

            # proper representation of parameter
            param_repr = f'${cov.param}' if params_marginal[types[0]][cov.param] >= 0 else f'$-{cov.param}'

            # set title
            ax.set_title(f"param={param_repr}, {p}={params_joint[types[0]][p]}")

            # adjust ticks
            ax.set_xticks(np.arange(len(types)) + width / 2)
            ax.set_xticklabels(types)

            # set legend
            ax.legend()

            # set y-scale
            if scale == 'log':
                ax.set_yscale('log')

        fig.tight_layout()
