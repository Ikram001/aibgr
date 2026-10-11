# Third-party components

This project redistributes the files below. Each keeps its own license.

| Component | Files | License | Source |
|---|---|---|---|
| ONNX Runtime Web 1.19.2 | `vendor/ort/*` | MIT | https://github.com/microsoft/onnxruntime |
| U²-Net-P (`u2netp`) model | `vendor/models/u2netp.onnx` | Apache-2.0 | https://github.com/xuebinqin/U-2-Net |
| IS-Net general-use (OPTIONAL, not bundled) | `vendor/models/isnet-q8.onnx` if you add it | Apache-2.0 | https://github.com/xuebinqin/DIS |
| JetBrains Mono (latin subset) | `vendor/fonts/*.woff2` | SIL OFL 1.1 | https://github.com/JetBrains/JetBrainsMono |

The ONNX export of `u2netp` was obtained from the release assets of the
rembg project (https://github.com/danielgatis/rembg, MIT):
`https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2netp.onnx`
(4,574,861 bytes, SHA-256 `309c8469258dda742793dce0ebea8e6dd393174f89934733ecc8b14c76f4ddd8`).
The optional IS-Net model (Qin et al., "Highly Accurate Dichotomous Image Segmentation") is not included in this repo. `tools/make-hq-model.py` builds it from the rembg release `isnet-general-use.onnx`; if you publish that file, the same Apache-2.0 terms (`vendor/licenses/Apache-2.0.txt`) apply to it.
The font files come from the `@fontsource/jetbrains-mono` npm package (5.3.0).

## ONNX Runtime Web - MIT

Copyright (c) Microsoft Corporation

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## U²-Net - Apache License 2.0

Copyright (c) Xuebin Qin and contributors. Licensed under the Apache License,
Version 2.0. The full license text is in `vendor/licenses/Apache-2.0.txt`.

## JetBrains Mono - SIL Open Font License 1.1

Copyright 2020 The JetBrains Mono Project Authors. The full license text is in
`vendor/fonts/OFL.txt`.
