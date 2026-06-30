import minecraft_launcher_lib as mc
from pathlib import Path
import os
import shutil
DEBUG = False

class installer_mc():
    def __init__(self):
        # default path
        self.mc_path_default = Path.home()
        # loaders
        self.fabric_loader = mc.mod_loader.Fabric()
        self.forge_loader = mc.mod_loader.Forge()
        self.quilt_loader = mc.mod_loader.Quilt()
        self.neoforge_loader = mc.mod_loader.Neoforge()
        
    def find_java_path(self):
        java_components = [
            "java-runtime-delta",  # Java 21 (Minecraft 1.20.5+)
            "java-runtime-gamma",  # Java 17 (Minecraft 1.18 - 1.20.4)
            "java-runtime-beta",   # Java 16 (Minecraft 1.17)
            "java-runtime-alpha",  # Java 8  (Minecraft 1.16 ke bawah)
        ]

        runtime_paths = []

        # Bangun daftar path berdasarkan OS
        if os.name == 'nt':
            for comp in java_components:
                runtime_paths.extend([
                    runtime_dir / comp / "windows-x64" / comp / "bin" / "java.exe",
                    runtime_dir / comp / "windows-x86" / comp / "bin" / "java.exe",
                ])
        elif os.name == "darwin":
            for comp in java_components:
                runtime_paths.append(
                    runtime_dir / comp / "mac-os" / comp / "jre.bundle" / "Contents" / "Home" / "bin" / "java"
                )
        else:
            # Linux (Mojang menggunakan 'linux' untuk 64-bit pada runtime baru)
            for comp in java_components:
                runtime_paths.extend([
                    runtime_dir / comp / "linux" / comp / "bin" / "java",
                    runtime_dir / comp / "linux-i386" / comp / "bin" / "java",
                ])
        for path in runtime_paths:
            if path.exists() and path.is_file():
                return path
        
        # kalo windows nya udah ada java di os nya
        java_win = "javaw.exe" if os.name == 'nt' else 'java'
        sys_java = shutil(java_win)
        if sys_java:
            return Path(sys_java)

    def get_compatible_loader_version(self,loader:str,minecraft_version:str):
        # fabric loader
        if loader == 'fabric':
            compatible_version = mc.fabric.is_minecraft_version_supported(minecraft_version)
        # forge loader
        elif loader == 'forge':
            compatible_version = mc.forge.find_forge_version(minecraft_version)
        # quilt loader
        else:
            compatible_version = mc.quilt.is_minecraft_version_supported(minecraft_version)
        return compatible_version
    
    def install(self,version:str,loader:str,mc_dir:str):
        def callback(name:str,progress:int,total:int):
            if total > 0:
                percentage = (progress / total) * 100

        # fabric loader
        if loader == 'fabric':
            return mc.fabric.install_fabric(version,mc_dir,self.get_compatible_loader_version(loader,version),callback(f'MC {loader} | {version}'),self.find_java_path())
        # forge loader
        elif loader == 'forge':
            return mc.forge.install_minecraft_version(version,mc_dir,self.get_compatible_loader_version(loader,version),callback(f'MC {loader} | {version}'))
        # quilt loader
        else:
            return mc.quilt.install_minecraft_version(version,mc_dir,self.get_compatible_loader_version(loader,version),callback(f'MC {loader} | {version}'))

    



if __name__ == "__main__":
    installer_mc()