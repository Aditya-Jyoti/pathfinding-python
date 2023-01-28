from pathfinding.runner import Pathfinder
from toml import load as toml_load

if __name__ == "__main__":
    with open("settings.toml", "r") as toml_file:
        contents = toml_load(toml_file)
        settings = contents["settings"]
        about = contents["projects"]

    print(f"""
    {about['description']}

    author: {about['author']}
    version: {about['version']}
    license: {about['license']}    
""")

    pathfinder = Pathfinder(settings)
    pathfinder.main()