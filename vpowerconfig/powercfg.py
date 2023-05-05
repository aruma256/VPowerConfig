import re
import subprocess


class PowerCfg:
    def __init__(self):
        self.configs = []

    def update(self):
        self.configs = PowerCfg.get_powercfg_list()

    @classmethod
    def extract_uuid_and_name(cls, s: str) -> tuple[str, str]:
        pattern = r"GUID:\s*([a-fA-F0-9\-]{36})\s*\((.*)\)"
        match = re.search(pattern, s)
        assert match
        return match.group(1), match.group(2)

    @classmethod
    def get_powercfg_list(cls) -> list[tuple[str, str, bool]]:
        output = subprocess.run(["powercfg", "/list"], capture_output=True)
        result = []
        for line in output.stdout.decode("shift_jis").strip().split("\n"):
            if "GUID" in line:
                uuid, name = PowerCfg.extract_uuid_and_name(line)
                result.append((uuid, name, "*" in line))
        return result
