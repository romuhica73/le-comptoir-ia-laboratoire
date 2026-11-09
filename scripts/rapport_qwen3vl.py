#!/usr/bin/env python3
"""Le Comptoir de l'IA : une seule analyse Qwen3-VL -> Terminal + HTML + Markdown + JSON."""
import argparse
import base64
import hashlib
import html
import json
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

API = "http://127.0.0.1:11434"
MODEL = "qwen3-vl:2b-instruct"
PROMPT = """Analyse uniquement la photographie jointe.
Rédige en français un rapport concis avec quatre sections :
1. ÉQUIPEMENTS : compte les instruments analogiques et décris les commandes visibles.
2. INSCRIPTIONS : recopie seulement les textes réellement lisibles.
3. SÉCURITÉ : identifie uniquement les dispositifs de sécurité visibles.
4. INCERTITUDES : signale ce qui est illisible ou impossible à déterminer.
Ne fabrique aucune valeur, inscription ou anomalie. Ne conclus jamais à la conformité.
Rends directement le rapport final sans détailler ton raisonnement."""


def request_json(path, payload=None, timeout=300):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API + path, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description="Analyse locale de photo avec Ollama.")
    parser.add_argument(
        "--image",
        type=Path,
        default=Path.home() / "Desktop" / "test-industrie.jpg",
        help="Chemin vers la photographie (défaut : ~/Desktop/test-industrie.jpg)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.home() / "Desktop" / "Rapport-Qwen3-VL",
        help="Dossier de sortie (défaut : ~/Desktop/Rapport-Qwen3-VL)",
    )
    args = parser.parse_args()
    image_path = args.image.expanduser()
    if not image_path.is_file():
        sys.exit(f"ERREUR : photographie introuvable : {image_path}")
    if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        sys.exit("ERREUR : utilisez une image JPG, PNG ou WebP.")

    image_bytes = image_path.read_bytes()
    image_sha = hashlib.sha256(image_bytes).hexdigest()

    try:
        tags = request_json("/api/tags", timeout=15)
    except (urllib.error.URLError, TimeoutError) as exc:
        sys.exit(f"ERREUR : Ollama ne répond pas sur {API}. Lancez son application. {exc}")

    model_info = next(
        (m for m in tags.get("models", []) if m.get("name") == MODEL), None
    )
    if model_info is None:
        sys.exit(f"ERREUR : modèle absent. Exécutez : ollama pull {MODEL}")

    options = {"num_ctx": 8192, "temperature": 0.2, "num_predict": 600}
    payload = {
        "model": MODEL,
        "stream": False,
        "messages": [{
            "role": "user",
            "content": PROMPT,
            "images": [base64.b64encode(image_bytes).decode("ascii")],
        }],
        "options": options,
    }
    print(f"Modèle demandé : {MODEL}")
    print(f"SHA-256 du modèle installé : {model_info.get('digest', 'inconnu')}")
    print(f"Image : {image_path} | SHA-256 : {image_sha}")
    print("Analyse locale en cours...")

    try:
        result = request_json("/api/chat", payload, timeout=300)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        sys.exit(f"ERREUR HTTP Ollama {exc.code} : {body}")
    except (urllib.error.URLError, TimeoutError) as exc:
        sys.exit(f"ERREUR de génération : {exc}")

    actual_model = result.get("model")
    if actual_model != MODEL:
        sys.exit(f"ERREUR : modèle exécuté inattendu : {actual_model!r}")
    response_text = result.get("message", {}).get("content", "").strip()
    if not response_text:
        sys.exit("ERREUR : réponse finale vide. Aucun rapport produit.")

    done_reason = result.get("done_reason", "inconnu")
    validation = "NON VALIDÉ — contrôle humain obligatoire"
    if done_reason == "length":
        validation = "NON VALIDÉ — réponse potentiellement tronquée"
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    trace = {
        "date": timestamp,
        "model_requested": MODEL,
        "model_executed": actual_model,
        "model_digest": model_info.get("digest"),
        "model_details": model_info.get("details"),
        "image_name": image_path.name,
        "image_sha256": image_sha,
        "prompt": PROMPT,
        "options": options,
        "done_reason": done_reason,
        "prompt_eval_count": result.get("prompt_eval_count"),
        "eval_count": result.get("eval_count"),
        "total_duration_ns": result.get("total_duration"),
        "report": response_text,
        "validation": validation,
    }

    output = args.output.expanduser()
    output.mkdir(parents=True, exist_ok=True)
    (output / "trace.json").write_text(
        json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output / "rapport.md").write_text(
        "# Rapport d'analyse visuelle — NON VALIDÉ\n\n" + response_text + "\n",
        encoding="utf-8",
    )
    report_escaped = html.escape(response_text)
    page = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>Rapport Qwen3-VL</title>
<style>
body {{background:#f3f0eb;color:#282037;font-family:-apple-system,BlinkMacSystemFont,Arial,sans-serif;padding:32px}}
main {{max-width:850px;margin:auto;background:white;border-radius:16px;padding:42px;box-shadow:0 8px 28px #0001}}
h1 {{margin-bottom:8px}} .meta {{color:#615b70;line-height:1.6}}
.warn {{background:#fff3e1;border-left:4px solid #ac6a20;padding:14px;margin:24px 0}}
pre {{white-space:pre-wrap;overflow-wrap:anywhere;font:16px/1.7 -apple-system,BlinkMacSystemFont,Arial,sans-serif}}
</style></head><body><main>
<h1>Rapport d'analyse visuelle</h1>
<p>Le Comptoir de l'IA — laboratoire expérimental</p>
<p class="meta">Date : {html.escape(timestamp)}<br>Modèle : {html.escape(MODEL)}
<br>Température : 0,2 — Contexte : 8192 tokens
<br>SHA-256 modèle : {html.escape(str(model_info.get("digest", "inconnu")))}</p>
<div class="warn"><strong>{html.escape(validation)}</strong><br>
Ne pas utiliser pour une décision de sécurité ou de conformité.</div>
<pre>{report_escaped}</pre>
</main></body></html>"""
    html_path = output / "rapport.html"
    html_path.write_text(page, encoding="utf-8")

    print("\n=== RÉPONSE DU MODÈLE (IDENTIQUE AU RAPPORT) ===\n")
    print(response_text)
    print(f"\nFin de génération : {done_reason}")
    print(f"Rapport HTML : {html_path}")
    print(f"Rapport Markdown : {output / 'rapport.md'}")
    print(f"Trace JSON : {output / 'trace.json'}")
    if sys.platform == "darwin":
        subprocess.run(["open", str(html_path)], check=False)


if __name__ == "__main__":
    main()
