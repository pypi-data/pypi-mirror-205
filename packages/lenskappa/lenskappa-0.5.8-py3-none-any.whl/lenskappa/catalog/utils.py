from heinlein.dtypes.catalog import Catalog
from astropy.coordinates import SkyCoord
from copy import copy
import astropy.units as u

def rotate(catalog: Catalog, center: SkyCoord, new_center: SkyCoord) -> Catalog:
    original = catalog.coords
    separations = original.separation(center)
    pas = original.position_angle(center)
    new_coords = new_center.directional_offset_by(pas - 180*u.deg, separations)
    new_cat = copy(catalog)
    new_cat.update_coords(new_coords)
    return new_cat