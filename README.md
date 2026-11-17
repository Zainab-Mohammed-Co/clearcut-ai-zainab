# ClearCut AI

Free, self-hosted image background remover using Flask + Rembg (`u2net`). No paid API key required.

## Start on Windows 11 with Docker Desktop

1. Extract this ZIP.
2. Open PowerShell in the extracted `clearcut-ai` folder.
3. Run `docker compose up --build -d`.
4. Open http://localhost:3000
5. To view errors: `docker compose logs -f web`
6. To stop: `docker compose down`

The AI model downloads on the first processing request; allow extra time and an internet connection. CPU inference can take time. Docker image and model require significant disk/RAM. Hosting is not automatically free, even though the AI model is open-source.

## Without Docker

Use Python 3.12, create and activate a virtual environment, run `pip install -r requirements.txt`, then `python app.py` and open http://localhost:3000.

## Notes

- Max 12 MB per image, max 25 megapixels.
- JPG/PNG/WebP input; transparent PNG output, optionally composited onto a color in the browser.
- Images are processed in memory and not intentionally saved by the application.
- For public deployment, add rate limiting, authentication/abuse protection, HTTPS and resource limits.
- Check the licenses for Rembg and any selected AI model before commercial deployment.
