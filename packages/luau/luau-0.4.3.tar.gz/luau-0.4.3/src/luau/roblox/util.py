import os
import sys
import subprocess
from pkg_resources import resource_filename
from importlib import resources

def get_instance_from_path(path: str) -> str:
	
	roblox_path_keys = path.split("/")

	roblox_path = ""

	for i, key in enumerate(roblox_path_keys):
		if i == 0:
			roblox_path += key
		else:
			roblox_path += f":WaitForChild(\"{key}\")"

	for service in ["ReplicatedStorage", "ServerStorage", "ServerScriptService", "ReplicatedFirst", "Lighting", "StarterGui", "StarterPlayer", "Workspace"]:
		roblox_path = roblox_path.replace(f"game:WaitForChild(\"{service}\")", f"game:GetService(\"{service}\")")

	return roblox_path

def run_bundled_exe(exe_name: str, args: list[str]=[]):
	def resource_path(relative_path: str) -> str:
		try:
			# PyInstaller creates a temp folder and stores path in _MEIPASS
			base_path = sys._MEIPASS
		except Exception:
			base_path = os.path.abspath(".")

		return os.path.join(base_path, relative_path)
	exe_path = resource_path(resources.path('luau', f'{exe_name}.exe'))
	subprocess.run([exe_path] + args)

def get_module_require(path: str):
	return f"require({get_instance_from_path(path)})"

def get_header_module(path: str, variable_name: str = ""):
	if variable_name == "":
		keys = path.split("/")
		variable_name = keys[len(keys)-1]

	value = get_module_require(path)

	return f"local {variable_name} = {value}"
