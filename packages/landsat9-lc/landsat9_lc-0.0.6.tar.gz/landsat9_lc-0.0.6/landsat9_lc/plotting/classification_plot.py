import xarray as xr
import matplotlib.pyplot as plt

def classification_plot(
    array: xr.DataArray,
    title: str = 'Result of the model',
    cmap_label: str = 'Estimated Land Cover'
    ) -> None:
    """
    
    """
    if not isinstance(array, xr.DataArray):
        raise TypeError('`array` parameter must be a xarray DataArray.')
    levels = [x for x in range(1, 11)]
    colors=['aqua', 'forestgreen', 'snow', 'lightgray', 'dimgray', 'lawngreen', 
            'springgreen', 'blanchedalmond','lightpink', 'turquoise']
    labels=['Water', 'Forest', 'Snow/Ice', 'Cloud', 'Cloud Shadow', 'Agriculture', 'Vegetation',
            'low/no Vegetation', 'Artificial Zone', 'Wetlands']
    fig, ax = plt.subplots()
    cax = array.plot(
    levels=levels,
    colors=colors,
    add_colorbar=False,
)
    cbar = plt.colorbar(
        cax,
        label=cmap_label,
        )
    cbar.ax.set_yticklabels(labels)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.draw()