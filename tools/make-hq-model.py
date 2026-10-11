#!/usr/bin/env python3
"""Builds the OPTIONAL high-quality model: IS-Net general-use, uint8-quantized (~46 MB).

The site works without it (it ships with the small 4.5 MB model only). Run this once,
then follow README -> "Optional: high quality model" to switch it on.

    pip install onnx onnxruntime
    python tools/make-hq-model.py            # writes vendor/models/isnet-q8.onnx
    python tools/make-hq-model.py out.onnx   # or write somewhere else

Downloads the original 170 MB model from the rembg project's GitHub release, checks its
SHA-256, quantizes it, and deletes the download. IS-Net / DIS is Apache-2.0.
"""
import hashlib, os, sys, tempfile, urllib.request
from pathlib import Path

URL = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-general-use.onnx"
SHA256 = "60920e99c45464f2ba57bee2ad08c919a52bbf852739e96947fbb4358c0d964a"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "vendor" / "models" / "isnet-q8.onnx"

def main():
    try:
        from onnxruntime.quantization import quantize_dynamic, QuantType
    except ImportError:
        sys.exit("Missing dependencies. Run:  pip install onnx onnxruntime")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "isnet-general-use.onnx")
        print("Downloading", URL)
        urllib.request.urlretrieve(URL, src)
        digest = hashlib.sha256(open(src, "rb").read()).hexdigest()
        if digest != SHA256:
            sys.exit(f"Checksum mismatch (got {digest}). Refusing to continue.")
        print("Checksum OK. Quantizing to uint8 ...")
        quantize_dynamic(src, str(OUT), weight_type=QuantType.QUInt8)
    print(f"Done: {OUT}  ({OUT.stat().st_size / 1048576:.1f} MB)")

if __name__ == "__main__":
    main()
