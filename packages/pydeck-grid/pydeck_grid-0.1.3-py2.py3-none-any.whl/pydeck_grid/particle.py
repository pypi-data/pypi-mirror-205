from .layer import GridLayer, GridLayerException, sanitize_color


class ParticleLayer(GridLayer):
    def __init__(
        self,
        data,
        datakeys,
        id=None,
        opacity=1.0,
        altitude=0.0,
        zscale=1.0,
        global_wrap=False,
        color="#999999",
        colormap=None,
        scale=1.0,
        offset=0.0,
        vmin=0.0,
        vmax=1.0,
        speed=0.5,
        direction="nautical_from",
        **kwargs,
    ):
        """Configures a deck.gl particle layer for rendering gridded data on a map. This layer only supports rectilinear grids.

        Args:
            data : xarray.DataArray
                Data to be visualized
            datakeys: dict,
                Dictionary of data keys to be used for the grid with keys:
                'x': x coordinate of the grid
                'y': y coordinate of the grid
                'z': z coordinate of the grid (optional)
                'u': u component of the vector field
                'v': v component of the vector field
                'm': magnitude of the vector field
                'd': direction of the vector field
            id : str, default None
                Unique name for layer
            opacity: float, default 1.0,
                Opacity of the layer
            altitude: float, default 0.0
                Base altitude of layer in meters
            zscale: float, default 1.0
                Multiplier scale for the vertical level of the layer
            global_wrap: bool, default False
                Boolean indicating whether the grid is global and should be wrapped around the globe
            color: str or list, default '#999999'
                Uniform color for the particles as a hex string or list of RGBA values (0-255)
            colormap: str or matplotlib.cm.ScalarMappable, default None
                If provided, colormap to use for the particles as a matplotlib predefined colormap name or a matplotlib ScalarMappable
            vmin: float, default 0.0
                Minimum value for the colormap (if colormap is a matplotlib colormap name)
            vmax: float, default 1.0
                Maximum value for the colormap (if colormap is a matplotlib colormap name)
            scale: float, default 1.0
                Multiplier scale for the values of the grid
            offset: float, default 0.0
                Offset for the values in the grid
            speed: float, default 0.5
                Speed of particles
            direction: string, default: "nautical_from"
                Type of the vector field direction. One of "nautical_from" (compass degrees), "nautical_to" (compass degrees), "cartesian_radians"

        Raises:
            GridLayerException - missing on invalid arguments
        """

        if "u" in datakeys and "v" in datakeys:
            if datakeys["u"] not in data or datakeys["v"] not in data:
                raise GridLayerException(
                    f"vector values {datakeys['u']},{datakeys['v']} not in data"
                )
        else:
            raise GridLayerException("datakeys must contain 'u' and 'v'")

        if direction not in ["nautical_from", "nautical_to", "cartesian_radians"]:
            raise GridLayerException(
                "direction must be one of 'nautical_from', 'nautical_to', 'cartesian_radians'"
            )

        super().__init__(
            type="ParticleLayer",
            data=data,
            id=id,
            opacity=opacity,
            altitude=altitude,
            zscale=zscale,
            global_wrap=global_wrap,
            color=sanitize_color(color),
            colormap=colormap,
            scale=scale,
            offset=offset,
            datakeys=datakeys,
            vmin=vmin,
            vmax=vmax,
            speed=speed,
            direction=direction,
            **kwargs,
        )


class PartmeshLayer(GridLayer):
    def __init__(
        self,
        data,
        datakeys,
        id=None,
        opacity=1.0,
        altitude=0.0,
        zscale=1.0,
        global_wrap=False,
        color="#999999",
        colormap=None,
        scale=1.0,
        offset=0.0,
        vmin=0.0,
        vmax=1.0,
        speed=0.5,
        animate=True,
        mesh={"shape": "quiver", "width": 1, "length": 4},
        **kwargs,
    ):
        """Configures a deck.gl particle mesh layer for rendering gridded data on a map. This layer only supports rectilinear grids.

        Args:
            data : xarray.DataArray
                Data to be visualized
            datakeys: dict,
                Dictionary of data keys to be used for the grid with keys:
                'x': x coordinate of the grid
                'y': y coordinate of the grid
                'z': z coordinate of the grid (optional)
                'c': scalar value of the grid
                or
                'u': u component of the vector field
                'v': v component of the vector field
            id : str, default None
                Unique name for layer
            opacity: float, default 1.0,
                Opacity of the layer
            altitude: float, default 0.0
                Base altitude of layer in meters
            zscale: float, default 1.0
                Multiplier scale for the vertical level of the layer
            global_wrap: bool, default False
                Boolean indicating whether the grid is global and should be wrapped around the globe
            color: str or list, default '#999999'
                Uniform color for the particles as a hex string or list of RGBA values
            colormap: str or matplotlib.cm.ScalarMappable, default None
                If provided, Colormap to use for the grid as a matplotlib predefined colormap name or a matplotlib ScalarMappable
            vmin: float, default 0.0
                Minimum value for the colormap (if colormap is a matplotlib colormap name)
            vmax: float, default 1.0
                Maximum value for the colormap (if colormap is a matplotlib colormap name)
            colorres: int, default 256
                Number of colors in the colormap
            scale: float, default 1.0
                Multiplier scale for the values of the grid
            offset: float, default 0.0
                Offset for the values in the grid
            speed: float, default 0.5
                Speed of particles
            animate: bool, default True
                Animate meshes
            mesh: str or dict, default {"shape": "quiver", "width": 1, "length": 4}
                Particle mesh parameters. Possible shapes are 'cone','arrow','quiver'.
                If a string is provided, the mesh will be the specified shape with default lengt and width.
                If a dictionary is provided, it must contain the key 'shape' with one of the possible shapes and optionally the keys 'width' and 'length' for the width and length of the mesh.

        Raises:
            GridLayerException - missing on invalid arguments
        """

        if "u" in datakeys and "v" in datakeys:
            if datakeys["u"] not in data or datakeys["v"] not in data:
                raise GridLayerException(
                    f"vector values {datakeys['u']},{datakeys['v']} not in data"
                )
        else:
            raise GridLayerException("datakeys must contain 'u' and 'v'")

        if isinstance(mesh, str):
            mesh = {"shape": mesh, "width": 1, "length": 4}

        if mesh["shape"] not in ["cone", "arrow", "quiver"]:
            raise GridLayerException(
                f"mesh shape {mesh['shape']} not in ['cone','arrow','quiver']"
            )
        if "width" not in mesh:
            mesh["width"] = 1

        if "length" not in mesh:
            mesh["length"] = 4

        super().__init__(
            type="PartmeshLayer",
            data=data,
            id=id,
            opacity=opacity,
            altitude=altitude,
            zscale=zscale,
            global_wrap=global_wrap,
            color=sanitize_color(color),
            colormap=colormap,
            scale=scale,
            offset=offset,
            datakeys=datakeys,
            vmin=vmin,
            vmax=vmax,
            speed=speed,
            animate=animate,
            mesh=mesh,
            **kwargs,
        )
