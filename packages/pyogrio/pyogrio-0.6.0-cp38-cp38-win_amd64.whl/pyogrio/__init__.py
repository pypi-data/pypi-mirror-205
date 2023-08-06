

""""""# start delvewheel patch
def _delvewheel_init_patch_1_3_6():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pyogrio.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if not is_pyinstaller or os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-pyogrio-0.6.0')
        if not is_pyinstaller or os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-pyogrio-0.6.0')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if not is_pyinstaller or os.path.isfile(lib_path):
                    ctypes.WinDLL(lib_path)


_delvewheel_init_patch_1_3_6()
del _delvewheel_init_patch_1_3_6
# end delvewheel patch

try:
    # we try importing shapely, to ensure it is imported (and it can load its
    # own GEOS copy) before we load GDAL and its linked GEOS
    import shapely  # noqa
    import shapely.geos  # noqa
except Exception:
    pass

from pyogrio.core import (
    list_drivers,
    list_layers,
    read_bounds,
    read_info,
    set_gdal_config_options,
    get_gdal_config_option,
    get_gdal_data_path,
    __gdal_version__,
    __gdal_version_string__,
    __gdal_geos_version__,
)
from pyogrio.geopandas import read_dataframe, write_dataframe
from pyogrio._version import get_versions


__version__ = get_versions()["version"]
del get_versions

__all__ = [
    "list_drivers",
    "list_layers",
    "read_bounds",
    "read_info",
    "set_gdal_config_options",
    "get_gdal_config_option",
    "get_gdal_data_path",
    "read_dataframe",
    "write_dataframe",
    "__gdal_version__",
    "__gdal_version_string__",
    "__gdal_geos_version__",
    "__version__",
]
