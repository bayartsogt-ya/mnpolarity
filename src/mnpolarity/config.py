import os
from .utils import read_config

# --------------- Configuration ---------------
package_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..",
)

config = read_config(
    os.path.join(package_dir, "configs", "main.yml")
)

config["package_dir"] = package_dir
config["data_dir"] = os.path.join(package_dir, "data")
