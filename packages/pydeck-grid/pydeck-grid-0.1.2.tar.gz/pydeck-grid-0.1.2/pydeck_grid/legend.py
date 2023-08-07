import jinja2
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, Normalize


def colorbar_div(
    colormap,
    labels=None,
    units=None,
    width=200,
    height=50,
    labelcolor="white",
):
    grads = labels or colormap["domain"]
    labelwidth = int(width / (len(grads) + int(units is not None)))
    gradient = [grads[0], grads[0], grads[0]] if units else [grads[0]]
    if len(colormap["scale"]) == len(colormap["domain"]):
        lscm = LinearSegmentedColormap.from_list(
            "colormap", zip(colormap["scale"], colormap["domain"])
        )
        norm = lambda x: x
    else:
        lscm = ListedColormap(colormap["scale"])
        norm = Normalize(vmin=colormap["domain"][0], vmax=colormap["domain"][-1])
    for i, l in enumerate(grads):
        i0 = i if i < len(grads) - 1 else i - 1
        gradient = gradient + [l, 0.5 * (l + grads[i0 + 1])]
    colorString = []
    for g in gradient:
        rgb = [int(255 * c) for c in lscm(norm(g))]
        colorString.append(f"rgb({rgb[0]},{rgb[1]},{rgb[2]})")
    ticks = ([units] if units else []) + grads
    labelsize = min(int(width / 2 / len(grads)), int(height / 1.5))
    colorbar_template = jinja2.Template(
        """
    <div
      style="
        width: {{ width }}px;
        height: {{ height }}px;
        border-radius: 5px;
        background: linear-gradient(to right, {{ ",".join(colorString) }});
        font-size: {{ labelsize }}px;
        display: flex;
        align-items: center;
      "
    >
        {% for tick in ticks %}
        <span
          style="
            width: {{ labelwidth }}px;
            text-align: center;
            vertical-align: middle;
            display: inline-block;
            color: {{ labelcolor }}"
        >
          {{ tick }}
        </span>
        {% endfor %}
    </div>
    """
    )
    html_str = colorbar_template.render(
        colorString=colorString,
        width=width,
        height=height,
        ticks=ticks,
        labelsize=labelsize,
        labelwidth=labelwidth,
        labelcolor=labelcolor,
    )
    return html_str
