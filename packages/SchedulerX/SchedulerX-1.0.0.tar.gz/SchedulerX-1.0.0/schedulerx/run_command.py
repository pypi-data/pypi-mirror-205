from dataclasses import dataclass

import subprocess


@dataclass
class CommandHandler:

    def run_shell_command(self, command: str):
        """ run shell command simple usage"""
        process = subprocess.run(
            [f"{command}"],
            shell=True,
            capture_output=True,
            encoding="utf-8",
            timeout=6,
        )
        return process


if __name__ == "__main__":
    ch = CommandHandler()
    print(ch.run_shell_command("sudo mkdir -p /mnt/delete"))
