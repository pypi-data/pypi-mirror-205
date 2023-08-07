import os
import shutil
import zipfile
from .util import run_bundled_exe, get_module_require

def format(path: str):
	run_bundled_exe(exe_name="py_luau_stylua.exe", args=[path])

def get_package_require(package_name: str) -> str:
	return get_module_require(f"script/{package_name}")

def write_script(build_path: str, content: str, write_as_directory: bool=False, packages_dir_zip_file_path: str | None = None):

	if packages_dir_zip_file_path != None:
		write_as_directory = True

	dir_name, file_name = os.path.split(build_path)
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
	elif os.path.exists(build_path):
		os.remove(build_path)

	if write_as_directory:
		full_dir_path = build_path.split(".")[0]
		full_ext = ".".join(build_path.split(".")[1:])
		final_dir_path = (dir_name+"/"+file_name).replace(full_ext, "")
		
		if os.path.exists(final_dir_path):
			shutil.rmtree(final_dir_path)

		os.makedirs(final_dir_path)
		init_file_path = final_dir_path+"/init."+full_ext
		out_file = open(init_file_path, "w")
		out_file.write(content)
		out_file.close()
		format(init_file_path)

		zip_ref = zipfile.ZipFile(packages_dir_zip_file_path, 'r')
		zip_ref.extractall(final_dir_path)
		zip_ref.close()

	else:
		out_file = open(build_path, "w")
		out_file.write(content)
		out_file.close()
		format(build_path)
