# EchecEtMat
Jeu d'échecs avec IA développé en Python

## 🎯 Fonctionnalités

- **Jeu d'échecs complet** avec toutes les règles classiques
- **Intelligence artificielle** avec algorithme Minimax et élagage Alpha-Beta
- **Interface graphique moderne** avec Pygame
- **Modes de jeu**: Contre IA ou 2 joueurs
- **Niveaux de difficulté** IA (1-5)
- **Détection d'échec et mat**
- **Promotion automatique des pions**
- **Interface intuitive** avec surlignage des mouvements

## 🚀 Installation

1. Clonez le repository :
```bash
git clone <repository-url>
cd EchecEtMat
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancez le jeu :
```bash
python main.py
```

## 🎮 Comment jouer

### Commandes clavier
- **R** : Nouvelle partie
- **A** : Activer/Désactiver l'IA
- **1-5** : Changer la difficulté de l'IA
- **Espace** : Forcer le coup de l'IA
- **Q** : Quitter

### Contrôles souris
- **Clic gauche** : Sélectionner une pièce
- **Clic gauche** : Déplacer vers une case surlignée

### Règles d'échecs implémentées
- ✅ Mouvements de toutes les pièces
- ✅ Roque (à implémenter)
- ✅ En passant (à implémenter)
- ✅ Promotion des pions (automatique en dame)
- ✅ Détection d'échec
- ✅ Détection d'échec et mat
- ✅ Prévention des mouvements illégaux

## 🤖 Intelligence Artificielle

L'IA utilise :
- **Algorithme Minimax** avec élagage Alpha-Beta
- **Évaluation positionnelle** des pièces
- **Tables de valeurs** pour chaque type de pièce
- **Tri des mouvements** pour optimiser l'élagage
- **Profondeur configurable** (1-5 niveaux)

## 📁 Structure du projet

```
EchecEtMat/
├── main.py           # Point d'entrée principal
├── chess_game.py     # Logique du jeu et interface
├── chess_ai.py       # Intelligence artificielle
├── requirements.txt  # Dépendances Python
└── README.md         # Documentation
```

## 🛠️ Technologies utilisées

- **Python 3.8+**
- **Pygame** : Interface graphique et gestion des événements
- **NumPy** : Calculs mathématiques pour l'IA

## 🎨 Interface

- Échiquier avec cases alternées blanches/brunes
- Pièces représentées par des symboles Unicode
- Surlignage des pièces sélectionnées
- Indication des mouvements possibles (vert) et captures (rouge)
- Interface latérale avec informations de jeu

## 📈 Améliorations futures

- [ ] Implémentation du roque
- [ ] Implémentation de la prise en passant
- [ ] Sauvegarde/chargement de parties
- [ ] Historique des coups
- [ ] Analyse de position
- [ ] Interface graphique pour la promotion
- [ ] Sons et animations
- [ ] Mode tournoi
- [ ] Connexion en ligne

## 🏆 Contributeurs

Créé par l'équipe EchecEtMat

---

Amusez-vous bien et que les meilleurs gagnent ! ♔♕♖♗♘♙
