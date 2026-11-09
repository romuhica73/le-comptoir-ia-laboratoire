# Le Comptoir de l'IA — Laboratoire ouvert

**Les ressources du fil rouge YouTube : construire et tester une IA locale, 10 minutes par émission.**

Ce dépôt est public et pédagogique. Il contient les commandes, les explications et les scripts utilisés dans l'émission. Aucun compte Hugging Face n'est nécessaire pour les premiers essais.

> **Important :** ce projet est expérimental. Les descriptions d'un équipement par une IA peuvent contenir des erreurs ; ne les utilisez pas pour prendre une décision de sécurité, de conformité ou de maintenance sans contrôle humain.

## Démarrage rapide (Mac Apple Silicon)

### 1 — Installer Ollama

Télécharger [Ollama pour macOS](https://ollama.com/download/mac), installer et **ouvrir l'application**.

Dans l'application **Terminal** du Mac (invite se terminant par `%` ou `$`) :

```bash
ollama --version
ollama pull qwen3-vl:2b-instruct
ollama list
ollama show qwen3-vl:2b-instruct
ollama run qwen3-vl:2b-instruct
```

### 2 — Régler le modèle

Quand vous voyez `>>>`, vous êtes **dans Ollama**, pas dans le shell macOS. Saisissez chaque ligne séparément :

```text
/set parameter num_ctx 8192
/set parameter temperature 0.2
/set parameter num_predict 600
```

- **Contexte 8192 :** espace de travail réservé pour les instructions et la représentation de l'image (nécessite de la mémoire).
- **Température 0,2 :** réduit généralement la variabilité des sorties, sans supprimer les erreurs.
- **600 tokens :** limite la longueur de la réponse.

### 3 — Analyser une photo

Dans Ollama, entrez cette consigne :

> Analyse cette photographie industrielle. Réponds en français avec quatre sections : ÉQUIPEMENTS (compte les instruments analogiques), INSCRIPTIONS (uniquement les textes lisibles avec certitude), SÉCURITÉ (uniquement les dispositifs visibles), INCERTITUDES (ce qui est illisible ou non déterminable). Ne fabrique aucune valeur, inscription ni anomalie.

**Ajoutez un espace et glissez l'image depuis Finder dans le Terminal avant Entrée.** Contrôlez l'apparition de `Added image`. Un simple nom de fichier mentionné dans la question n'est pas une preuve que le modèle a reçu l'image.

Pour quitter la session Ollama : `/bye`.

## Produire un rapport HTML, Markdown et JSON

Voir le guide détaillé : **[Installer Python et générer le rapport](docs/installation-python-et-rapport.md)**.

Le script [`scripts/rapport_qwen3vl.py`](scripts/rapport_qwen3vl.py) fait **une seule requête** à l'API Ollama locale, imprime la réponse dans le Terminal, puis enregistre **exactement cette même réponse** en HTML et Markdown, ainsi qu'une trace JSON (nom et empreinte du modèle, empreinte de l'image, paramètres, durée de génération).

Pour l'essai de l'émission, placez une image nommée `test-industrie.jpg` sur votre Bureau et exécutez :

```bash
python3 scripts/rapport_qwen3vl.py
```

Le dossier `~/Desktop/Rapport-Qwen3-VL/` est créé, et le rapport HTML est ouvert dans votre navigateur.

## Pourquoi Instruct plutôt que Thinking ?

- `qwen3-vl:2b-instruct` : variante adaptée aux consignes directes et aux comptes rendus.
- `qwen3-vl:2b` : variante de raisonnement qui peut générer une longue phase de réflexion.
- Changer de variante **et** de température simultanément ne permet pas de mesurer l'effet isolé de la température.

## Ressources officielles

- [Qwen3-VL-2B-Instruct sur Hugging Face](https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct)
- [Qwen3-VL 2B Instruct pour Ollama](https://ollama.com/library/qwen3-vl:2b-instruct)
- [Documentation d'Ollama](https://docs.ollama.com/)
- [Téléchargement de Python](https://www.python.org/downloads/)

## Organisation

- `README.md` — guide de démarrage et liens de l'émission
- `docs/installation-python-et-rapport.md` — installation de Python, dépannage, production de documents
- `scripts/rapport_qwen3vl.py` — script autonome, bibliothèque standard Python uniquement
- `.gitignore` — protection contre la publication accidentelle de résultats et photos locales

Les résultats de l'IA ne sont **pas** certifiés ; le contrôle humain demeure obligatoire.
