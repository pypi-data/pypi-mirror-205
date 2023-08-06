
import os
import setuptools


def walk(path, ext):
	files = []
	for dirpath, dirnames, filenames in os.walk(path):
		for filename in filenames:
			if os.path.splitext(filename)[1] in ext:
				files.append(os.path.join(dirpath, filename))
	return files

def sources(path): return walk(path, [".cpp"])
def headers(path): return walk(path, [".h"])


MODULES = {
	"lzss": ["src/module_lzss.cpp"],
	"gx2": [
		"src/module_gx2.cpp",
		"src/type_surface.cpp",
		*sources("src/addrlib"),
		*sources("src/gx2")
	],
	"endian": ["src/module_endian.cpp"],
	"yaz0": ["src/module_yaz0.cpp"],
	"audio": [
		"src/module_audio.cpp",
		*sources("src/dsptool")
	]
}

description = \
	"C++ extension with functions for which python is too slow."

long_description = description

extensions = []
for name, files in MODULES.items():
	extension = setuptools.Extension(
		name = "ninty.%s" %name,
		sources = files,
		include_dirs = ["src", "src/addrlib"]
	)
	extensions.append(extension)

setuptools.setup(
	name = "ninty",
	version = "0.0.11",
	description = description,
	long_description = long_description,
	author = "Yannik Marchand",
	author_email = "ymarchand@me.com",
	url = "https://github.com/kinnay/ninty",
	license = "GPLv3",
	ext_modules = extensions,
	package_data = {"": headers("src")}
)
