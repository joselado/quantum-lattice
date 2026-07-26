"""Shared PyVista plotting helpers for the utilities/ scripts.

PyVista wraps VTK with a friendly, actively maintained API, giving the
same real lighting/shading and true spheres/tubes mayavi had. Unlike
mayavi (whose own tvtk wrapper-generation step fails to build on newer
Python - confirmed while testing this port), PyVista installs from
prebuilt wheels with no compiler needed, the same way this app's other
dependencies do.

Not a `ql-*` command: this module is only imported by sibling scripts in
this directory, never launched directly.
"""
import numpy as np
import pyvista as pv
from scipy.spatial import cKDTree
import plotstyle # same directory - matplotlib scripts already rely on
                  # this sys.path.insert(0,dirname) done by every caller


def new_plotter(title=None):
    pl = pv.Plotter(title=title or "Quantum Lattice")
    dark = plotstyle._env_wants_dark() # follows the same QL_THEME switch
                                        # plotstyle.apply() uses for the
                                        # matplotlib-based ql-* scripts
    pl.set_background(plotstyle.BACKGROUND_DARK if dark else "white")
    return pl


def text_color():
    """Foreground color for on-screen labels (pl.add_text/add_text
    below), matching whichever background new_plotter() just picked -
    default PyVista text is black, invisible against a dark background."""
    return plotstyle.FOREGROUND_DARK if plotstyle._env_wants_dark() else "black"


def add_text(pl,*args,**kwargs):
    """pl.add_text() with a theme-correct default color; pass color=...
    explicitly to override."""
    kwargs.setdefault("color",text_color())
    return pl.add_text(*args,**kwargs)


def nearest_neighbor_distance(points):
    """Median distance from each point to its nearest neighbor, used to
    size atoms relative to the lattice instead of an arbitrary constant"""
    points = np.asarray(points)
    if len(points)<2: return 1.0
    d,_ = cKDTree(points).query(points,k=2) # k=1 is the point itself (d=0)
    return float(np.median(d[:,1]))


def add_atoms(pl,xyz,color="cyan",radius=None,opacity=1.0):
    """Draw atoms as true shaded spheres (in world/data coordinates, so
    they keep a fixed physical size independent of camera zoom) at the
    given (3,n) positions. Defaults to 1/3 of the nearest-neighbor
    distance, which keeps neighboring atoms from overlapping."""
    points = np.asarray(xyz).T
    if radius is None: radius = nearest_neighbor_distance(points)/3.0
    sphere = pv.Sphere(radius=radius,theta_resolution=12,phi_resolution=12)
    glyph = pv.PolyData(points).glyph(geom=sphere,scale=False,orient=False)
    pl.add_mesh(glyph,color=color,opacity=opacity)
    return points


def add_scaled_points(pl,xyz,scalars,color=None,cmap="viridis",point_size=30,opacity=0.6):
    """Draw points scaled/colored by a per-point scalar (e.g. LDOS weight)"""
    points = np.asarray(xyz).T
    cloud = pv.PolyData(points)
    cloud["scalars"] = np.asarray(scalars)
    kwargs = dict(render_points_as_spheres=True,scalars="scalars",
                  point_size=point_size,opacity=opacity,show_scalar_bar=False)
    if color is not None: kwargs["color"] = color
    else: kwargs["cmap"] = cmap
    pl.add_mesh(cloud,**kwargs)


def bonds_between(rs1,rs2,dmin=0.0,dmax=1.1):
    """Index pairs (i,j) whose Euclidean distance falls in (dmin,dmax)"""
    pairs = []
    for i,ri in enumerate(rs1):
        for j,rj in enumerate(rs2):
            dr = ri-rj
            d = np.sqrt(dr.dot(dr))
            if dmin<d<dmax: pairs.append((i,j))
    return pairs


def add_bonds(pl,rs1,rs2,pairs=None,dmin=0.0,dmax=1.1,color="gray",radius=0.1):
    """Draw bonds as true cylindrical tubes between the given index pairs
    of positions (or every pair within (dmin,dmax) if pairs is not given)"""
    if pairs is None: pairs = bonds_between(rs1,rs2,dmin=dmin,dmax=dmax)
    if len(pairs)==0: return None
    points,lines = [],[]
    for (i,j) in pairs:
        n = len(points)
        points.append(rs1[i]); points.append(rs2[j])
        lines.append([2,n,n+1])
    poly = pv.PolyData()
    poly.points = np.array(points)
    poly.lines = np.hstack(lines)
    tubes = poly.tube(radius=radius)
    pl.add_mesh(tubes,color=color)
    return tubes


def add_arrows(pl,xyz,vec,color="red",mag=1.0):
    """Draw arrows at positions xyz with direction/magnitude vec"""
    points = np.asarray(xyz).T
    directions = np.asarray(vec).T
    pl.add_arrows(points,directions,mag=mag,color=color)


def add_trisurf(pl,x,y,z,cmap="viridis"):
    """Delaunay-triangulated surface through scattered (x,y,z) points"""
    points = np.column_stack([x,y,z])
    cloud = pv.PolyData(points)
    cloud["z"] = z
    surf = cloud.delaunay_2d()
    pl.add_mesh(surf,scalars="z",cmap=cmap,show_scalar_bar=False)
    return surf


def enable_point_picking(pl,points,callback):
    """Wire up click-to-pick on a point cloud; `callback(index)` is called
    with the index of the point nearest the click. Replaces mayavi's
    figure.on_mouse_pick point picker."""
    points = np.asarray(points)
    def _on_pick(picked_point):
        if picked_point is None: return
        d2 = np.sum((points-np.asarray(picked_point))**2,axis=1)
        callback(int(np.argmin(d2)))
    pl.enable_point_picking(callback=_on_pick,picker="point",
                             left_clicking=True,show_message=True)


def enable_area_picking(pl,points,callback):
    """Wire up click-drag rectangle picking on a point cloud (press "r" to
    start drawing, drag, release to select, "r" again to stop); `callback`
    is called with the array of indices of every point enclosed by the
    selection, projected through the full depth of the scene - the 3D
    equivalent of a 2D lasso-select, for bulk selection instead of
    clicking points one by one. A rectangle click-drag is also VTK's
    trackball camera rotation gesture, so this can't just run alongside
    enable_point_picking the way the matplotlib LassoSelector runs
    alongside a plain click in the 2D pickers (see ql-remove-atoms-geometry) -
    the caller is expected to toggle between the two with pl.disable_picking()
    in between, e.g. bound to its own key event."""
    points = np.asarray(points)
    cloud = pv.PolyData(points)
    def _on_rectangle(selection):
        sel = cloud.select_interior_points(selection.frustum_mesh,check_surface=False)
        indices = np.nonzero(np.asarray(sel["selected_points"],dtype=bool))[0]
        if len(indices)==0: return
        callback(indices)
    pl.enable_rectangle_picking(callback=_on_rectangle,show_message=True)
