#!/usr/bin/env python3
"""Plot symmetry function values."""

from typing import Optional, List, Dict, Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from .setup import GenericPlots


class RunnerStructureSymmetryFunctionValuesPlots(GenericPlots):
    """A plotting interface for symmetry function values of one structure."""

    def __init__(
        self,
        data: Dict[str, np.ndarray]
    ) -> None:
        """Initialize the class."""
        self.data = data

    # pylint: disable=too-many-locals
    def boxplot(
        self,
        axes: Optional[plt.Axes] = None,
        normalize: Optional[bool] = False
    ) -> plt.Axes:
        """Create a boxplot of the distribution of symmetry function values.

        This routine generates a statistical analysis of the different RuNNer
        symmetry functions in the form of a boxplot.

        Parameters
        ----------
        axes : plt.Axes
            A maplotlib.pyplot `Axes` instance to which the data will be added.
            If no axis is supplied, a new one is generated and returned instead.
        """
        # If no axis object was provided, use the last one or create a new one.
        if axes is None:
            axes = plt.gca()

        # Choose the right style for a bar plot.
        self.add_style('bar')

        legend_elements = []

        n_bars = len(self.data)
        bar_width = self.boxplot_style['widths']

        for idx_element, (element, sfvalues) in enumerate(self.data.items()):
            # Stack the arrays of each element and remove the first column
            # which contains the atomic index.
            sfdata = sfvalues[:, 1:]
            labels = np.arange(0, sfdata.shape[1], 1)

            # Normalize the values.
            if normalize is True:
                norm = sfdata.max()
                sfdata /= norm

            # Shift boxes to accomodate multiple elements.
            bar_offset = (idx_element - n_bars / 2) * bar_width + bar_width / 2
            barcenter = labels + bar_offset

            # Use a context manager to apply styles locally.
            with plt.style.context(self.styles):
                boxplot = axes.boxplot(sfdata, positions=barcenter,
                                       **self.boxplot_style)

            # Fill the boxes with colors.
            for patch in boxplot['boxes']:
                patch.set_facecolor(self.colors[idx_element])

            # Add a legend entry.
            legend_elements += [Patch(facecolor=self.colors[idx_element],
                                label=element)]

        with plt.style.context(self.styles):
            axes.set_xticks(labels)
            axes.set_xticklabels(labels)
            axes.set_xlabel('Symmetry Function ID')

            if normalize is True:
                axes.set_ylabel('Normalized Symmetry Function Values / a. u.')
            else:
                axes.set_ylabel('Symmetry Function Values / a. u.')

            axes.set_title('Atom-centered Symmetry Function Values')
            axes.legend(handles=legend_elements, loc='upper right')

        return axes


class RunnerSymmetryFunctionValuesPlots(GenericPlots):
    """A plotting interface for all symmetry function values of one dataset."""

    def __init__(
        self,
        data  # type: ignore
    ) -> None:
        """Initialize the class."""
        self.data = data

    # pylint: disable=too-many-locals
    def boxplot(
        self,
        axes: Optional[plt.Axes] = None,
        normalize: Optional[bool] = False
    ) -> plt.Axes:
        """Create a boxplot of the distribution of symmetry function values.

        This routine generates a statistical analysis of the different RuNNer
        symmetry functions in the form of a boxplot.

        Parameters
        ----------
        axes : plt.Axes
            A maplotlib.pyplot `Axes` instance to which the data will be added.
            If no axis is supplied, a new one is generated and returned instead.
        normalize : bool
            Whether all data should be normalized individually or not.
        """
        # If no axis object was provided, use the last one or create a new one.
        if axes is None:
            axes = plt.gca()

        # Choose the right style for a bar plot.
        self.add_style('bar')

        # Collect the symmetry function values of all structures in one dict
        # of lists of np arrays.
        allsfvalues: Dict[str, List[np.ndarray]] = {}
        for structure in self.data:
            for element, sfvalues in structure.data.items():
                if element not in allsfvalues:
                    allsfvalues[element] = []

                allsfvalues[element].append(sfvalues)

        n_bars = len(allsfvalues)
        bar_width = self.boxplot_style['widths']

        legend_elements = []
        for idx_element, (element, sfvalues) in enumerate(allsfvalues.items()):
            # Stack the arrays of each element and remove the first column
            # which contains the atomic index.
            sfdata = np.vstack(sfvalues)[:, 1:]
            labels = np.arange(0, sfdata.shape[1], 1)

            # Normalize the values.
            if normalize is True:
                norm = sfdata.max(axis=0)
                sfdata /= norm

            # Shift boxes to accomodate multiple elements.
            bar_offset = (idx_element - n_bars / 2) * bar_width + bar_width / 2
            barcenter = labels + bar_offset

            # Use a context manager to apply styles locally.
            with plt.style.context(self.styles):
                boxplot = axes.boxplot(sfdata, positions=barcenter,
                                       **self.boxplot_style)

            # Fill the boxes with colors.
            for patch in boxplot['boxes']:
                patch.set_facecolor(self.colors[idx_element])

            # Add a legend entry.
            legend_elements += [Patch(facecolor=self.colors[idx_element],
                                label=element)]

        with plt.style.context(self.styles):
            axes.set_xticks(labels)
            axes.set_xticklabels(labels)
            axes.set_xlabel('Symmetry Function ID')

            if normalize is True:
                axes.set_ylabel('Normalized Symmetry Function Values / a. u.')
            else:
                axes.set_ylabel('Symmetry Function Values / a. u.')

            axes.set_title('Atom-centered Symmetry Function Values')
            axes.legend(handles=legend_elements, loc='upper right')

        return axes

    def sklearn_dimensionality_reduction(
        self,
        method,
        labels: Optional[Dict[str, List[float]]] = None,
        axes: Optional[plt.Axes] = None,
        normalize: Optional[bool] = False,
    ) -> Tuple[plt.Figure, plt.Axes]:
        """Apply scikit-learn function to symmetry function values.

        This routines prepares the symmetry function values
        of all structures in the dataset for dimensionality reduction using
        any `method` implemented in scikit-learn that works with a two-
        dimensional numpy ndarray of floats. The analysis is done separately
        for all elements in the dataset.

        Parameters
        ----------
        method : Function
            The scikit-learn algorithm to be used.
        labels : Dict[List[float]]
            If given, a flat array of color labels or numbers that is used
            to color the scatter plots in the low-dimensional manifold.
        axes : plt.Axes
            A maplotlib.pyplot `Axes` instance to which the data will be added.
            The number of axes must equal the number of elements.
            If no axis is supplied, a new one is generated and returned instead.
        normalize : bool
            Whether all data should be normalized by element or not.
        """
        # Collect the symmetry function values of all structures in one dict
        # of lists of np arrays.
        elementdata: Dict[str, List[np.ndarray]] = {}
        for structure in self.data:
            for element, data in structure.by_atoms():

                if element not in elementdata:
                    elementdata[element] = []

                elementdata[element].append(data)

        # If no axes were provided, create new ones.
        if axes is None:
            _, axes = plt.subplots(1, len(elementdata))

        # Perform dim. red. for each element and generate a scatter plot.
        for idx, (element, data) in enumerate(elementdata.items()):

            print(f'Processing element {element}...')

            # First index is just the structure number.
            data = np.array(data)[:, 1:]

            if len(elementdata) == 1:
                axis = axes
            else:
                axis = axes[idx]

            # Shift every symmetry funciton to zero mean and unit variance.
            if normalize is True:
                mean = data.mean(axis=0)
                std_dev = data.std(axis=0)
                data = (data - mean) / std_dev

            # Perform dim. red.
            result = method.fit_transform(data)

            # Scatter the data in the low-dimensional manifold.
            # Use a context manager to apply styles locally.
            with plt.style.context(self.styles):
                vals = axis.scatter(
                    result[:, 0],
                    result[:, 1],
                    c=labels[element] if labels is not None else None
                )
                axis.set_title(f'Embedding for {element}')

                if labels is not None:
                    plt.colorbar(vals, ax=axis)

        return axes, result

    def pca(
        self,
        n_components: int = 3,
        labels: Optional[Dict[str, List[float]]] = None,
        axes: Optional[plt.Axes] = None,
        normalize: Optional[bool] = False,
        **kwargs
    ) -> plt.Axes:
        """Perform principle component analysis on the symmetry functions.

        See `_sklearn_dimensionality_reduction` for details.
        """
        method = PCA(
            n_components=n_components,
            **kwargs
        )

        return self.sklearn_dimensionality_reduction(
            method=method,
            labels=labels,
            axes=axes,
            normalize=normalize,
        )

    # pylint: disable=too-many-arguments
    def tsne(
        self,
        n_components: int = 2,
        perplexity: float = 20.0,
        labels: Optional[Dict[str, List[float]]] = None,
        axes: Optional[plt.Axes] = None,
        normalize: Optional[bool] = False,
        **kwargs
    ) -> plt.Axes:
        """Perform tSNE on the symmetry function values.

        Apply t-distributed stochastic neighbor embedding as
        presented by Laurentz von der Maaten to the symmetry function
        values.

        See `_sklearn_dimensionality_reduction` for details.
        """
        method = TSNE(
            n_components=n_components,
            perplexity=perplexity,
            **kwargs
        )

        return self.sklearn_dimensionality_reduction(
            method=method,
            labels=labels,
            axes=axes,
            normalize=normalize,
        )
