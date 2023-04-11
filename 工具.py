import os
import urllib
import json
import subprocess
import ctypes
import sys


def getFileSize(path3: str) -> int:
    if not os.path.exists(path3):
        return 0;
    return os.path.getsize(path3);


def getUrlFileSize(url: str) -> int:
    return int(urllib.request.urlopen(url).headers['Content-Length'])


def getGoogleFileSize(id: str) -> int:
    id2: str = "https://drive.google.com/uc?id=" + id
    return getUrlFileSize(id2)


def getKataGoLatestVersion():
    url_ = "https://api.github.com/repos/lightvector/KataGo/releases/latest"
    request_ = urllib.request.urlopen(url_)
    json_ = json.loads(request_.read())
    files = json_["assets"]
    download_url_ = ""
    size = 0
    for file in files:
        if file["name"].endswith("-linux-x64.zip"):
            download_url_ = file["browser_download_url"]
            size = file["size"]
            break

    if getFileSize("./katago") == 0:
        print("Downloading katago.zip...")
        status1 = callShell(f"wget -O /content/katago.zip {download_url_}")
        handle_process(status1, "downloaded katago.zip", "downloading katago.zip", 1)
        chmod()

        if isFileExists("/content/katago.zip") and (not isProcessFailed(1)):
            chmod()
            print("Unzipping katago.zip")
            status2 = callShell("unzip -o /content/katago.zip -d \"/content/\"")
            handle_process(status2, "unzipped katago.zip", "unzipping katago.zip", 2)


def getConfigs():
    if getFileSize("./contribute_example.cfg") == 0:
        print("Downloading contribute_example.cfg...")
        callShell(f"gdown '1pqj2pspklPE3gsZlkJDYs7T0h5dqNQ88&confirm=t' -O ./contribute_example.cfg")
        print("Downloaded contribute_example.cfg successfully.")


def callShell(cmd: str) -> int:
    return subprocess.call(cmd, shell=True)


def unpacking_deb(dir_: str, lib1_path: str, targetDir: str):
    if isFileExists(lib1_path) and (not isProcessFailed(3)):
        callShell(f"mkdir -p {dir_}/extract")
        cmd_1 = f"dpkg -X {lib1_path} {dir_}/extract"
        cmd_2 = f"cp -rf {dir_}/extract/usr/lib/x86_64-linux-gnu/. {targetDir}"
        callShell(f"{cmd_1} && {cmd_2}")
        chmod_file(f"{targetDir}")
        callShell(f"rm -rf {lib1_path}")
        callShell(f"rm -rf {dir_}/extract")


def isProcessFailed(code: int) -> int:
    a = isFileExists(f"/root/byTNTChina/error{code}.txt")
    b = not isFileExists(f"/root/byTNTChina/success{code}.txt")
    return a or b


def check_libnvinfer_so(version: str):
    dir_ = "/root/byTNTChina"
    lib1_path = f"{dir_}/lib1.deb"
    targetPath = "/content/libnvinfer.so.8"
    targetDir = "/content"
    try:
        ctypes.cdll.LoadLibrary(targetPath)
    except OSError as e_1:
        print("Start to download libs...")
        download_libnvinfer_deb(version, lib1_path)
        unpacking_deb(dir_, lib1_path, targetDir)


def download_libnvinfer_deb(version: str, path: str):
    repo = "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64"
    url_ = f"{repo}/libnvinfer8_{version}_amd64.deb"
    isDownloadedFailed = isProcessFailed(3)
    isEqual = getUrlFileSize(url_) == getFileSize(path)
    if isDownloadedFailed and (not isEqual):
        status = callShell(f"wget {url_} -O {path}")
        chmod_file(path)
        handle_process(status, "downloaded lib1.deb", "downloading lib1.deb", 3)


def isFileExists(path4: str) -> bool:
    if os.path.exists(path4):
        if os.path.isfile(path4):
            return True
        else:
            return False
    else:
        return False


def isDirExists(path5: str):
    if os.path.exists(path5):
        if os.path.isdir(path5):
            return True
        else:
            return False
    else:
        return False


def getFileSize(path3: str) -> int:
    if not os.path.exists(path3):
        return 0
    return os.path.getsize(path3)


def chmod():
    callShell("chmod 777 -R .")


def chmod_file(file: str):
    callShell(f"chmod 777 -R {file}")


def handle_process(status: int, smg: str, emg: str, code: int):
    if status == 0:
        print(f"Successfully {smg}.")
        if isFileExists("/root/byTNTChina/error1.txt"):
            callShell(f"rm -rf /root/byTNTChina/error{code}.txt")
        callShell(f"echo '{code}' > /root/byTNTChina/success{code}.txt")
    else:
        print(f"There was an error while {emg}. Please contant with the jupter notebook's author.")
        callShell(f"echo '{code}'> /root/byTNTChina/error{code}.txt")
        sys.exit(1)
