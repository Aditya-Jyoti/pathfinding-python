from pathfinding.runner import Pathfinder
from toml import load as toml_load

if __name__ == "__main__":
    with open("settings.toml", "r") as toml_file:
        settings = toml_load(toml_file)["settings"]

    pathfinder = Pathfinder(settings)
    pathfinder.pathfind()