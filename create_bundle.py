import requests
import base64
import os, sys

from concurrent.futures import ThreadPoolExecutor


DIR = os.path.dirname(os.path.abspath(__file__))

f = open(os.path.join(DIR, "template.js"), "r")
TEMPLATE = f.read()
f.close()


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

	f = open(os.path.join(DIR, "out", "bundle.js"), "w")
	f.write(
		TEMPLATE.replace("FFMPEG_LOADER", ffmpeg_loader.decode("utf-8"))
		.replace("FFMPEG_CORE", base64.b64encode(ffmpeg_core).decode("ascii"))
		.replace("FFMPEG_WORKER", base64.b64encode(ffmpeg_worker).decode("ascii"))
		.replace("FFMPEG_WASM", base64.b64encode(ffmpeg_wasm).decode("ascii"))
	)
	
	f.close()
def generateFromVersion(version):
	urls = [
		f"https://cdnjs.cloudflare.com/ajax/libs/ffmpeg/{version}/umd/814.ffmpeg.min.js",
		f"https://cdnjs.cloudflare.com/ajax/libs/ffmpeg/{version}/umd/ffmpeg.min.js",
		f"https://unpkg.com/@ffmpeg/core@{version}/dist/esm/ffmpeg-core.js",
		f"https://unpkg.com/@ffmpeg/core@{version}/dist/esm/ffmpeg-core.wasm"
	]


	exe = ThreadPoolExecutor()
	reqs = list(exe.map(requests.get, urls))
	
	for r in reqs:
		if r.status_code != 200:
			raise ValueError(f"{r.url} returned with code {r.status_code}")
	

	ffmpeg_worker, ffmpeg_loader, ffmpeg_core, ffmpeg_wasm = list(
		map( 
			lambda x: x.content,
			reqs
		)
	)

	f = open(os.path.join(DIR, "out", f"{version}.bundle.js"), "w")
	f.write(
		TEMPLATE.replace("FFMPEG_LOADER", ffmpeg_loader.decode("utf-8"))
		.replace("FFMPEG_CORE", base64.b64encode(ffmpeg_core).decode("ascii"))
		.replace("FFMPEG_WORKER", base64.b64encode(ffmpeg_worker).decode("ascii"))
		.replace("FFMPEG_WASM", base64.b64encode(ffmpeg_wasm).decode("ascii"))
	)
	
	f.close()
def onlineGen(v):
	try:
		generateFromVersion(v)
		print(f"Online bundle generated for {v}")
	except Exception as e:
		print(f"Error: Unable to generate bundle from online version {v}: {e}")

def main():
	try:
		generateFromLocal()
		print("Local bundle generated!")
	except Exception as e:
		print("Error: Unable to generate bundle from local: " + e)
	with ThreadPoolExecutor() as e:
		for v in requests.get("https://api.cdnjs.com/libraries/ffmpeg?fields=versions").json()["versions"]:
			# This wont work with older versions
			if v.split(".")[1] != "12":
				continue
			e.submit(onlineGen, v)

if __name__ == "__main__":
	main()