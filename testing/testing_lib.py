import minecraft_launcher_lib as mc
import os

fabric = mc.mod_loader.Fabric()

fabric.install('26.1.1',minecraft_directory=f"{os.getcwd()}/testing/")

