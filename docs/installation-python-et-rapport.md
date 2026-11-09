# Installer Python et produire un rapport industriel avec Qwen3-VL

Guide Mac (Apple Silicon M1/M2/M3/M4/M5), adapté au fil rouge du **Comptoir de l'IA**.

## 1. Vérifier Python

Ouvrez **Terminal** (Applications → Utilitaires → Terminal).

```bash
python3 --version
```

Si Python 3 est disponible, vous pouvez continuer. Le script utilise uniquement la **bibliothèque standard** : ni `pip install`, ni environnement virtuel, ni abonnement nécessaire.

Si la commande manque ou affiche une version ancienne, téléchargez un installateur macOS officiel depuis [python.org/downloads](https://www.python.org/downloads/) et suivez les instructions, puis **rouvrez le Terminal** et revérifiez `python3 --version`.

> Astuce : sur macOS, utilisez `python3` plutôt que `python`. Python 3.9+ est conseillé pour ce tutoriel.

## 2. Installer Ollama et le modèle

Télécharger l'application officielle : [ollama.com/download/mac](https://ollama.com/download/mac), puis **la lancer**.

Dans le Terminal macOS :

```bash
ollama --version
ollama pull qwen3-vl:2b-instruct
ollama list
ollama show qwen3-vl:2b-instruct
```

Documentation du modèle source : [Hugging Face — Qwen3-VL-2B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct).

La variante `instruct` vise une réponse directe aux consignes ; la variante `qwen3-vl:2b` est orientée raisonnement. Ce sont deux variantes distinctes, pas simplement deux réglages de température.

## 3. Test interactif dans Ollama

Toujours dans le Terminal macOS :

```bash
ollama run qwen3-vl:2b-instruct
```

À l'invite **`>>>`**, saisir **une commande par ligne** :

```text
/set parameter num_ctx 8192
/set parameter temperature 0.2
/set parameter num_predict 600
```

Puis copier la consigne :

> Analyse cette photographie industrielle. Décris les équipements visibles, retranscris les textes réellement lisibles, identifie les dispositifs de sécurité visibles et indique toutes les incertitudes. N'invente aucun chiffre ni aucune anomalie.

**Important :** ajoutez un espace et **glissez l'image depuis Finder** vers le Terminal avant de valider. Le message `Added image` indique qu'Ollama a reconnu le fichier. Sans preuve d'envoi, un modèle peut générer une description imaginaire.

Pour revenir au Terminal macOS : `/bye`.

### Leçons des épisodes précédents

- `/set parameter ...` fonctionne dans **Ollama** (`>>>`), pas dans le shell `zsh` (`%`).
- Une requête image pouvait nécessiter **4126 tokens**, au-delà d'une limite initiale de **4096**. Le réglage à 8192 a permis de dépasser ce blocage précis.
- Une **température basse** influence la diversité des sorties, mais **n'assure pas l'exactitude**.
- Un rapport produit par un script séparé peut différer d'une réponse interactive : ce sont **deux requêtes différentes**.

## 4. Récupérer le script du dépôt

Sur la page du dépôt GitHub, cliquez sur **Code → Download ZIP**, décompressez le dossier téléchargé puis ouvrez le Terminal dans le dossier contenant le dépôt.

Alternative pour les utilisateurs disposant de Git :

```bash
git clone https://github.com/romuhica73/le-comptoir-ia-laboratoire.git
cd le-comptoir-ia-laboratoire
```

Placez une photographie non confidentielle nommée `test-industrie.jpg` sur votre Bureau. **Cette photographie n'est pas fournie dans le dépôt** ; utilisez la vôtre avec les droits appropriés.

Exécutez :

```bash
python3 scripts/rapport_qwen3vl.py
```

Ou, depuis n'importe quel dossier, indiquez le chemin exact du script. Vous pouvez aussi choisir une autre image :

```bash
python3 scripts/rapport_qwen3vl.py --image "/chemin/vers/photo.jpg"
```

Le script contacte **l'API locale** `http://127.0.0.1:11434`, encode et transmet l'image, vérifie le nom du modèle renvoyé, et utilise explicitement :
- `num_ctx=8192`
- `temperature=0.2`
- `num_predict=600`

Il ne relance **qu'une seule inférence** pour le Terminal et les rapports : le contenu affiché correspond à celui enregistré.

## 5. Où sont les résultats ?

Dans `~/Desktop/Rapport-Qwen3-VL/` :
- `rapport.html` : document lisible dans un navigateur, ouvert automatiquement sur Mac ;
- `rapport.md` : rapport texte Markdown ;
- `trace.json` : date, paramètres, nom et empreinte du modèle, empreinte de l'image, sortie et métriques disponibles.

La trace permet de documenter **quel artefact local** a été sollicité, pas de garantir que son raisonnement est juste. Le rapport reste **non validé**.

**Confidentialité :** la requête d'inférence du script est envoyée à `127.0.0.1`. Cela ne garantit pas automatiquement la confidentialité de l'ordinateur, des sauvegardes ou des autres applications. Ne publiez pas les photos, rapports et traces contenant des données sensibles.

## 6. Dépannage rapide

| Symptôme | Vérification |
|---|---|
| `ollama: command not found` | Lancer/réinstaller Ollama, relancer le Terminal |
| Modèle absent | `ollama pull qwen3-vl:2b-instruct` |
| `/set: no such file` | Vous êtes dans le shell : exécuter d'abord `ollama run ...` |
| `exceeds available context size` | Régler `num_ctx 8192`, ou réduire l'image et le prompt |
| Image non reconnue | Glisser le fichier dans l'invite Ollama ; dans le script, contrôler son chemin |
| Le modèle invente | Vérifier la transmission réelle, réduire l'ambiguïté, contrôler manuellement |
| Aucune page ouverte | Ouvrir manuellement `~/Desktop/Rapport-Qwen3-VL/rapport.html` |
| Réponse tronquée | Consulter `done_reason` dans `trace.json` ; augmenter prudemment `num_predict` |

## 7. Limites et usages interdits

Un petit modèle visuel peut confondre une inscription, une unité, un cadran ou un dispositif de consignation. Une température faible ne résout pas ces erreurs. **Ne vous fiez pas à ce rapport pour décider de mettre sous tension un appareil, confirmer une consignation ou déclarer une installation conforme.** Faites vérifier le document par un professionnel compétent.

Sources : [Ollama](https://docs.ollama.com/), [Qwen sur Hugging Face](https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct), [Python](https://www.python.org/downloads/).
