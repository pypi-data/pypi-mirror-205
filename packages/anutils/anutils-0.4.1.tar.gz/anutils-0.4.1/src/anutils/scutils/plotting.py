import matplotlib as mpl
import matplotlib.pyplot as plt
import scanpy as sc
import numpy as np
import pandas as pd
import seaborn as sns


def init_fig_params():
    plt.rcParams['axes.unicode_minus'] = False
    plt.rc('font', family='Helvetica')
    plt.rcParams['pdf.fonttype'] = 42
    # sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
    # sc.logging.print_header()
    sc.set_figure_params(dpi=120, facecolor='w', frameon=True, figsize=(4, 4))
    # %config InlineBackend.figure_format='retina'
    # %matplotlib inline


def embeddings(adata,
               basis=None,
               *,
               group_adata_by=None,
               replicate_key=None,
               groups_order=None,
               add_bg=False,
               ncols=None,
               figsize=None,
               zoom=False,
               return_fig_axes=False,
               **embedding_kwargs):
    """plot embeddings of adata grouped by group_adata_by

    Parameters
    ----------
    group_adata_by : str or list of str
        column(s) in adata.obs. if a list, they will be concatenated with '::' as the group key
    replicate_key : str, optional
        a column in adata.obs, by default None. If not None, the number of replicates will be shown in the title
    groups_order : iterable, optional
        a ordered list of keys in `adata.obs[group_adata_by]`, by default None
    add_bg : bool, optional
        whether to add umap background (from other groups), by default False
    ncols : int, optional
        ncols, by default 3
    figsize : 2 length tuple, optional
        figsize, by default `(5 * ncols, 5 * nrows)`
    zoom : bool, optional
        whether to zoom each umap plot, by default False, which means the xlim and ylim will be the same for all plots
    return_fig_axes : bool, optional
        whether to return the fig and axes, by default False
    embedding_kwargs : dict
        kwargs for sc.pl.embedding. `adata` is required. if `basis` is not provided, `X_umap` will be used.

    Returns
    -------
    fig
        the fig object
    """
    if basis is None:
        basis = 'X_umap'

    assert group_adata_by is not None, 'argument `group_adata_by` is required'

    # reorder
    if isinstance(group_adata_by, str):
        pass
    else:  # iterable
        group_adata_by = '::'.join(group_adata_by)
        adata.obs[group_adata_by] = adata.obs[list(group_adata_by.split('::'))].apply(
            lambda x: '::'.join(x), axis=1)
    indices = adata.obs.groupby(group_adata_by).indices
    if groups_order is None:
        groups_order = indices.keys()
    indices = {k: indices[k] for k in groups_order}
    if ncols is None:
        ncols = min(4, len(indices))
    # plot
    N = adata.obs[group_adata_by].nunique()
    nrows = (N - 1) // ncols + 1
    if figsize is None:
        figsize = (5 * ncols, 5 * nrows)
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows, figsize=figsize)

    if 'color' in embedding_kwargs:
        if isinstance(embedding_kwargs['color'], str):
            embedding_kwargs['color'] = [embedding_kwargs['color']]
        # freeze the colors for categorical variables to make sure the colors are
        # the same for different plots. (scanpy will change the colors for categorical
        # variables if the number of categories changes when subseting the adata)
        # sc.pl.embedding(**embedding_kwargs, show=False)

    for i, (k, v) in enumerate(indices.items()):
        ad = adata[v, :]
        # scanpy changes the number of categories when subseting the adata, so we need
        # to reset the categories
        if 'color' in embedding_kwargs:
            for c in embedding_kwargs['color']:
                if c not in ad.obs.columns:
                    # might be a gene name
                    continue
                # if it is categorical
                if adata.obs[c].dtype.name == 'category':
                    ad.obs[c].cat.set_categories(adata.obs[c].cat.categories, inplace=True)

        title = k
        if replicate_key is not None:
            title += f' (n={ad.obs[replicate_key].nunique()})'
        kwargs = embedding_kwargs.copy()
        if add_bg:
            _ = sc.pl.embedding(
                adata,
                basis=basis,
                ax=axes.flatten()[i],
                show=False,
            )
        _ = sc.pl.embedding(
            ad,
            basis=basis,
            **kwargs,
            ax=axes.flatten()[i],
            show=False,
            title=title,
        )

    # remove empty axes
    while i < ncols * nrows - 1:
        i += 1
        axes.flatten()[i].axis('off')

    if not zoom:
        axes_used = axes.flatten()[:N]
        # adjust axes lims to make them equal
        xlims = np.array([ax.get_xlim() for ax in axes_used.flat])
        ylims = np.array([ax.get_ylim() for ax in axes_used.flat])
        xlims = np.array([xlims[:, 0].min(), xlims[:, 1].max()])
        ylims = np.array([ylims[:, 0].min(), ylims[:, 1].max()])
        for ax in axes_used.flat:
            ax.set_xlim(xlims)
            ax.set_ylim(ylims)

    # fig.tight_layout()
    return (fig, axes) if return_fig_axes else None


def change_bar_width(ax, new_value):
    for patch in ax.patches:
        current_width = patch.get_width()
        diff = current_width - new_value

        # we change the bar width
        patch.set_width(new_value)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)


def barplot(df,
            key='celltype',
            color=sns.color_palette("tab20"),
            width=0.6,
            figsize=(16, 6),
            save=False):
    fig = plt.figure(figsize=figsize)
    ax = sns.barplot(x=key, y='counts', data=df, color=color, saturation=1)
    plt.xlabel('donor', fontsize=22, labelpad=8)
    plt.ylabel('Cell Number', fontsize=22, labelpad=8)
    plt.xticks(rotation=45, fontsize=20, ha='right')
    plt.yticks([0, 5000, 10000, 15000], rotation=0, fontsize=20)
    plt.title('', fontsize=25, ha='center')

    change_bar_width(ax, width)

    if save:
        plt.savefig(save, dpi=100, format='pdf', bbox_inches='tight')


def dotplot(adata, groupby, var_names, inplace=False, **dotplot_kwargs):
    if not inplace:
        adata = adata.copy()
    if 'base' not in adata.uns['log1p']:
        adata.uns['log1p']['base'] = np.e
    adata.obs[groupby] = adata.obs[groupby].astype('category')
    sc.tl.dendrogram(adata, groupby=groupby, var_names=var_names)
    sc.pl.dotplot(adata,
                  groupby=groupby,
                  var_names=var_names,
                  dendrogram=True,
                  **dotplot_kwargs)


def composition_plot(data,
                     x,
                     hue,
                     x_subset=None,
                     hue_subset=None,
                     hue_colors=None,
                     bar_width=None,
                     figsize=None,
                     legend_fontsize=None,
                     label_fontsize=None,
                     label_pad=None,
                     label_rotation=None):
    """plot the composition of a categorical variable `hue` in different groups of `x`

    Parameters
    ----------
    data : Union[DataFrame, AnnData]
        data to plot
    x : str
        groupby variable
    hue : str
        categorical variable to plot
    x_subset : List[str], optional
        x subset, by default None
    hue_subset : List[str], optional
        hue subset, by default None
    hue_colors : Iterable, optional
        hue colors, by default None

    Returns
    -------
    matplotlib.axes.Axes
        axes

    Raises
    ------
    ValueError
        data must be a pandas.DataFrame or an anndata.AnnData
    """
    if type(data).__name__ == 'DataFrame':
        df = data
    elif type(data).__name__ == 'AnnData':
        df = data.obs
    else:
        raise ValueError('data must be a pandas.DataFrame or an anndata.AnnData')
    tmp = df.groupby(x)[hue].value_counts().unstack()
    if x_subset is None:
        x_subset = tmp.index
    if hue_subset is None:
        hue_subset = tmp.columns
    if bar_width is None:
        bar_width = .6
    if figsize is None:
        figsize = (16, 8)
    if legend_fontsize is None:
        legend_fontsize = 20
    if label_rotation is None:
        label_rotation = 45
    if label_fontsize is None:
        label_fontsize = 22
    if label_pad is None:
        label_pad = 8
    tmp = tmp.loc[x_subset, hue_subset]
    tmp = tmp.T
    tmp = tmp.div(tmp.sum(axis=0), axis=1).T * 100
    ax = tmp.plot(kind='bar', stacked=True, figsize=figsize, color=hue_colors)
    plt.xticks(fontsize=label_fontsize, rotation=label_rotation)
    plt.yticks(fontsize=label_fontsize)
    plt.ylabel('Relative celltype abundacy(%)')
    plt.xlabel('', fontsize=label_fontsize, labelpad=label_pad)
    legend_params = {
        'loc': 'center left',
        'bbox_to_anchor': (1.01, 0.5),
        'fontsize': legend_fontsize,
        'ncol': 2,
        'frameon': False,
        'markerscale': 100,
    }

    plt.legend(**legend_params)

    change_bar_width(ax, bar_width)
    return ax


def get_cmap_colors(cmap, n, alpha=1, pad=1):
    colors = getattr(mpl.cm, cmap)(np.linspace(start=0, stop=1, num=n + 2 * pad), alpha=alpha)
    if pad > 0:
        colors = colors[pad:-pad]
    return colors


def get_grouped_colors(items, group_items, group_cmaps, alpha=1, pad=1):
    """
    Example
    ---
    ```Python
    # define the group items
    cts = adata.obs['ct_mye'].unique().tolist()
    cts = sorted(cts) # same as the order in plots. scanpy sorts the cts, but if not as this order, change this value. 
    
    # group the cell types and assign the colors
    group_cts = {
        'AM': [s for s in cts if s.startswith('AM')],
        'Mac': [s for s in cts if s.startswith('Mac')],
        'Mono': [s for s in cts if s.startswith('Mono')],
        'Others': ['cDC2', 'cDC3', 'pDC', 'Mast', 'Neutrophil'],
        'Doublets': ['Epi doublet', 'T doublet'],
    }
    group_cmaps = {
        'AM': 'Greens',
        'Mac': 'Blues',
        'Mono': 'Oranges',
        'Others': 'Purples',
        'Doublets': 'Greys',
    }
    
    # get the colors
    colors = get_grouped_colors(items=cts, group_items=group_cts, group_cmaps=group_cmaps)
    
    # plot
    sc.pl.umap(adata, color='ct_mye', palette=colors)
    ax = composition_plot(adata.obs, 'donor', 'ct_mye', figsize=(5,5), label_fontsize=10, legend_fontsize=10, hue_colors=colors)
    ```
    """
    group_colors = {}
    item_colors = {}
    groups = list(group_items.keys())
    for g in groups:
        group_colors[g] = get_cmap_colors(cmap=group_cmaps[g],
                                          n=len(group_items[g]),
                                          pad=pad,
                                          alpha=alpha)
        for i, item in enumerate(group_items[g]):
            item_colors[item] = group_colors[g][i]
    item_colors = {k: item_colors[k] for k in items}
    colors = list(item_colors.values())
    return colors