import requests
import platform
import os
import sys
import zipfile
import io

# Configuration
TARGET_MILESTONE = "135"
DOWNLOAD_DIR = "./chromium_binaries"
VERSIONS_URL = "googlechromelabs.github.io"


def get_platform_details():
    """Returns platform key for Windows."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    print(machine)
    if system == "windows" and machine in ["amd64", "x86_64"]:
        return "win64"
    elif system == "linux" and machine == "x86_64":
        return "linux64"
    raise ValueError(
        "Unsupported platform: Only Linux 64bit and Windows x86 64bit are supported."
    )


def find_latest_build(milestone):
    """Fetches version info for the given milestone."""
    try:
        response = requests.get(VERSIONS_URL, timeout=30)
        response.raise_for_status()
        for version in reversed(response.json().get("versions", [])):
            if version.get("version", "").startswith(milestone + "."):
                return version
    except Exception as e:
        print(f"Error fetching version data: {e}")
        sys.exit(1)
    print(f"No build found for milestone {milestone}.")
    sys.exit(1)


def download_and_extract(url, download_dir):
    """Downloads and extracts Chromium binaries with progress output."""
    try:
        response = requests.get(url, stream=True, timeout=600)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        block_size = 8192
        os.makedirs(download_dir, exist_ok=True)

        zip_content = io.BytesIO()
        downloaded_size = 0
        print(f"Downloading from url {download_url}...")

        # Download with progress bar
        for chunk in response.iter_content(block_size):
            downloaded_size += len(chunk)
            zip_content.write(chunk)
            done = int(50 * downloaded_size / total_size) if total_size > 0 else 0
            sys.stdout.write(
                f"\r[{'=' * done}{' ' * (50 - done)}] {downloaded_size / (1024 * 1024):.2f} MB"
            )
            sys.stdout.flush()

        print("\nDownload complete. Extracting...")

        # Extracting the archive
        with zipfile.ZipFile(zip_content) as zf:
            zf.extractall(download_dir)
        print(f"Extracted to: {download_dir}")

    except Exception as e:
        print(f"Error during download or extraction: {e}")
        sys.exit(1)


def find_executable(download_dir):
    """Searches for Chromium executable."""
    exec_name = "chrome.exe" if platform.system().lower() == "windows" else "chrome"
    for root, _, files in os.walk(download_dir):
        if exec_name in files:
            return os.path.join(root, exec_name)
    return None


if __name__ == "__main__":
    try:
        # Detect platform
        platform_key = get_platform_details()
        print(f"Platform detected: {platform_key}")

        # Find version and download URL
        version_info = find_latest_build(TARGET_MILESTONE)
        download_url = next(
            (
                d.get("url")
                for d in version_info.get("downloads", {}).get("chrome", [])
                if d.get("platform") == platform_key
            ),
            None,
        )

        if not download_url:
            print("Download URL not found for the platform.")
            sys.exit(1)

        download_and_extract(download_url, DOWNLOAD_DIR)

        executable_path = find_executable(DOWNLOAD_DIR)
        if not executable_path:
            print(f"Executable not found in directory: {DOWNLOAD_DIR}")
            sys.exit(1)

        print(f"Chromium executable ready: {os.path.abspath(executable_path)}")

        if platform.system().lower() == "linux":
            print("Add execution permission to chromium")
            os.chmod(executable_path, 0o755)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
