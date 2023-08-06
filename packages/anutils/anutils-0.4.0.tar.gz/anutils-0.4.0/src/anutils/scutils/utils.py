def filter_batches_with_too_few_samples(adata, batch_key, min_samples, inplace=True):
    """
    params:
    ---
    adata: anndata.AnnData
        AnnData object
    batch_key: str
        key in `adata.obs` to use for batch
    min_samples: int
        minimum number of samples in a batch to keep
    
    returns:
    ---
    adata: anndata.AnnData
        AnnData object with batches with fewer than `min_samples` removed
    """
    batch_sizes = adata.obs[batch_key].value_counts()
    batches_to_keep = batch_sizes[batch_sizes >= min_samples].index
    if not inplace:
        adata = adata.copy()
    adata = adata[adata.obs[batch_key].isin(batches_to_keep)]
    return adata

