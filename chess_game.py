import pygame
import sys
import math
from enum import Enum
from typing import List, Tuple, Optional, Dict

# Initialisation de Pygame
pygame.init()

# Constantes
BOARD_SIZE = 640
CELL_SIZE = BOARD_SIZE // 8
WINDOW_WIDTH = BOARD_SIZE + 300  # Espace pour l'interface
WINDOW_HEIGHT = BOARD_SIZE + 100

# Couleurs
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT = (255, 255, 0, 128)
MOVE_HIGHLIGHT = (0, 255, 0, 128)
CAPTURE_HIGHLIGHT = (255, 0, 0, 128)
BACKGROUND = (40, 40, 40)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)
PIECE_WHITE = (255, 255, 255)
PIECE_BLACK = (0, 0, 0)
PIECE_OUTLINE = (128, 128, 128)

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"

class PieceType(Enum):
    PAWN = "pawn"
    ROOK = "rook"
    KNIGHT = "knight"
    BISHOP = "bishop"
    QUEEN = "queen"
    KING = "king"

class Color(Enum):
    WHITE = "white"
    BLACK = "black"

class Piece:
    def __init__(self, piece_type: PieceType, color: Color, row: int, col: int):
        self.type = piece_type
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = False

    def __str__(self):
        return f"{self.color.value}_{self.type.value}"

class MenuButton:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False

    def draw(self, screen):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, TEXT_COLOR, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = Color.WHITE
        self.game_over = False
        self.winner = None
        self.selected_piece = None
        self.valid_moves = []
        self.move_history = []
        self.king_positions = {Color.WHITE: (7, 4), Color.BLACK: (0, 4)}
        self.setup_board()

    def setup_board(self):
        # Placement des pions
        for col in range(8):
            self.board[1][col] = Piece(PieceType.PAWN, Color.BLACK, 1, col)
            self.board[6][col] = Piece(PieceType.PAWN, Color.WHITE, 6, col)

        # Placement des pièces noires
        piece_order = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, 
                      PieceType.QUEEN, PieceType.KING, PieceType.BISHOP, 
                      PieceType.KNIGHT, PieceType.ROOK]
        
        for col, piece_type in enumerate(piece_order):
            self.board[0][col] = Piece(piece_type, Color.BLACK, 0, col)
            self.board[7][col] = Piece(piece_type, Color.WHITE, 7, col)

    def get_valid_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        row, col = piece.row, piece.col

        if piece.type == PieceType.PAWN:
            moves = self._get_pawn_moves(piece)
        elif piece.type == PieceType.ROOK:
            moves = self._get_rook_moves(piece)
        elif piece.type == PieceType.KNIGHT:
            moves = self._get_knight_moves(piece)
        elif piece.type == PieceType.BISHOP:
            moves = self._get_bishop_moves(piece)
        elif piece.type == PieceType.QUEEN:
            moves = self._get_queen_moves(piece)
        elif piece.type == PieceType.KING:
            moves = self._get_king_moves(piece)

        # Filtrer les mouvements qui mettent le roi en échec
        valid_moves = []
        for move in moves:
            if self._is_valid_move_check(piece, move):
                valid_moves.append(move)

        return valid_moves

    def _get_pawn_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        row, col = piece.row, piece.col
        direction = -1 if piece.color == Color.WHITE else 1

        # Mouvement d'une case
        new_row = row + direction
        if 0 <= new_row < 8 and self.board[new_row][col] is None:
            moves.append((new_row, col))
            
            # Mouvement de deux cases (premier mouvement)
            if not piece.has_moved:
                new_row2 = row + 2 * direction
                if 0 <= new_row2 < 8 and self.board[new_row2][col] is None:
                    moves.append((new_row2, col))

        # Captures en diagonale
        for dc in [-1, 1]:
            new_row, new_col = row + direction, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target and target.color != piece.color:
                    moves.append((new_row, new_col))

        return moves

    def _get_rook_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row = piece.row + dr * i
                new_col = piece.col + dc * i
                
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                target = self.board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != piece.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves

    def _get_knight_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dr, dc in knight_moves:
            new_row = piece.row + dr
            new_col = piece.col + dc
            
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target is None or target.color != piece.color:
                    moves.append((new_row, new_col))
        
        return moves

    def _get_bishop_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row = piece.row + dr * i
                new_col = piece.col + dc * i
                
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                target = self.board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != piece.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves

    def _get_queen_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        # La dame combine les mouvements de la tour et du fou
        return self._get_rook_moves(piece) + self._get_bishop_moves(piece)

    def _get_king_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            new_row = piece.row + dr
            new_col = piece.col + dc
            
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target is None or target.color != piece.color:
                    moves.append((new_row, new_col))
        
        return moves

    def _is_valid_move_check(self, piece: Piece, move: Tuple[int, int]) -> bool:
        # Simuler le mouvement pour vérifier s'il met le roi en échec
        old_row, old_col = piece.row, piece.col
        new_row, new_col = move
        
        # Sauvegarder l'état
        captured_piece = self.board[new_row][new_col]
        
        # Faire le mouvement temporaire
        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.row, piece.col = new_row, new_col
        
        # Mettre à jour la position du roi si nécessaire
        if piece.type == PieceType.KING:
            old_king_pos = self.king_positions[piece.color]
            self.king_positions[piece.color] = (new_row, new_col)
        
        # Vérifier si le roi est en échec
        is_valid = not self._is_king_in_check(piece.color)
        
        # Restaurer l'état
        self.board[old_row][old_col] = piece
        self.board[new_row][new_col] = captured_piece
        piece.row, piece.col = old_row, old_col
        
        if piece.type == PieceType.KING:
            self.king_positions[piece.color] = (old_row, old_col)
        
        return is_valid

    def _is_king_in_check(self, color: Color) -> bool:
        king_row, king_col = self.king_positions[color]
        enemy_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        
        # Vérifier si une pièce ennemie peut attaquer le roi
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == enemy_color:
                    enemy_moves = self._get_basic_moves(piece)
                    if (king_row, king_col) in enemy_moves:
                        return True
        return False

    def _get_basic_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        # Obtenir les mouvements sans vérification d'échec pour éviter la récursion
        if piece.type == PieceType.PAWN:
            return self._get_pawn_moves(piece)
        elif piece.type == PieceType.ROOK:
            return self._get_rook_moves(piece)
        elif piece.type == PieceType.KNIGHT:
            return self._get_knight_moves(piece)
        elif piece.type == PieceType.BISHOP:
            return self._get_bishop_moves(piece)
        elif piece.type == PieceType.QUEEN:
            return self._get_queen_moves(piece)
        elif piece.type == PieceType.KING:
            return self._get_king_moves(piece)
        return []

    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        if not piece or piece.color != self.current_player:
            return False
        
        if to_pos not in self.get_valid_moves(piece):
            return False
        
        # Effectuer le mouvement
        captured_piece = self.board[to_row][to_col]
        self.board[from_row][from_col] = None
        self.board[to_row][to_col] = piece
        piece.row, piece.col = to_row, to_col
        piece.has_moved = True
        
        # Mettre à jour la position du roi
        if piece.type == PieceType.KING:
            self.king_positions[piece.color] = (to_row, to_col)
        
        # Promotion du pion
        if piece.type == PieceType.PAWN:
            if (piece.color == Color.WHITE and to_row == 0) or \
               (piece.color == Color.BLACK and to_row == 7):
                # Promotion automatique en dame
                piece.type = PieceType.QUEEN
        
        # Enregistrer le mouvement
        self.move_history.append((from_pos, to_pos, captured_piece))
        
        # Changer de joueur
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        
        # Vérifier l'échec et mat
        if self._is_checkmate(self.current_player):
            self.game_over = True
            self.winner = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        
        return True

    def _is_checkmate(self, color: Color) -> bool:
        if not self._is_king_in_check(color):
            return False
        
        # Vérifier si le joueur a des mouvements légaux
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    if self.get_valid_moves(piece):
                        return False
        
        return True

    def select_piece(self, row: int, col: int):
        piece = self.board[row][col]
        if piece and piece.color == self.current_player:
            self.selected_piece = piece
            self.valid_moves = self.get_valid_moves(piece)
        else:
            self.selected_piece = None
            self.valid_moves = []

class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Échecs et Mat")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 72)
        
        self.state = GameState.MENU
        self.board = None
        self.ai_enabled = False
        self.ai_difficulty = 3
        self.ai_thinking = False
        
        # Boutons du menu
        self.setup_menu()

    def setup_menu(self):
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        button_width = 300
        button_height = 60
        
        self.menu_buttons = [
            MenuButton(center_x - button_width//2, center_y - 120, 
                      button_width, button_height, "Jouer contre IA", self.font),
            MenuButton(center_x - button_width//2, center_y - 40, 
                      button_width, button_height, "Mode 2 joueurs", self.font),
            MenuButton(center_x - button_width//2, center_y + 40, 
                      button_width, button_height, "Quitter", self.font)
        ]
        
        # Boutons de difficulté
        self.difficulty_buttons = []
        for i in range(5):
            self.difficulty_buttons.append(
                MenuButton(center_x - 200 + i * 80, center_y + 120, 
                          60, 40, f"{i+1}", self.font)
            )

    def draw_piece(self, screen, piece: Piece, x: int, y: int, size: int):
        """Dessine une pièce avec des formes géométriques"""
        center_x = x + size // 2
        center_y = y + size // 2
        color = PIECE_WHITE if piece.color == Color.WHITE else PIECE_BLACK
        
        if piece.type == PieceType.PAWN:
            # Pion: cercle simple
            pygame.draw.circle(screen, color, (center_x, center_y), size//3)
            pygame.draw.circle(screen, PIECE_OUTLINE, (center_x, center_y), size//3, 2)
            
        elif piece.type == PieceType.ROOK:
            # Tour: rectangle avec créneaux
            rect_size = size // 2
            rect = pygame.Rect(center_x - rect_size//2, center_y - rect_size//2, rect_size, rect_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, PIECE_OUTLINE, rect, 2)
            # Créneaux
            for i in range(3):
                creneau = pygame.Rect(center_x - rect_size//2 + i * rect_size//3, 
                                     center_y - rect_size//2, rect_size//6, rect_size//4)
                pygame.draw.rect(screen, color, creneau)
                
        elif piece.type == PieceType.KNIGHT:
            # Cavalier: forme en L stylisée
            points = [
                (center_x - size//4, center_y + size//3),
                (center_x - size//6, center_y - size//3),
                (center_x + size//6, center_y - size//4),
                (center_x + size//4, center_y + size//3)
            ]
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, PIECE_OUTLINE, points, 2)
            
        elif piece.type == PieceType.BISHOP:
            # Fou: triangle
            points = [
                (center_x, center_y - size//3),
                (center_x - size//3, center_y + size//3),
                (center_x + size//3, center_y + size//3)
            ]
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, PIECE_OUTLINE, points, 2)
            # Croix au sommet
            pygame.draw.line(screen, PIECE_OUTLINE, 
                           (center_x-5, center_y-size//3-10), 
                           (center_x+5, center_y-size//3-10), 2)
            pygame.draw.line(screen, PIECE_OUTLINE, 
                           (center_x, center_y-size//3-15), 
                           (center_x, center_y-size//3-5), 2)
            
        elif piece.type == PieceType.QUEEN:
            # Dame: cercle avec couronne
            pygame.draw.circle(screen, color, (center_x, center_y), size//3)
            pygame.draw.circle(screen, PIECE_OUTLINE, (center_x, center_y), size//3, 2)
            # Couronne
            crown_points = []
            for i in range(5):
                angle = i * 2 * math.pi / 5
                x = center_x + int((size//4) * math.cos(angle))
                y = center_y - size//3 + int((size//6) * math.sin(angle))
                crown_points.append((x, y))
            pygame.draw.polygon(screen, color, crown_points)
            pygame.draw.polygon(screen, PIECE_OUTLINE, crown_points, 2)
            
        elif piece.type == PieceType.KING:
            # Roi: cercle avec croix
            pygame.draw.circle(screen, color, (center_x, center_y), size//3)
            pygame.draw.circle(screen, PIECE_OUTLINE, (center_x, center_y), size//3, 2)
            # Croix
            cross_size = size // 5
            pygame.draw.line(screen, PIECE_OUTLINE, 
                           (center_x - cross_size, center_y - size//2), 
                           (center_x + cross_size, center_y - size//2), 3)
            pygame.draw.line(screen, PIECE_OUTLINE, 
                           (center_x, center_y - size//2 - cross_size//2), 
                           (center_x, center_y - size//2 + cross_size//2), 3)

    def draw_menu(self):
        self.screen.fill(BACKGROUND)
        
        # Titre
        title = self.big_font.render("ÉCHECS ET MAT", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Sous-titre
        subtitle = self.font.render("Jeu d'échecs avec Intelligence Artificielle", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH//2, 150))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Boutons principaux
        for button in self.menu_buttons:
            button.draw(self.screen)
        
        # Section difficulté IA si pertinent
        if hasattr(self, 'show_difficulty') and self.show_difficulty:
            diff_text = self.font.render("Choisissez la difficulté:", True, TEXT_COLOR)
            diff_rect = diff_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 80))
            self.screen.blit(diff_text, diff_rect)
            
            for button in self.difficulty_buttons:
                button.draw(self.screen)

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                # Dessiner les pièces
                piece = self.board.board[row][col]
                if piece:
                    self.draw_piece(self.screen, piece, col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE)

    def draw_highlights(self):
        # Surligner la pièce sélectionnée
        if self.board.selected_piece:
            row, col = self.board.selected_piece.row, self.board.selected_piece.col
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            highlight_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            highlight_surface.fill(HIGHLIGHT)
            self.screen.blit(highlight_surface, rect)
        
        # Surligner les mouvements valides
        for row, col in self.board.valid_moves:
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            highlight_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            
            if self.board.board[row][col]:  # Case avec pièce ennemie
                highlight_surface.fill(CAPTURE_HIGHLIGHT)
            else:  # Case vide
                highlight_surface.fill(MOVE_HIGHLIGHT)
            
            self.screen.blit(highlight_surface, rect)

    def draw_ui(self):
        ui_rect = pygame.Rect(BOARD_SIZE, 0, 300, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, BACKGROUND, ui_rect)
        
        title = self.font.render("Échecs et Mat", True, TEXT_COLOR)
        self.screen.blit(title, (BOARD_SIZE + 10, 20))
        
        current_player_text = f"Joueur: {'Blanc' if self.board.current_player == Color.WHITE else 'Noir'}"
        player_surface = self.small_font.render(current_player_text, True, TEXT_COLOR)
        self.screen.blit(player_surface, (BOARD_SIZE + 10, 70))
        
        if self.board.game_over:
            winner_text = f"Victoire: {'Blanc' if self.board.winner == Color.WHITE else 'Noir'}!"
            winner_surface = self.font.render(winner_text, True, (255, 215, 0))
            self.screen.blit(winner_surface, (BOARD_SIZE + 10, 110))
        elif self.board._is_king_in_check(self.board.current_player):
            check_surface = self.font.render("ÉCHEC!", True, (255, 0, 0))
            self.screen.blit(check_surface, (BOARD_SIZE + 10, 110))
        
        if self.ai_enabled:
            ai_text = f"IA: Niveau {self.ai_difficulty}"
            ai_surface = self.small_font.render(ai_text, True, (0, 255, 0))
            self.screen.blit(ai_surface, (BOARD_SIZE + 10, 150))
            
            if self.ai_thinking:
                thinking_text = "IA réfléchit..."
                thinking_surface = self.small_font.render(thinking_text, True, (255, 255, 0))
                self.screen.blit(thinking_surface, (BOARD_SIZE + 10, 170))
    
        instructions = [
            "Instructions:",
            "- Clic: Sélectionner/Bouger",
            "- R: Nouvelle partie", 
            "- M: Retour au menu",
            "- Q: Quitter"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_surface = self.small_font.render(instruction, True, TEXT_COLOR)
            self.screen.blit(inst_surface, (BOARD_SIZE + 10, 200 + i * 25))

    def handle_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_buttons[0].handle_event(event):  # Contre IA
                self.ai_enabled = True
                self.show_difficulty = True
                return
            elif self.menu_buttons[1].handle_event(event):  # 2 joueurs
                self.start_game(False)
                return
            elif self.menu_buttons[2].handle_event(event):  # Quitter
                return "quit"
            
            # Vérifier les boutons de difficulté
            if hasattr(self, 'show_difficulty') and self.show_difficulty:
                for i, button in enumerate(self.difficulty_buttons):
                    if button.handle_event(event):
                        self.ai_difficulty = i + 1
                        self.start_game(True)
                        return
        
        # Mettre à jour l'état des boutons
        for button in self.menu_buttons:
            button.handle_event(event)
        
        if hasattr(self, 'show_difficulty') and self.show_difficulty:
            for button in self.difficulty_buttons:
                button.handle_event(event)

    def start_game(self, ai_enabled):
        self.ai_enabled = ai_enabled
        self.board = ChessBoard()
        self.state = GameState.PLAYING
        self.show_difficulty = False

    def handle_click(self, pos: Tuple[int, int]):
        x, y = pos
        if x >= BOARD_SIZE:
            return
        
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        
        if not (0 <= row < 8 and 0 <= col < 8):
            return
        
        if self.board.selected_piece:
            if (row, col) in self.board.valid_moves:
                from_pos = (self.board.selected_piece.row, self.board.selected_piece.col)
                self.board.make_move(from_pos, (row, col))
                self.board.selected_piece = None
                self.board.valid_moves = []
            else:
                self.board.select_piece(row, col)
        else:
            self.board.select_piece(row, col)

    def handle_ai_move(self):
        if self.ai_enabled and self.board.current_player == Color.BLACK and not self.board.game_over:
            # Import ici pour éviter les problèmes de dépendance circulaire
            from chess_ai import get_ai_move
            move = get_ai_move(self.board, self.ai_difficulty)
            if move:
                from_pos, to_pos = move
                self.board.make_move(from_pos, to_pos)

    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif self.state == GameState.MENU:
                    result = self.handle_menu_events(event)
                    if result == "quit":
                        running = False
                
                elif self.state == GameState.PLAYING:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 and not self.ai_thinking:
                            self.handle_click(event.pos)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.board = ChessBoard()
                        elif event.key == pygame.K_m:
                            self.state = GameState.MENU
                            self.setup_menu()
                        elif event.key == pygame.K_q:
                            running = False
            
            # IA automatique
            if (self.state == GameState.PLAYING and 
                self.ai_enabled and 
                self.board.current_player == Color.BLACK and 
                not self.board.game_over and 
                not self.ai_thinking):
                self.handle_ai_move()
            
            # Dessiner
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.screen.fill(BACKGROUND)
                self.draw_board()
                self.draw_highlights()
                self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ChessGame()
    game.run() 