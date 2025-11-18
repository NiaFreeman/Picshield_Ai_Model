# PicShield (Privacy-first image safety)

PicShield is a privacy-first demo that detects potential sensitive data exposure in images using client-side models and local processing. This repository contains training notebooks and a browser-based demo (phone-like UI) that runs inference with TensorFlow.js models under `webapp/public/models/`.

Key goals and constraints
- On-device / local-first processing: the web demo performs inference in the browser using TF.js and does not upload your images by default.
- No automatic cloning or external telemetry: the notebooks and demo no longer include automatic git cloning or external-hosted badges that reference third-party repos or services.
- Explicit consent for any cloud operation: uploads or telemetry require explicit, per-action consent from the user (see the Privacy Center in the demo).

## Quick demo (browser)
Run the phone-like UI locally and open it in your browser. Serving over HTTP(S) is required so model files load correctly (file:// will block model XHRs):

```powershell
cd webapp/public
python -m http.server 8000
# open http://localhost:8000 in your browser
```

The demo HTML is `webapp/public/index.html`. Models used by the demo are in `webapp/public/models/` (TF.js converted artifacts). The demo contains a simple encrypted "Hidden" folder implementation for demonstration — for production Android you should use the Android Keystore + BiometricPrompt (see `docs/android_keystore.md`).

## Notebooks & training
- `Image_Classification.ipynb` and `Text_Classification.ipynb` contain training code and are intended to be run in a Python environment. All commands are designed to run in local environments with standard Python/Jupyter setups.

## Privacy & security notes
- Do not commit secrets (API keys, Firebase service files) to the repo. This project includes a placeholder `.firebaserc`; do not deploy to a public Firebase project without creating your own project and replacing the placeholder.
- The web demo's IndexedDB + WebCrypto AES-GCM storage is for demonstration. For production-grade storage on mobile, use platform-provided key stores and biometric gating.

## Spicy image guidelines

- **Legal & consent:** Only include images that are explicitly adult (18+) and that you have permission to use. Do not include any images of minors or content that would be illegal in your jurisdiction. I will not assist with content involving minors or illegal material.
- **Privacy:** Remove or anonymize any metadata (EXIF, geolocation) before sharing or committing datasets. Use `exiftool` or similar to strip metadata.
- **Storage:** Large or sensitive images should not be committed directly to a public Git repository. Use Git LFS, private storage (S3, Google Drive), or keep them outside the repo and add a small manifest (see below).
- **Labeling & split:** Keep labeled folders or a manifest file that maps image paths to labels (e.g., `nsfw`, `safe`, `suggestive`). Keep a reproducible train/val/test split (store the split indices/CSV in the dataset folder).
- **Demo examples:** The demo includes example images in `webapp/public/assets/images/examples/`. To add spicy demo examples, place (or copy) up to three representative adult-only images there named `spicy_example_1.jpg`, `spicy_example_2.jpg`, and `spicy_example_3.jpg`. The repo contains a helper script `scripts/resize_spicy_samples.py` to resize and copy images from an external samples folder into the demo folder.

Example: copy + resize using the included script (run from repo root):
```powershell
python scripts\resize_spicy_samples.py \
	--src "C:\Users\Shado\Downloads\Spicy_Ai\Spicy_Ai_Training\samples" \
	--dest "webapp/public/assets/images/examples" \
	--count 3
```

The script creates demo-sized images (512px) and training-sized images (224px) under `webapp/public/assets/images/examples/train/`.

## Project structure (relevant)
- `webapp/public/` — demo HTML/CSS/JS and TF.js models
- `dataset/` — image dataset used for training and validation
- `text_dataset/` — JSON datasets for text classification
- `models/` — original keras h5 models (if present)
- `docs/` — guidance for production hardening (Android Keystore, etc.)

## How to visually see it work (VS Code Live Server)
If you prefer to use VS Code and the Live Server extension to preview the phone UI, follow these steps.

1. Get the Live Server extension
	- In VS Code open the Extensions view (left sidebar) and install "Live Server" by Ritwick Dey.

2. Open the demo folder
	- In VS Code open the folder `webapp/public` (you can open the repo root and then expand `webapp/public`).

3. Launch Live Server
	- Right-click `index.html` in the VS Code Explorer and choose "Open with Live Server".
	- This opens your default browser and serves the page over http://127.0.0.1:5500 (or a similar local URL).

4. What to expect
	- The demo's status area will initially show "Loading AI Model..." and then change to "✅ AI Model Loaded." once the TF.js model has been fetched and initialized in the browser.

5. Quick test
	- Click the "Choose Files" button in the demo UI.
	- Upload an image you expect to be detected as sensitive.
	- The image should appear in the gallery, be visually blurred, and display the ⚠️ (warning) icon — that indicates the model flagged it as sensitive.

Notes
- If the model fails to load, open the browser DevTools Console to see network errors. Serving over Live Server or `python -m http.server` is required because TF.js performs XHR requests to load model artifacts.
- Live Server is convenient for development; when you want to fully test model loading performance or CORS behaviors, use the `python -m http.server` approach shown above.


