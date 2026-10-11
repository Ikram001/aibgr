# Background Remover

A free, private background remover that runs **entirely in your browser**.
Open an image, click one button, and the AI cuts out the subject. Then touch up the
edges with a magic wand, colour remover and brushes, and download a transparent PNG
at the **original resolution**.

🚀 **[Try it live here](https://ikram001.github.io/aibgr/)**

## Before & After

| Before | After |
|:---:|:---:|
| ![Before background removal](screenshots/before.jpg) | ![After background removal](screenshots/after.png) |

## 🔒 Privacy-first by design

- **Nothing is uploaded.** No server, no account, no analytics. Your image never leaves the page.
- **Nothing is re-encoded.** The original RGB bytes are kept as they are and only an alpha (transparency) channel is added, so quality is preserved.
- **Fully self-hosted.** The AI model, the ONNX runtime and the font are all inside this repo. The page makes zero third-party requests.

It is a static site: plain HTML, CSS and JavaScript. There is no build step and no dependencies to install.

---

## Features

**Getting an image in**
- Drag and drop, click to browse, paste with `Ctrl+V`, or use **Open image...**
- PNG, JPG and WebP, up to about 32 megapixels

**Removing the background**
- **AI cutout** (`A`): finds the subject automatically using the small U²-Net-P model (4.5 MB), running locally via WebAssembly
- **Sharpen edges after cutout** (on by default): re-fits the AI matte to the photo's real edges with a guided filter, which removes the soft halo a small model leaves around hair and fur. Costs well under a second, even on large photos
- **Optional high-quality mode:** a bigger model (IS-Net, 46 MB) with noticeably cleaner edges. It is *not* included or downloaded by default; see [Optional: high quality model](https://huggingface.co/xrds/isnet-general-onnx-int8)
- **Magic wand** (`W`): click a region to remove all connected pixels of a similar colour
- **Remove color** (`C`): click a colour to remove it everywhere in the image
- **Erase** (`E`) and **Restore** (`R`): paint transparency in or out by hand
- **Tolerance** (0-120) controls wand and colour matching; **Brush size** (3-200) controls the brushes (`[` and `]` to adjust)

**Refining edges** (live and non-destructive: they never change the pixels underneath)
- **Soften** (0-12) feathers the cutout edge
- **Shrink / grow** (-10 to +10) contracts or expands the cutout edge

**Viewing**
- Zoom with the scroll wheel, trackpad pinch, or the `-` / `+` buttons; `F` fits to window, `1` shows 100%
- Pan by holding `Space` and dragging (or middle mouse button)
- Switch the preview backdrop between dark, light and a solid colour
- Hold **Compare** (or `X`) to see the original

**History**
- Undo / redo up to 30 steps (`Ctrl+Z`, `Ctrl+Y`), capped by a memory budget so large images stay safe

**Exporting**
- Formats: PNG (lossless), WebP, JPG (JPG needs a background colour, which is set automatically)
- Background: transparent or a solid colour
- **Trim to content** crops the output to the visible subject
- **Download** the file, or **Copy to clipboard** as PNG

### Keyboard shortcuts

| Key | Action |
|---|---|
| `W` `C` `E` `R` | Magic wand, Remove color, Erase, Restore |
| `A` | Run AI cutout |
| `[` `]` | Smaller / larger brush |
| `Ctrl+Z` / `Ctrl+Y` | Undo / redo |
| `Space` + drag | Pan |
| Scroll | Zoom |
| `F` / `1` | Fit to window / 100% |
| `X` (hold) | Compare with the original |

---

## Setup

### 1. Get the files

Clone or download this repository. It already contains everything, including the model (about 4.4 MB) and the ONNX runtime (about 11 MB). The whole repo is roughly 16 MB.

### 2. Run it locally

The page must be served over `http://`. Opening `index.html` by double-clicking (`file://`) will not work, because browsers block loading the model and WebAssembly from local files.

Use any static server from the repo folder:

```bash
# Python (already installed on most systems)
python -m http.server 8000

# or Node
npx serve .
```

Then open <http://localhost:8000>.

### 3. Publish it

It is a static site, so any static host works.

**GitHub Pages**
1. Push the repo to GitHub (the files are well under the 100 MB per-file limit, so no Git LFS is needed).
2. Go to **Settings, Pages**, choose **Deploy from a branch**, select `main` and `/ (root)`, then save.
3. Your site will be at `https://<username>.github.io/<repo>/`.

**Netlify, Cloudflare Pages, Vercel:** connect the repo, leave the build command empty, and set the output directory to the repo root. Netlify also accepts a drag-and-drop of the folder.

Notes for hosting:
- It works from a sub-path (such as `/<repo>/`), because all asset URLs are relative.
- HTTPS is required in production (for the Cache API and clipboard). `localhost` counts as secure.
- No special headers (COOP/COEP) are needed, because the WebAssembly runtime is configured to use a single thread.
- Your host should serve `.wasm` as `application/wasm`. GitHub Pages, Netlify, Vercel and Cloudflare all do.

### 4. Optional: high quality model

By default the site ships with, and downloads, only the small 4.5 MB model. If you want a higher-quality option, you can add IS-Net (general-use, uint8-quantized, about 46 MB, Apache-2.0). Visitors still download nothing extra unless they pick it.

1. Build the model file (one time):
   ```bash
   pip install onnx onnxruntime
   python tools/make-hq-model.py        # writes vendor/models/isnet-q8.onnx
   ```
   The script downloads the original model from the rembg project, verifies its SHA-256, quantizes it, and cleans up. It needs about 200 MB of temporary disk space.
2. In `index.html`, find `const HQ_MODEL = { enabled: false, ...` and change it to `enabled: true`.
3. Commit `vendor/models/isnet-q8.onnx` (46 MB is under both GitHub's 50 MB warning and its 100 MB hard limit, so no Git LFS is needed) and publish as usual.

A **Quality** selector (Fast / High quality) then appears under the AI button. The high-quality model is downloaded only when someone selects it and runs a cutout, and it is cached in their browser afterwards.

You can also host the file elsewhere (your own storage or CDN) and point `HQ_MODEL.url` at it. In that case the host must send CORS headers.

What to expect from high quality: cleaner, tighter edges and better handling of hair and fine detail, at the cost of time. In my tests (single-threaded WebAssembly, headless Chromium, a modest CPU) one cutout took roughly 13 s of inference, compared with about 2 s for the fast model. The page stays responsive while it runs. Speed depends heavily on the visitor's device.

---

## Project structure

```
background-remover/
├── index.html                 the whole app (HTML, CSS and JS in one file)
├── README.md
├── .nojekyll                  tells GitHub Pages to serve files as-is
└── vendor/
    ├── ort/
    │   ├── ort.min.js                    ONNX Runtime Web 1.19.2
    │   ├── ort-wasm-simd-threaded.mjs    runtime loader
    │   └── ort-wasm-simd-threaded.wasm   runtime (WebAssembly)
    ├── models/
    │   └── u2netp.onnx                   U²-Net-P segmentation model
    │   └── isnet-q8.onnx                 (optional, not included - see "Optional: high quality model")
    ├── fonts/                            JetBrains Mono (woff2) + OFL license
    ├── licenses/Apache-2.0.txt
    └── LICENSES.md                       third-party license notices
└── tools/
    └── make-hq-model.py                  builds the optional high quality model
```

## How it works

1. **Load:** the image is decoded and its original pixels are stored untouched. A separate *mask* (one alpha value per pixel) starts fully opaque.
2. **Edit:** every tool (AI, wand, colour, brushes) changes only the mask. Undo history stores compressed snapshots of the mask.
3. **Edge controls:** Soften and Shrink/grow are applied to the mask at render and export time, so they can be changed or removed at any moment.
4. **Preview:** the visible canvas is the original RGB plus the current mask. Edits to a region only recompute that region, which keeps large images responsive.
5. **AI cutout:** the image is scaled to the model's input size (320x320 for the fast model, 1024x1024 for the optional one) and run through the network with ONNX Runtime Web (WebAssembly, in a background worker so the page stays responsive). The resulting matte is scaled back up and, if "Sharpen edges" is on, refined with a guided filter against the original photo before being written into the mask. You can keep editing it with the other tools.
6. **Export:** the original-resolution pixels plus the final alpha are encoded to PNG, WebP or JPG.

The first AI cutout loads the runtime and the model. The model is stored in the browser's Cache API, so later visits do not download it again.

---

## Browser support

Any current Chrome, Edge, Firefox or Safari with WebAssembly. Copy-to-clipboard needs a browser that supports writing images to the clipboard; if it is blocked, use Download instead.

## Troubleshooting

| Problem | What to check |
|---|---|
| "AI unavailable (offline?)" | Open the browser console (F12). Make sure you are using a local server or HTTPS, not `file://`, and that `vendor/ort/*` and `vendor/models/u2netp.onnx` load without a 404. |
| Everything works except AI, on a custom host | The host may be serving `.wasm` with the wrong MIME type, or blocking large files. |
| A very large image is rejected | The limit is about 32 megapixels. Resize the image first. |
| Edges look soft on large photos | Make sure **Sharpen edges after cutout** is ticked. Then use Shrink / grow and Soften, the Erase and Restore brushes, or enable the optional high quality model. |
| No Quality selector | It is hidden until you set `HQ_MODEL.enabled` to `true` in `index.html` (and add the model file). |
| "Couldn't load the AI model file" | The file for the selected quality is missing or the path is wrong. Check `vendor/models/` and, for the optional model, `HQ_MODEL.url`. |
| Changed the model but still see old results | The model is cached by URL. Give the new file a different name (for example `u2netp-v2.onnx`) and update `MODEL_URLS` in `index.html`. |

## Customising

- **Different model:** models are described in the `AI_MODELS` table in the script section of `index.html` (file, input size, normalisation). Other U²-Net variants with a 320x320 input and the same normalisation drop in; add the file to `vendor/models/` and update the `fast` entry's `urls`.
- **Updating the runtime:** replace all three files in `vendor/ort/` with the same version of `onnxruntime-web` (from the npm package's `dist/` folder). Never mix versions between the `.js` and the `.wasm`.
- **Look and feel:** all styling is in the `<style>` block at the top of `index.html`, driven by CSS variables in `:root`.

## Credits and licenses

Built by Ikram Nizamani.

This repo bundles third-party files, each under its own license: ONNX Runtime Web (MIT), the U²-Net-P model (Apache-2.0) and JetBrains Mono (SIL OFL 1.1). The optional IS-Net model (Apache-2.0) is built from the rembg project's release if you choose to add it. See [`vendor/LICENSES.md`](vendor/LICENSES.md) for details. Add a license for your own code (for example a `LICENSE` file) before publishing.
