# The FFmepg-Wasm bundler

A quick and hacky way to bundle [ffmpeg.wasm](https://github.com/ffmpegwasm/ffmpeg.wasm/) into a single .js file, allowing for it to be used in offline enviroments, and when CORS is an issue.


## Usage
See the [releases page](https://github.com/HeronErin/FFmpeg-bundler/releases) for pre-compiled bundles, and link to it on your own site. To create an FFmpeg object call the global function `create_ffmpeg`. 

Ex:
```js
	let ff = await createFFmpeg();
	console.log(await ffmpeg.listDir(".")); //> [{"name":".","isDir":true},{"name":"..","isDir":true},{"name":"tmp","isDir":true},{"name":"home","isDir":true},{"name":"dev","isDir":true},{"name":"proc","isDir":true}]
```


## Building
You also might (for security reasons) wish to build to bundles yourself. Heres how:

1. Clone the repo
```bash
git clone --recurse-submodules https://github.com/HeronErin/FFmpeg-bundler.git
```
2. Install the python dep
```bash
pip install requests
```
3. Run the script
```bash
python create_bundle.py
```

Optionally, if you also wish to build ffmpeg-wasm yourself, and create a bundle. See the instructions [here](https://ffmpegwasm.netlify.app/docs/contribution/core/):
```bash
make prd
npm install
npm run build
```
If the ffmpeg.wasm is compiled, then the create_bundle script will detect that an bundle it for you.
