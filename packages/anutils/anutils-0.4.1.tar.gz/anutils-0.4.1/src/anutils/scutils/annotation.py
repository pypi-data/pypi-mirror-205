"""
cell type annotation utils.
---
Ning Weixi 20230209
"""
import scanpy as sc
import numpy as np
import pandas as pd


def score_celltypes_by_markers(adata, groupby, markers):
    """infer cell types from markers

    Parameters
    ----------
    adata : AnnData
        adata object.
    groupby : str
        groupby.
    markers : dict
        a dict of celltype: [marker genes] pairs.
    """
    adata = adata.copy()
    for celltype, genes in markers.items():
        sc.tl.score_genes(adata, genes, score_name=celltype)
    scores = adata.obs.groupby(groupby)[list(markers.keys())].mean()
    return scores


def infer_celltype_from_dotplot(adata, groupby, markers):
    """
    params
    ---
    markers: same as `var_names` in `sc.pl.DotPlot`. a `dict` of `celltype: gene list` pairs.
    
    returns
    ---
    cts: a `dict` of `celltype: group list` pairs.
    """
    dp = sc.pl.DotPlot(adata, groupby=groupby, use_raw=True, var_names=markers)
    inferred_cts = np.array(
        sum([[celltype] * (item[1] + 1 - item[0])
             for celltype, item in zip(dp.var_group_labels, dp.var_group_positions)],
            start=[]))[np.argmax((dp.dot_color_df * dp.dot_size_df).values, axis=1)]
    cts = {ct: np.where(inferred_cts == ct)[0].tolist() for ct in np.unique(inferred_cts)}
    return cts


def get_marker_genes(marker_genes, adata):
    """subset marker genes to those in adata.raw.var_names

    Parameters
    ----------
    marker_genes : dict
        dict of celltype: [marker genes] pairs.
    adata : AnnData
        adata object.

    Returns
    -------
    new_markers : dict
        dict of celltype: [marker genes] pairs.
    """
    new_markers = {}
    for k, v in marker_genes.items():
        gene_list = [gene for gene in v if gene in adata.raw.var_names]
        if len(gene_list) > 0:
            new_markers[k] = gene_list
    return new_markers


def group_degs(adata,
               groupby,
               groups=None,
               nhead=6,
               ncols=6,
               min_logfoldchange=2.5,
               max_pval_adj=1e-4,
               min_pct=0.0,
               plot=True):
    """get DEGs for each group, and plot them on UMAP

    Parameters
    ----------
    adata : AnnData
        adata object.
    groupby : str
        column name in adata.obs.
    groups : Iterable[str], optional
        group subset, by default None
    nhead : int, optional
        number of highest score genes to show and plot, by default 6
    ncols : int, optional
        ncols of the umaps, by default 6
    min_logfoldchange : float, optional
        log2fc_min, by default 2.5
    max_pval_adj : float, optional
        padj_max, by default 1e-4
    min_pct : float, optional
        min percentage of cells to express the gene in the group, by default 0.0
    plot : bool, optional
        whether to plot, by default True

    Returns
    -------
    dfs : list[pd.DataFrame]
        list of DEGs for each group.
    """
    ad = adata.copy()
    if groups is None:
        groups = ad.obs[groupby].cat.categories.tolist()
    # add log1p base to adata
    if 'log1p' in ad.uns and 'base' not in ad.uns['log1p']:
        ad.uns['log1p']['base'] = np.e
    sc.tl.rank_genes_groups(ad, groupby=groupby, groups=groups, pts=True)
    dfs = []
    for g in groups:
        df = sc.get.rank_genes_groups_df(ad, group=g)
        df = df[(df.logfoldchanges > min_logfoldchange) & (df.pvals_adj < max_pval_adj) &
                (df.pct_nz_group > min_pct)]
        print(f'group `{g}`: {len(df)} DEGs')
        if len(df) == 0:
            continue
        if nhead > 0:
            print(df.head(nhead))
        if plot:
            sc.pl.umap(ad,
                       color=df.names.values[:nhead],
                       ncols=ncols,
                       frameon=False,
                       colorbar_loc=None,
                       wspace=0)
        dfs.append((g, df))
    return dfs


def infer_celltype_from_scores(ad, markers, groupby, no_verbose=True):
    if no_verbose:
        verb = sc.settings.verbosity
        sc.settings.verbosity = 0
    markers = get_marker_genes(markers, ad)
    ad = ad.copy()
    cts = []
    for ct in markers.keys():
        cts.append(ct)
        sc.tl.score_genes(ad,
                          gene_list=markers[ct],
                          copy=False,
                          score_name=ct,
                          gene_pool=sum(markers.values(), []))
    df = ad.obs.loc[:, [groupby] + cts]
    df = df.groupby(groupby).mean()
    anno_dict = pd.DataFrame(
        zip(df.columns[np.argmax(df.values, 1)], df.index),
        columns=['anno',
                 groupby]).groupby('anno').apply(lambda df: df[groupby].to_list()).to_dict()
    if no_verbose:
        sc.settings.verbosity = verb
    return anno_dict