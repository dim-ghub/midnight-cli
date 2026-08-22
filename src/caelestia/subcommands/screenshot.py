import shlex
import subprocess
from argparse import Namespace
from datetime import datetime
from pathlib import Path
from typing import Any

from caelestia.utils import hypr
from caelestia.utils.notify import notify
from caelestia.utils.paths import get_config, screenshots_cache_dir, screenshots_dir


class Command:
    args: Namespace

    def __init__(self, args: Namespace) -> None:
        self.args = args

    def run(self) -> None:
        if getattr(self.args, "file", None):
            self.file()
        elif self.args.region:
            self.region()
        else:
            self.fullscreen()

    def file(self) -> None:
        raw_path = Path(self.args.file)
        if not raw_path.is_file():
            raise FileNotFoundError(f"Screenshot file not found: {raw_path}")
        sc_data = raw_path.read_bytes()
        self.handle_action(sc_data, is_region=True)

    def get_action(self, cfg: dict[str, Any], is_region: bool) -> str:
        # CLI flags have highest priority
        if getattr(self.args, "save", False):
            return "save"
        if getattr(self.args, "copy", False) or getattr(self.args, "clipboard", False):
            return "copy"
        if getattr(self.args, "edit", False) or getattr(self.args, "open", False):
            return "edit"
        if getattr(self.args, "notify", False):
            return "notify"
        if getattr(self.args, "action", None):
            act = self.args.action.lower()
            if act == "open":
                return "edit"
            if act == "clipboard":
                return "copy"
            return act

        # Config file options
        if is_region and "regionAction" in cfg:
            act = str(cfg["regionAction"]).lower()
            return "edit" if act == "open" else "copy" if act == "clipboard" else act
        if not is_region and "fullscreenAction" in cfg:
            act = str(cfg["fullscreenAction"]).lower()
            return "edit" if act == "open" else "copy" if act == "clipboard" else act
        if "action" in cfg:
            act = str(cfg["action"]).lower()
            return "edit" if act == "open" else "copy" if act == "clipboard" else act

        # Defaults
        return "edit" if is_region else "notify"

    def get_app(self, cfg: dict[str, Any]) -> str | list[str]:
        if getattr(self.args, "app", None):
            return self.args.app
        return cfg.get("app") or cfg.get("editor") or cfg.get("command") or "swappy"

    def launch_app(self, app_spec: str | list[str], sc_data: bytes, file_path: Path) -> None:
        if isinstance(app_spec, list):
            cmd_list = [str(c) for c in app_spec]
        else:
            cmd_list = shlex.split(str(app_spec))

        if not cmd_list:
            cmd_list = ["swappy"]

        path_str = str(file_path)
        placeholders = ["{}", "{file}", "{filename}", "%f", "$FILE", "<FILENAME>", "<filename>", "<FILE>", "<file>"]

        has_placeholder = any(any(ph in token for ph in placeholders) for token in cmd_list)

        if has_placeholder:
            final_cmd: list[str] = []
            for token in cmd_list:
                for ph in placeholders:
                    token = token.replace(ph, path_str)
                final_cmd.append(token)
            subprocess.Popen(final_cmd, start_new_session=True)
        elif "-" in cmd_list:
            proc = subprocess.Popen(cmd_list, stdin=subprocess.PIPE, start_new_session=True)
            if proc.stdin:
                proc.stdin.write(sc_data)
                proc.stdin.close()
        elif len(cmd_list) == 1:
            base_cmd = cmd_list[0]
            if base_cmd == "tensaku":
                subprocess.Popen(["tensaku", "--filename", path_str], start_new_session=True)
            elif base_cmd == "satty":
                subprocess.Popen(["satty", "--filename", path_str], start_new_session=True)
            elif base_cmd == "swappy":
                subprocess.Popen(["swappy", "-f", path_str], start_new_session=True)
            else:
                subprocess.Popen([base_cmd, path_str], start_new_session=True)
        else:
            subprocess.Popen([*cmd_list, path_str], start_new_session=True)

    def handle_action(self, sc_data: bytes, is_region: bool) -> None:
        cfg = get_config().get("screenshot", {})
        action = self.get_action(cfg, is_region)
        save_dir = Path(cfg.get("saveDir") or cfg.get("directory") or screenshots_dir).expanduser()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        screenshots_cache_dir.mkdir(exist_ok=True, parents=True)
        cache_dest = screenshots_cache_dir / f"{timestamp}.png"
        cache_dest.write_bytes(sc_data)

        if action == "edit":
            app_spec = self.get_app(cfg)
            self.launch_app(app_spec, sc_data, cache_dest)

        elif action == "copy":
            subprocess.run(["wl-copy"], input=sc_data)
            notify(
                "-i",
                "image-x-generic-symbolic",
                "-h",
                f"STRING:image-path:{cache_dest}",
                "Screenshot copied",
                "Screenshot copied to clipboard",
            )

        elif action == "save":
            save_dir.mkdir(exist_ok=True, parents=True)
            save_dest = save_dir / f"{timestamp}.png"
            save_dest.write_bytes(sc_data)
            if cfg.get("copyOnSave", True):
                subprocess.run(["wl-copy"], input=sc_data)
            notify(
                "-i",
                "image-x-generic-symbolic",
                "-h",
                f"STRING:image-path:{save_dest}",
                "Screenshot saved",
                f"Saved to {save_dest}",
            )

        elif action == "notify":
            subprocess.run(["wl-copy"], input=sc_data)
            res = notify(
                "-i",
                "image-x-generic-symbolic",
                "-h",
                f"STRING:image-path:{cache_dest}",
                "--action=open=Open",
                "--action=save=Save",
                "Screenshot taken",
                f"Screenshot stored in {cache_dest} and copied to clipboard",
            )
            if res == "open":
                app_spec = self.get_app(cfg)
                self.launch_app(app_spec, sc_data, cache_dest)
            elif res == "save":
                save_dir.mkdir(exist_ok=True, parents=True)
                save_dest = save_dir / f"{timestamp}.png"
                cache_dest.rename(save_dest)
                notify(
                    "-i",
                    "image-x-generic-symbolic",
                    "-h",
                    f"STRING:image-path:{save_dest}",
                    "Screenshot saved",
                    f"Saved to {save_dest}",
                )

    def region(self) -> None:
        if self.args.region == "slurp":
            subprocess.run(
                ["qs", "-c", "caelestia", "ipc", "call", "picker", "openFreeze" if self.args.freeze else "open"]
            )
        else:
            sc_data = subprocess.check_output(["grim", "-l", "0", "-g", self.args.region.strip(), "-"])
            self.handle_action(sc_data, is_region=True)

    def fullscreen(self) -> None:
        cmd = ["grim"]
        monitors = hypr.message("monitors")
        focused_monitor = next((m for m in monitors if m.get("focused")), None)
        if focused_monitor:
            cmd += ["-o", focused_monitor["name"]]
        cmd += ["-"]
        sc_data = subprocess.check_output(cmd)
        self.handle_action(sc_data, is_region=False)

