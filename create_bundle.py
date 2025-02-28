import requests
import base64
import os

f = open("template.js", "r")
TEMPLATE = f.read()
f.close()

DIR = os.path.dirname(os.path.abspath(__file__))
def getFileContents(*relativePath):
	f = open(os.path.join(DIR, "ffmpeg.wasm", "packages", *relativePath), "rb")
	rt = f.read()
	f.close()
	return rt
def generateFromLocal():

	ffmpeg_worker = getFileContents("ffmpeg", "dist", "umd", "814.ffmpeg.js")
	ffmpeg_loader = getFileContents("ffmpeg", "dist", "umd", "ffmpeg.js")
	ffmpeg_core = getFileContents("core", "dist", "umd", "ffmpeg-core.js")
	ffmpeg_wasm = getFileContents("core", "dist", "umd", "ffmpeg-core.wasm")

	f = open(f"bundle.js", "w")
	f.write(
		TEMPLATE.replace("FFMPEG_LOADER", ffmpeg_loader.decode("utf-8"))
		.replace("FFMPEG_CORE", base64.b64encode(ffmpeg_core).decode("ascii"))
		.replace("FFMPEG_WORKER", base64.b64encode(ffmpeg_worker).decode("ascii"))
		.replace("FFMPEG_WASM", base64.b64encode(ffmpeg_wasm).decode("ascii"))
	)
	
	f.close()
def generateFromVersion(version):
	ffmpeg_worker = requests.get(f"https://cdnjs.cloudflare.com/ajax/libs/ffmpeg/{version}/umd/814.ffmpeg.min.js").content
	ffmpeg_loader = requests.get(f"https://cdnjs.cloudflare.com/ajax/libs/ffmpeg/{version}/umd/ffmpeg.min.js").content
	ffmpeg_core = requests.get(f"https://unpkg.com/@ffmpeg/core@{version}/dist/esm/ffmpeg-core.js").content
	ffmpeg_wasm = requests.get(f"https://unpkg.com/@ffmpeg/core@{version}/dist/esm/ffmpeg-core.wasm").content

	f = open(f"{version}.bundle.js", "w")
	f.write(
		TEMPLATE.replace("FFMPEG_LOADER", ffmpeg_loader.decode("utf-8"))
		.replace("FFMPEG_CORE", base64.b64encode(ffmpeg_core).decode("ascii"))
		.replace("FFMPEG_WORKER", base64.b64encode(ffmpeg_worker).decode("ascii"))
		.replace("FFMPEG_WASM", base64.b64encode(ffmpeg_wasm).decode("ascii"))
	)
	
	f.close()
