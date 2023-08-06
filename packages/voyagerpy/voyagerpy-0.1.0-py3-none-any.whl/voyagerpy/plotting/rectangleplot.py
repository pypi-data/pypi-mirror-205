from matplotlib.patches import Rectangle


def boxs(adata, x="cluster", y="in_tissue", color_by: str = None, cmap: str = "dittoseq"):
    assert y is not None

    group_columns = [y] if x is None else [x, y]
    legend = color_by in group_columns
    tab = adata.obs.groupby(group_columns).size()

    rel = tab / tab.max()
    tab = pd.DataFrame({"counts_": tab}, dtype="int")
    tab["density_"] = rel
    size_const = 0.45
    tab["x"] = size_const
    tab["y"] = size_const

    if x is not None:
        levels = tab.index.levels
        x_levels, y_levels = levels
    else:
        x_levels, y_levels = [0], tab.index.categories
    x_size, y_size = len(x_levels), len(y_levels)

    if y_size == 1 and x_size != 1:
        tab["y"] *= tab["density_"]
    elif y_size != 1 and x_size == 1:
        tab["x"] *= tab["density_"]
    else:
        tab["x"] *= np.sqrt(tab["density_"])
        tab["y"] *= np.sqrt(tab["density_"])

    fig, ax = plt.subplots()
    cmap = plt.get_cmap(cmap)

    if x is not None:
        enumerator = [((x_pos, y_pos), (x_key, y_key)) for x_pos, x_key in enumerate(x_levels) for y_pos, y_key in enumerate(y_levels)]
    else:
        enumerator = [((0, y_pos), y_key) for y_pos, y_key in enumerate(y_levels)]

    for (x_pos, y_pos), key in enumerator:
        width, height, n_points = tab.loc[key, ["x", "y", "counts_"]]
        x_offset = x_pos + 0.5 - width
        y_offset = y_pos + 0.5 - height

        points = np.random.random(size=(int(n_points), 2)) * [2 * width, 2 * height] + [x_offset, y_offset]

        color = 0
        if color_by == x:
            color = cmap(x_pos)
        elif color_by == y:
            color = cmap(y_pos)
        else:
            color = cmap(0)

        xy, w, h = (x_offset, y_offset), 2 * width, 2 * height
        rect = Rectangle(xy, w, h, edgecolor="k", facecolor="lightgray", alpha=0.5)
        ax.add_patch(rect)

        label = x_pos if color_by == x else y_pos
        ax.scatter(*points.T, alpha=0.5, s=8, color=color, label=label)

    ax.set_xticks(np.arange(x_size) + 0.5, labels=x_levels)
    ax.set_yticks(np.arange(y_size) + 0.5, labels=y_levels)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.grid(False)

    if legend:
        handles = ax.collections

        if color_by == x:
            handles = handles[::y_size]
            labels = list(x_levels)
        elif color_by == y:
            handles = handles[:y_size]
            labels = list(y_levels)
        else:
            return ax
        ax.legend(labels=labels, handles=handles, loc="best")

    return ax


x = None
x = "cluster"
ax = boxs(adata, x=x, cmap="tab10", color_by="in_tissue")
