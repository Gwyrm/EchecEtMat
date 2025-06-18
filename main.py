#!/usr/bin/env python3
"""
Échecs et Mat - Jeu d'échecs avec IA
"""

from chess_game import ChessGame

def main():
    """Fonction principale"""
    print("🎯 Lancement d'Échecs et Mat...")
    print("Interface graphique avec menu intégré")
    
    # Lancer le jeu avec menu graphique
    game = ChessGame()
    game.run()

if __name__ == "__main__":
    main() 