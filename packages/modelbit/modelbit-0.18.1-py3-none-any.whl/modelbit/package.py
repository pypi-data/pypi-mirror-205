#!/usr/bin/env python3

import hashlib
import logging
import os
import re
import shutil
import stat
import tarfile
import tempfile
from contextlib import contextmanager
from typing import Dict, Iterator, List, Optional, Tuple, Union

import build
import build.env
import build.util
import pkginfo

from .ux import printTemplate

from .cli.api import MbApi
from .cli.login import loginAndPickWorkspace
from .utils import timeago
from .helpers import isAuthenticated, performLogin, runtimeAuthInfo

logger = logging.getLogger(__name__)


class PackageInfo:
  name: str
  version: str

  def __init__(self, name: str, version: str):
    self.name = name
    self.version = version

  def __repr__(self):
    return f"{self.name}=={self.version}"


class PackageDescResponse:
  name: Optional[str] = None
  version: Optional[str] = None
  createdAtMs: Optional[int] = None
  size: Optional[int] = None

  def __init__(self, data: Dict[str, str]):
    if "name" in data:
      self.name = data['name']
    if "version" in data:
      self.version = data['version']
    if "createdAtMs" in data:
      self.createdAtMs = int(data['createdAtMs'])
    if "size" in data:
      self.size = int(data['size'])

  def __repr__(self):
    return f"{self.name}=={self.version}"


def auth_and_add_package(path: str, force: bool = False):
  if not isAuthenticated():
    performLogin(refreshAuth=True)
    if not isAuthenticated():
      return None
  return add_package(path, force, MbApi(*runtimeAuthInfo()))


def auth_and_delete_package(name: str, version: str):
  if not isAuthenticated():
    performLogin(refreshAuth=True)
    if not isAuthenticated():
      return None
  return delete_package(name, version, MbApi(*runtimeAuthInfo()))


def auth_and_list_package(name: Optional[str]):
  if not isAuthenticated():
    performLogin(refreshAuth=True)
    if not isAuthenticated():
      return None
  return PackageApi(MbApi(*runtimeAuthInfo())).fetchPackageList(name)


def add_package(path: str, force: bool = False, api: Optional[MbApi] = None) -> Optional[PackageInfo]:
  try:
    builder = PackageBuilder(api)
    pkgKind, pkgInfo = builder.packageInfo(path)
    printTemplate("package-uploading",
                  None,
                  pkgInfo=pkgInfo,
                  path=os.path.abspath(path),
                  isBuilding=pkgKind != "wheel")
    pkgInfo = builder.uploadPackage(path, force, (pkgKind, pkgInfo))
    printTemplate("package-uploaded", None, pkgInfo=pkgInfo)
    return pkgInfo
  except Exception as e:
    printTemplate("error", None, errorText=f"Error uploading package: {str(e)}")
    return None


def delete_package(name: str, version: str, api: Optional[MbApi] = None) -> Optional[PackageDescResponse]:
  if "==" in name and not version:
    name, version = name.split("==")
  try:
    resp = PackageApi(api).deletePackage(name, version)
    if resp is None:
      raise Exception(f"Package {name}=={version} not found")
    printTemplate("package-deleted", None, name=name, version=version)
    return resp
  except Exception as e:
    printTemplate("error", None, errorText=f"Error deleting package: {str(e)}")
  return None


class PackageApi:
  api: MbApi

  def __init__(self, api: Optional[MbApi] = None):
    if api is None:
      api = MbApi()
      loginAndPickWorkspace(api, source="package")
    self.api = api

  def fetchPackageDesc(self, name: str, version: Optional[str]) -> Optional[PackageDescResponse]:
    name = normalizePkgName(name)
    resp = self.api.getJson("api/cli/v1/package/info", {"name": name, "pkgversion": version})
    error = resp.get("errorMsg", None)
    if error is not None:
      raise Exception(error)
    pkgResp = resp.get("package", None)
    pkgDesc = PackageDescResponse(pkgResp) if pkgResp is not None else None
    if pkgDesc:
      logger.info("Found package name=%s version=%s", pkgDesc.name, pkgDesc.version)
    else:
      logger.info("No package, searching for name=%s, version=%s", name, version)
    return pkgDesc

  def fetchPackageList(self, name: Optional[str]) -> List[PackageDescResponse]:
    resp = self.api.getJson("api/cli/v1/package/list_all", {"name": name})
    error = resp.get("errorMsg", None)
    if error is not None:
      raise Exception(error)
    return [PackageDescResponse(pkgResp) for pkgResp in resp.get("packages", [])]

  def deletePackage(self, name: str, version: str) -> Optional[PackageDescResponse]:
    resp = self.api.getJson("api/cli/v1/package/delete", {"name": name, "pkgversion": version})
    error = resp.get("errorMsg", None)
    if error is not None:
      raise Exception(error)
    pkgResp = resp.get("package", None)
    return PackageDescResponse(pkgResp) if pkgResp is not None else None

  def uploadWheel(self, name: str, version: str, wheelPath: str, allowClobberVersions: bool) -> None:
    name = normalizePkgName(name)

    with open(wheelPath, 'rb') as f:
      data = f.read()
      contentHash = f"sha1:{hashlib.sha1(data).hexdigest()}"
      self.api.uploadFile(
          f"api/cli/v1/package/upload_wheel", {os.path.basename(wheelPath): data},
          dict(name=name,
               version=version,
               contentHash=contentHash,
               allowClobberVersions=str(allowClobberVersions).lower()))


class PackageBuilder:
  api: PackageApi

  def __init__(self, api: Optional[MbApi] = None):
    self.api = PackageApi(api)

  def packageInfo(self, path: str) -> Tuple[str, PackageInfo]:
    stat_res = os.stat(path)
    if stat.S_ISDIR(stat_res.st_mode):
      pkgInfo = _pkgMetadata(path)
      if pkgInfo:
        return "packagedir", pkgInfo
      else:
        pkgName = normalizePkgName(os.path.basename(os.path.abspath(path)))
        pkgInfo = self._fetchNextPackageVersion(pkgName)
        if pkgInfo is None:
          raise Exception("Unable to create package")
        return "rawdir", pkgInfo
    elif _pathIsSDist(path):
      sDistInfo = pkginfo.SDist(path)
      return "sdist", PackageInfo(name=sDistInfo.name, version=sDistInfo.version)
    elif _pathIsWheel(path):
      wheelInfo = pkginfo.Wheel(path)
      return "wheel", PackageInfo(name=wheelInfo.name, version=wheelInfo.version)
    else:
      raise Exception(f"Unknown filetype {os.path.splitext(path)[-1]}")

  def uploadPackage(self,
                    path: str,
                    allowClobberVersions: bool,
                    pkgKindInfo: Optional[Tuple[str, PackageInfo]] = None) -> PackageInfo:
    wheelPath: str
    pkgKind, pkgInfo = pkgKindInfo or self.packageInfo(path)

    self._validatePackageInfo(pkgInfo, allowClobberVersions)
    if pkgKind == "packagedir":
      wheelPath = _buildViaSdist(path)
    elif pkgKind == "sdist":
      wheelPath = _buildViaSdist(path)  # Convert sdist to wheel
    elif pkgKind == "wheel":
      wheelPath = path
    elif pkgKind == "rawdir":
      with _temporaryProjectFolder(path, pkgInfo) as path:
        wheelPath = _buildViaSdist(path)
    else:
      raise Exception("Unknown package kind")

    self.api.uploadWheel(pkgInfo.name, pkgInfo.version, wheelPath, allowClobberVersions)
    return pkgInfo

  def _validatePackageInfo(self, pkgInfo: PackageInfo, allowClobberVersions: bool) -> None:
    fetchedPkgDesc = self.api.fetchPackageDesc(pkgInfo.name, pkgInfo.version)
    if fetchedPkgDesc is None or allowClobberVersions:
      return
    raise Exception(
        f"Package {fetchedPkgDesc.name}=={fetchedPkgDesc.version} already uploaded {timeago(fetchedPkgDesc.createdAtMs or 0)}"
    )

  def _fetchNextPackageVersion(self, name: str) -> Optional[PackageInfo]:
    pkgInfo = self.api.fetchPackageDesc(name, None)
    nextVersion = _nextSemVer(pkgInfo.version) if pkgInfo is not None and pkgInfo.version else "0.0.1"
    if nextVersion is None:
      return None
    return PackageInfo(name=name, version=nextVersion)


def _pkgMetadata(path: str) -> Optional[PackageInfo]:
  try:
    metadata = build.util.project_wheel_metadata(path)
    return PackageInfo(name=metadata["Name"], version=metadata["Version"])
  except build.BuildException:
    return None


def _genSetupPy(pkgInfo: PackageInfo) -> str:
  return f"""from setuptools import setup, find_packages
setup(
    name='{pkgInfo.name}',
    version='{pkgInfo.version}',
    packages=find_packages(),
)"""


# # This cannot be used until we deprecate python3.6 but it is the future
# def _genProjectToml(pkgInfo: PackageInfo) -> str:
#   return f"""[project]
# name = "{pkgInfo.name}"
# version = "{pkgInfo.version}"
# """


# Copies the project into a properly named sub-folder so pip will install properly
# Create a temporary project setupPy so we can set the version and name
# Creates an __init__.py it none exists as it's required for a project
# Without these, you cannot import files the same as you do in a notebook
@contextmanager
def _temporaryProjectFolder(path: str, pkgInfo: PackageInfo) -> Iterator[str]:
  tmpdir = tempfile.mkdtemp('modelbit')
  try:
    pkgdir = os.path.join(tmpdir, pkgInfo.name)
    initPyPath = os.path.join(pkgdir, "__init__.py")
    shutil.copytree(path, pkgdir)

    logger.info("Not a python project, creating temporary setup.py")
    setupPyPath = os.path.join(tmpdir, "setup.py")
    handle = os.open(setupPyPath, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(handle, 'w') as file_obj:
      file_obj.write(_genSetupPy(pkgInfo))
    if not os.path.exists(initPyPath):
      open(initPyPath, "w").close()
    yield tmpdir
  finally:
    shutil.rmtree(tmpdir)


# We build via sdist to ensure the wheel is built clean
def _buildViaSdist(path: str) -> str:
  shouldDeleteSdist = False
  if path.endswith(".tar.gz"):  # Is sdist
    sdist = path
  else:
    sdist = _build(path, "sdist")  # Build the sdist
    shouldDeleteSdist = True
  sdist_name = os.path.basename(sdist)
  sdist_out = tempfile.mkdtemp(prefix='build-via-sdist-')
  with tarfile.open(sdist) as t:
    t.extractall(sdist_out)
    try:
      return _build(os.path.join(sdist_out, sdist_name[:-len('.tar.gz')]), "wheel")
    finally:
      shutil.rmtree(sdist_out, ignore_errors=True)
      if shouldDeleteSdist:
        os.unlink(sdist)


def _build(path: str, kind: str) -> str:
  outdir = os.path.join(tempfile.gettempdir(), 'modelbit')
  with build.env.IsolatedEnvBuilder() as env:
    builder = build.ProjectBuilder(path, python_executable=env.executable, scripts_dir=env.scripts_dir)
    # first install the build dependencies
    env.install(builder.build_system_requires)
    # then get the extra required dependencies from the backend
    env.install(builder.get_requires_for_build(kind))
    return builder.build(kind, outdir, {})


simpleSemVer = re.compile(
    r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
)
onlyNumbers = re.compile('[^0-9]+')


def _nextSemVer(version: str) -> Optional[str]:
  m = simpleSemVer.match(version)
  if not m:
    return None
  parts = [int(onlyNumbers.sub("", v)) for v in m.groups() if v is not None]
  parts[-1] += 1
  return ".".join(str(p) for p in parts)


def _pathIsSDist(path: str) -> bool:
  return path.endswith(".tar.gz")


def _pathIsWheel(path: str) -> bool:
  return path.endswith(".whl")


def normalizePkgName(name):
  return re.sub(r"[-_.]+", "-", name).lower()
