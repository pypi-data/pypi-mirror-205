import sys
import json
import subprocess
import urllib.request
import argparse
import distro
import toml


def get_linux_distribution():
    return distro.id()


def update_pip_packages() -> None:
    print("Checking for pip updates...")

    pip_version = subprocess.check_output(
        [sys.executable, "-m", "pip", "--version"]).decode().split()[1]

    with urllib.request.urlopen("https://pypi.org/pypi/pip/json") as response:
        pip_latest_version = json.load(response)["info"]["version"]

    if pip_version != pip_latest_version:
        print(
            f"Updating pip from version {pip_version} to version {pip_latest_version}...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("Pip updated successfully.")
    else:
        print(f"Pip is already up-to-date (version {pip_version}).")

    print("Checking for available pip package updates...")
    outdated_packages = subprocess.check_output(
        [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"]).decode()
    packages_to_update = [pkg["name"] for pkg in json.loads(outdated_packages)]

    if not packages_to_update:
        print("All pip packages are up-to-date.")
    else:
        print("Updating pip packages...")
        for package in packages_to_update:
            update_result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", package])
            if update_result.returncode == 0:
                print(f"{package} updated successfully.")
            else:
                print(
                    f"Error updating {package}. Return code: {update_result.returncode}")
        print("Pip packages update completed.")


def update_apt_packages() -> None:
    print("Updating apt packages...")
    apt_update_result = subprocess.run(["sudo", "apt", "update"])
    if apt_update_result.returncode == 0:
        print("Apt update completed successfully.")
    else:
        print(
            f"Apt update completed with errors. Return code: {apt_update_result.returncode}")

    apt_upgrade_result = subprocess.run(["sudo", "apt", "upgrade", "-y"])
    if apt_upgrade_result.returncode == 0:
        print("Apt packages updated successfully.")
    else:
        print(
            f"Apt packages update completed with errors. Return code: {apt_upgrade_result.returncode}")


def update_yum_packages() -> None:
    print("Updating YUM packages...")
    yum_update_result = subprocess.run(["sudo", "yum", "update", "-y"])
    if yum_update_result.returncode == 0:
        print("YUM packages updated successfully.")
    else:
        print(
            f"YUM packages update completed with errors. Return code: {yum_update_result.returncode}")


def update_dnf_packages() -> None:
    print("Updating DNF packages...")
    dnf_update_result = subprocess.run(["sudo", "dnf", "upgrade", "-y"])
    if dnf_update_result.returncode == 0:
        print("DNF packages updated successfully.")
    else:
        print(
            f"DNF packages update completed with errors. Return code: {dnf_update_result.returncode}")


def update_pacman_packages() -> None:
    print("Updating Pacman packages...")
    pacman_update_result = subprocess.run(
        ["sudo", "pacman", "-Syu", "--noconfirm"])
    if pacman_update_result.returncode == 0:
        print("Pacman packages updated successfully.")
    else:
        print(
            f"Pacman packages update completed with errors. Return code: {pacman_update_result.returncode}")


def update_zypper_packages() -> None:
    print("Updating Zypper packages...")
    zypper_update_result = subprocess.run(["sudo", "zypper", "refresh"])
    if zypper_update_result.returncode == 0:
        print("Zypper repositories refreshed successfully.")
    else:
        print(
            f"Zypper repositories refresh completed with errors. Return code: {zypper_update_result.returncode}")

    zypper_upgrade_result = subprocess.run(["sudo", "zypper", "update", "-y"])
    if zypper_upgrade_result.returncode == 0:
        print("Zypper packages updated successfully.")
    else:
        print(
            f"Zypper packages update completed with errors. Return code: {zypper_upgrade_result.returncode}")


def update_app_packages() -> None:
    distro_id = get_linux_distribution()

    if distro_id.lower() in ("ubuntu", "debian"):
        update_apt_packages()
    elif distro_id.lower() in ("fedora"):
        update_dnf_packages()
    elif distro_id.lower() in ("centos", "redhat"):
        update_yum_packages()
    elif distro_id.lower() in ("arch", "manjaro"):
        update_pacman_packages()
    elif distro_id.lower() in ("opensuse", "suse"):
        update_zypper_packages()
    else:
        print(
            f"Unsupported distribution: {distro_id}. Cannot update packages.")


def get_version_from_pyproject_toml() -> str:
    with open("pyproject.toml") as f:
        pyproject_toml = toml.load(f)
    return pyproject_toml["tool"]["poetry"]["version"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Update pip and app packages")
    parser.add_argument('--pip', action='store_true',
                        help='Update pip packages')
    parser.add_argument('--app', action='store_true',
                        help='Update app packages')
    parser.add_argument('-v', '--version', action='store_true',
                        help='Display the version of the package')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.version:
        version = get_version_from_pyproject_toml()
        print(f"update-pip-packages version: {version}")
        sys.exit(0)

    if args.pip:
        update_pip_packages()
    if args.app:
        update_app_packages()


if __name__ == "__main__":
    main()
