import io
import os
from functools import lru_cache
from flask import Flask, jsonify, request, send_file, send_from_directory
from PIL import Image, ImageOps, UnidentifiedImageError
from rembg import new_session, remove

app = Flask(__name__, static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 12 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 30_000_000

# Smaller inputs reduce the peak RAM needed by the segmentation model.
MAX_AI_SIDE = 1024

@lru_cache(maxsize=1)
def session():
    return new_session('u2netp')

@app.get('/')
def home():
    return send_from_directory('static', 'index.html')

@app.get('/health')
def health():
    return jsonify(status='ok')

@app.post('/api/remove')
def remove_background():
    upload = request.files.get('image')
    if not upload:
        return jsonify(error='Please upload an image.'), 400
    if upload.mimetype not in ('image/png', 'image/jpeg', 'image/webp'):
        return jsonify(error='Only JPG, PNG and WebP are supported.'), 400
    try:
        with Image.open(upload.stream) as check:
            check.verify()
        upload.stream.seek(0)
        with Image.open(upload.stream) as source:
            if source.width * source.height > 25_000_000:
                return jsonify(error='Image resolution is too large (max 25 megapixels).'), 400
            image = ImageOps.exif_transpose(source).convert('RGB')
        image.thumbnail((MAX_AI_SIDE, MAX_AI_SIDE), Image.Resampling.LANCZOS)
        result = remove(image, session=session()).convert('RGBA')
        out = io.BytesIO()
        result.save(out, format='PNG', optimize=False)
        out.seek(0)
        return send_file(out, mimetype='image/png', download_name='clearcut.png', as_attachment=False)
    except (UnidentifiedImageError, OSError, ValueError):
        return jsonify(error='Could not read this image.'), 400
    except Exception:
        app.logger.exception('Background removal failed')
        return jsonify(error='Processing failed. Please try again.'), 500

@app.errorhandler(413)
def too_large(_):
    return jsonify(error='File is too large (maximum 12 MB).'), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '3000')))
