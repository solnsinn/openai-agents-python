"""
CodingAutomationAgent: An agent for code generation, website scaffolding, and automation tasks.
"""
import os
import subprocess
from pathlib import Path
from typing import Optional

# Base directory for all generated artifacts; resolves to an absolute path.
BASE_DIR = Path("src/agents/generated").resolve()

class CodingAutomationAgent:
    """
    CodingAutomationAgent
    ---------------------

    A small helper class to create and manage simple code and website scaffolding tasks
    and to run shell commands for basic automation workflows.

    This class is intentionally lightweight and performs direct filesystem and shell
    operations; callers are responsible for providing safe, validated inputs.

    Attributes:
        name (str): Human-readable name for the agent instance.

    Methods:
        __init__(name: str = "CodingAutomationAgent") -> None
            Initialize the agent with an optional name.

        generate_code(code: str, filename: str, directory: str = "src/agents/generated/") -> str
            Write the provided source `code` to a file named `filename` inside `directory`.
            Creates the target directory if it does not exist and returns the full path to
            the written file.

            Notes:
                - The method performs filesystem writes inside a constrained base directory
                  to avoid accidental path traversal outside the intended area.
                - May raise OSError (or its subclasses) if the directory cannot be created or
                  the file cannot be written (permission errors, disk full, etc).

        scaffold_website(site_name: str, template: Optional[str] = None) -> str
            Create a basic website folder named with `site_name` under
            "src/agents/generated/" and write a minimal index.html with a page title and
            heading set to `site_name`. Returns the path to the created site base directory.

            Args:
                site_name: Name of the website folder to create.
                template: Optional template identifier (currently not applied by default).
            Notes:
                - As implemented, `template` is optional but not used to populate additional
                  files; callers can extend this behavior to copy templates or assets.
                - May raise OSError on filesystem errors.

        automate_task(command: str) -> int
            Execute a shell command using subprocess.run and return its exit status code.

            Security and behavioral notes:
                - Using a shell (shell=True) is intentionally preserved for compatibility with
                  shell features; callers should avoid passing untrusted input into `command`.
                - The command runs with the same privileges as the current process and may
                  have side effects (create/modify files, network access, etc).
    """
    def __init__(self, name: str = "CodingAutomationAgent"):
        self.name = name

    def _ensure_within_base(self, path: Path) -> None:
        """Raise ValueError if path is not inside BASE_DIR."""
        try:
            path.relative_to(BASE_DIR)
        except Exception:
            raise ValueError(f"Target path {str(path)} is outside the allowed base directory {BASE_DIR}")

    def generate_code(self, code: str, filename: str, directory: str = ".") -> str:
        """Generate a code file in the specified directory under the constrained base directory."""
        # Normalize directory input: if absolute, treat as explicit; otherwise resolve relative to BASE_DIR.
        dir_path = Path(directory)
        if dir_path.is_absolute():
            target_dir = dir_path.resolve()
        else:
            # If caller passed the default ".", use BASE_DIR directly to avoid doubling the path.
            if str(dir_path) in (".", ""):
                target_dir = BASE_DIR
            else:
                target_dir = (BASE_DIR / dir_path).resolve()

        # Ensure the target dir is within the allowed base directory.
        self._ensure_within_base(target_dir)

        # Create the directory tree.
        target_dir.mkdir(parents=True, exist_ok=True)

        # Sanitize filename: only use the final name component to avoid path traversal.
        safe_name = Path(filename).name
        if not safe_name or safe_name in (".", ".."):
            raise ValueError("Invalid filename provided")

        file_path = target_dir / safe_name
        # Write the file using a safe Path method.
        file_path.write_text(code, encoding="utf-8")
        return str(file_path)

    def scaffold_website(self, site_name: str, template: Optional[str] = None) -> str:
        """Scaffold a basic website structure inside the constrained generated base directory."""
        # Basic validation to avoid directory traversal via site_name.
        if not site_name or any(sep in site_name for sep in (os.path.sep, "/", "\\")) or site_name in (".", ".."):
            raise ValueError("Invalid site_name")

        base_dir = (BASE_DIR / site_name).resolve()
        self._ensure_within_base(base_dir)
        base_dir.mkdir(parents=True, exist_ok=True)

        # Create index.html
        index_html = "<html><head><title>{}</title></head><body><h1>Welcome to {}</h1></body></html>".format(site_name, site_name)
        (base_dir / "index.html").write_text(index_html, encoding="utf-8")
        # Optionally add more files from template
        return str(base_dir)

    def automate_task(self, command: str) -> int:
        """Run a shell command for automation purposes and return the subprocess return code."""
        try:
            result = subprocess.run(command, shell=True)
            return result.returncode
        except Exception:
            # On failure to execute the command, return a non-zero code.
            return 1

    def __repr__(self) -> str:
        return f"<CodingAutomationAgent name={self.name}>"
