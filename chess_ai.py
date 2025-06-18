import random
import math
from typing import List, Tuple, Optional
from chess_game import ChessBoard, Color, PieceType, Piece

class ChessAI:
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty  # Profondeur de recherche (1-5)
        self.piece_values = {
            PieceType.PAWN: 100,
            PieceType.KNIGHT: 320,
            PieceType.BISHOP: 330,
            PieceType.ROOK: 500,
            PieceType.QUEEN: 900,
            PieceType.KING: 20000
        }
        
        # Tables de position pour l'évaluation
        self.pawn_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ]
        
        self.knight_table = [
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ]
        
        self.bishop_table = [
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ]
        
        self.rook_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [5, 10, 10, 10, 10, 10, 10,  5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [0,  0,  0,  5,  5,  0,  0,  0]
        ]
        
        self.queen_table = [
            [-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [-5,  0,  5,  5,  5,  5,  0, -5],
            [0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]
        ]
        
        self.king_middle_game = [
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [20, 20,  0,  0,  0,  0, 20, 20],
            [20, 30, 10,  0,  0, 10, 30, 20]
        ]

    def get_best_move(self, board: ChessBoard) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Retourne le meilleur mouvement pour l'IA"""
        if board.current_player == Color.WHITE:
            return None  # L'IA joue uniquement les noirs
        
        _, best_move = self.minimax(board, self.difficulty, -math.inf, math.inf, True)
        return best_move

    def minimax(self, board: ChessBoard, depth: int, alpha: float, beta: float, 
                maximizing_player: bool) -> Tuple[float, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        """Algorithme minimax avec élagage alpha-beta"""
        if depth == 0 or board.game_over:
            return self.evaluate_board(board), None
        
        best_move = None
        moves = self.get_all_possible_moves(board, board.current_player)
        
        if not moves:
            # Pas de mouvements possibles
            if board._is_king_in_check(board.current_player):
                # Échec et mat
                return -math.inf if maximizing_player else math.inf, None
            else:
                # Pat
                return 0, None
        
        # Trier les mouvements pour améliorer l'élagage
        moves = self.order_moves(board, moves)
        
        if maximizing_player:
            max_eval = -math.inf
            for move in moves:
                # Simuler le mouvement
                board_copy = self.make_move_copy(board, move)
                eval_score, _ = self.minimax(board_copy, depth - 1, alpha, beta, False)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Élagage alpha-beta
            
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in moves:
                # Simuler le mouvement
                board_copy = self.make_move_copy(board, move)
                eval_score, _ = self.minimax(board_copy, depth - 1, alpha, beta, True)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Élagage alpha-beta
            
            return min_eval, best_move

    def get_all_possible_moves(self, board: ChessBoard, color: Color) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Retourne tous les mouvements possibles pour une couleur"""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece and piece.color == color:
                    piece_moves = board.get_valid_moves(piece)
                    for move in piece_moves:
                        moves.append(((row, col), move))
        return moves

    def make_move_copy(self, board: ChessBoard, move: Tuple[Tuple[int, int], Tuple[int, int]]) -> ChessBoard:
        """Crée une copie du plateau avec le mouvement effectué"""
        # Créer une copie profonde du plateau
        new_board = ChessBoard()
        
        # Copier l'état du plateau
        for row in range(8):
            for col in range(8):
                if board.board[row][col]:
                    piece = board.board[row][col]
                    new_piece = Piece(piece.type, piece.color, piece.row, piece.col)
                    new_piece.has_moved = piece.has_moved
                    new_board.board[row][col] = new_piece
                else:
                    new_board.board[row][col] = None
        
        new_board.current_player = board.current_player
        new_board.king_positions = board.king_positions.copy()
        new_board.game_over = board.game_over
        new_board.winner = board.winner
        
        # Effectuer le mouvement
        from_pos, to_pos = move
        new_board.make_move(from_pos, to_pos)
        
        return new_board

    def order_moves(self, board: ChessBoard, moves: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Ordonne les mouvements pour améliorer l'élagage alpha-beta"""
        def move_priority(move):
            from_pos, to_pos = move
            to_row, to_col = to_pos
            
            score = 0
            
            # Prioriser les captures
            target = board.board[to_row][to_col]
            if target:
                score += self.piece_values[target.type]
            
            # Prioriser les mouvements vers le centre
            center_distance = abs(3.5 - to_row) + abs(3.5 - to_col)
            score += (7 - center_distance) * 10
            
            return score
        
        return sorted(moves, key=move_priority, reverse=True)

    def evaluate_board(self, board: ChessBoard) -> float:
        """Évalue la position du plateau"""
        if board.game_over:
            if board.winner == Color.BLACK:
                return 10000
            elif board.winner == Color.WHITE:
                return -10000
            else:
                return 0  # Match nul
        
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece:
                    piece_value = self.piece_values[piece.type]
                    position_value = self.get_position_value(piece, row, col)
                    
                    total_value = piece_value + position_value
                    
                    if piece.color == Color.BLACK:
                        score += total_value
                    else:
                        score -= total_value
        
        # Bonus pour la sécurité du roi
        if board._is_king_in_check(Color.WHITE):
            score += 50
        if board._is_king_in_check(Color.BLACK):
            score -= 50
        
        # Bonus pour la mobilité
        white_moves = len(self.get_all_possible_moves(board, Color.WHITE))
        black_moves = len(self.get_all_possible_moves(board, Color.BLACK))
        score += (black_moves - white_moves) * 10
        
        return score

    def get_position_value(self, piece: Piece, row: int, col: int) -> int:
        """Retourne la valeur positionnelle d'une pièce"""
        if piece.color == Color.WHITE:
            # Inverser la table pour les blancs
            row = 7 - row
        
        if piece.type == PieceType.PAWN:
            return self.pawn_table[row][col]
        elif piece.type == PieceType.KNIGHT:
            return self.knight_table[row][col]
        elif piece.type == PieceType.BISHOP:
            return self.bishop_table[row][col]
        elif piece.type == PieceType.ROOK:
            return self.rook_table[row][col]
        elif piece.type == PieceType.QUEEN:
            return self.queen_table[row][col]
        elif piece.type == PieceType.KING:
            return self.king_middle_game[row][col]
        
        return 0

# Fonction utilitaire pour intégrer l'IA dans le jeu principal
def get_ai_move(board: ChessBoard, difficulty: int = 3) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Interface simplifiée pour obtenir un mouvement de l'IA"""
    ai = ChessAI(difficulty)
    return ai.get_best_move(board) 