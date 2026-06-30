import os
import json
import uuid
import hashlib
import subprocess
from pathlib import Path
import minecraft_launcher_lib as mc
from src.installer import find_java_path

USER_SETTINGS = ''
LAUNCHER_SETTINGS = ''
DEBUG = False


class launcher():
    def __init__(self):
        self.settings = Path(f'{os.getcwd()}/src/data/{USER_SETTINGS}.json')
        self.process = None
        
    def launch(self):
        settings = self.settings
        options = {
            "username": username,
            "uuid": uuid,
            "token": access_token,
            "executablePath": str(find_java_path) if find_java_path else None,
            "gameDirectory": str(self.minecraft_dir / "instances" / "my_custom_instance"),
        }
        java_args = [
            f"-Xmx{self.settings['max_memory']}M",
            f"-Xms{self.settings['min_memory']}M"
        ]
        # Masukkan jvm_args ke dalam options
        options["jvmArgs"] = jvm_args
        
        cmd = mc.command.get_minecraft_command(
            version=self.settings['current_version'],
            minecraft_directory=settings['mc_dir'],
            options=options
        )
        self.process = subprocess.Popen(
            stdin=subprocess.PIPE,
            stdout=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'   
        )
        

if __name__ == "__main__":
    launcher()
