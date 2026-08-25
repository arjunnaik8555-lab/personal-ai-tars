import fnmatch
import os
import subprocess
from typing import Optional


def search_files(query: str, search_path: str = ".") -> str:
    """Searches for files or directories matching a name pattern recursively.
    
    Args:
        query: Filename pattern to search for (e.g. '*.py', 'settings', 'README.md', '*.pdf').
        search_path: Directory path to start searching from (default is current workspace).
    """
    print(f"\n  📂 [TARS Action] Searching files matching '{query}' in '{search_path}'...")
    matches = []
    normalized_path = os.path.expanduser(search_path)

    try:
        for root, dirs, files in os.walk(normalized_path):
            # Skip hidden git or cache directories
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("venv", ".venv", "__pycache__", "node_modules")]
            
            for filename in files:
                if fnmatch.fnmatch(filename.lower(), f"*{query.lower()}*"):
                    full_path = os.path.join(root, filename)
                    matches.append(full_path)
                    if len(matches) >= 30:
                        break
            if len(matches) >= 30:
                break

        if not matches:
            return f"No files found matching '{query}' in {search_path}."

        result_list = "\n".join([f" - {m}" for m in matches])
        return f"Found {len(matches)} matching file(s):\n{result_list}"

    except Exception as e:
        return f"Error searching files: {str(e)}"


def read_file_content(file_path: str, max_lines: int = 200) -> str:
    """Reads and returns the textual content of a file.
    
    Args:
        file_path: Absolute or relative path to the file.
        max_lines: Maximum number of lines to read (default 200).
    """
    print(f"\n  📂 [TARS Action] Reading file: {file_path}...")
    normalized_path = os.path.expanduser(file_path)

    if not os.path.exists(normalized_path):
        return f"Error: File '{file_path}' does not exist."

    if os.path.isdir(normalized_path):
        return f"Error: '{file_path}' is a directory. Use list_directory instead."

    try:
        with open(normalized_path, "r", encoding="utf-8", errors="replace") as f:
            lines = [f.readline() for _ in range(max_lines)]
            content = "".join(lines)
            
            # Check if there were more lines
            has_more = bool(f.readline())

        summary = f"Content of '{file_path}' (first {len(lines)} lines):\n\n{content}"
        if has_more:
            summary += "\n\n... [File truncated for length]"
        return summary

    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"


def write_file_content(file_path: str, content: str, mode: str = "write") -> str:
    """Creates a new file or appends content to an existing file.
    
    Args:
        file_path: Path where the file will be saved.
        content: The text content to write into the file.
        mode: 'write' to overwrite/create new, or 'append' to add to existing file.
    """
    print(f"\n  📂 [TARS Action] Writing to file: {file_path} (mode: {mode})...")
    normalized_path = os.path.expanduser(file_path)

    try:
        os.makedirs(os.path.dirname(os.path.abspath(normalized_path)), exist_ok=True)
        file_mode = "a" if mode == "append" else "w"
        
        with open(normalized_path, file_mode, encoding="utf-8") as f:
            f.write(content)

        return f"Successfully saved content to '{file_path}' ({len(content)} characters written)."

    except Exception as e:
        return f"Error writing to file '{file_path}': {str(e)}"


def list_directory(directory_path: str = ".") -> str:
    """Lists files and folders inside a given directory path.
    
    Args:
        directory_path: Directory path to inspect (defaults to current folder).
    """
    print(f"\n  📂 [TARS Action] Listing directory: {directory_path}...")
    normalized_path = os.path.expanduser(directory_path)

    if not os.path.exists(normalized_path):
        return f"Directory '{directory_path}' does not exist."

    try:
        entries = os.listdir(normalized_path)
        folders = []
        files = []

        for entry in sorted(entries):
            if entry.startswith("."):
                continue
            full = os.path.join(normalized_path, entry)
            if os.path.isdir(full):
                folders.append(f" 📁 {entry}/")
            else:
                size_kb = os.path.getsize(full) / 1024
                files.append(f" 📄 {entry} ({size_kb:.1f} KB)")

        output = [f"Contents of '{directory_path}':"]
        output.extend(folders)
        output.extend(files)
        return "\n".join(output)

    except Exception as e:
        return f"Error listing directory '{directory_path}': {str(e)}"


def run_terminal_command(command: str) -> str:
    """Runs a shell command on the local machine and returns the stdout/stderr output.
    
    Args:
        command: The terminal command to execute (e.g. 'git status', 'python --version', 'ls -la').
    """
    print(f"\n  💻 [TARS Action] Executing shell command: `{command}`...")
    try:
        res = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=20,
            check=False
        )
        
        output = []
        if res.stdout.strip():
            output.append(f"Output:\n{res.stdout.strip()}")
        if res.stderr.strip():
            output.append(f"Errors/Warnings:\n{res.stderr.strip()}")
        if not output:
            output.append("Command executed successfully with no output.")
            
        output.append(f"(Exit code: {res.returncode})")
        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return f"Command `{command}` timed out after 20 seconds."
    except Exception as e:
        return f"Failed to execute command `{command}`: {str(e)}"
