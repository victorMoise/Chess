import pygame
import pieces
import clock
import check_interrupt

pygame.init()

WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 8
SQUARE_SIZE = HEIGHT // BOARD_SIZE
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
DARK_YELLOW = (246, 190, 0)
LIGHT_YELLOW = (241, 235, 156)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

moves = []
playing_board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

game_over = False
player = 1
selected_piece = None
selected_piece_position = None

# variables for the castles moves
white_right_rook_moved = False
white_left_rook_moved = False
black_right_rook_moved = False
black_left_rook_moved = False
white_king_moved = False
black_king_moved = False

def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):            
            square_color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(screen, square_color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # make the selected square yellow
            if selected_piece_position == (row, col):
                yellow_square = LIGHT_YELLOW if (row + col) % 2 == 0 else DARK_YELLOW
                pygame.draw.rect(screen, yellow_square, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = playing_board[row][col]
            if piece != " ":
                match piece:
                    case "p":
                        piece_image = pieces.black_pawn
                    case "P":
                        piece_image = pieces.white_pawn
                    case "n":
                        piece_image = pieces.black_knight
                    case "N":
                        piece_image = pieces.white_knight
                    case "b":
                        piece_image = pieces.black_bishop
                    case "B":
                        piece_image = pieces.white_bishop
                    case "r":
                        piece_image = pieces.black_rook
                    case "R":
                        piece_image = pieces.white_rook
                    case "q":
                        piece_image = pieces.black_queen
                    case "Q":
                        piece_image = pieces.white_queen
                    case "k":
                        piece_image = pieces.black_king
                    case "K":
                        piece_image = pieces.white_king

                piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))
                screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))


def valid_bishop_move(src_row, src_col, dest_row, dest_col):
    if abs(dest_row - src_row) == abs(dest_col - src_col):
        # Check if there are any obstructions along the diagonal path
        row_step = 1 if dest_row > src_row else -1
        col_step = 1 if dest_col > src_col else -1
            
        current_row = src_row + row_step
        current_col = src_col + col_step
            
        while current_row != dest_row and current_col != dest_col:
            # Check if there is a piece at each position along the diagonal path
            if playing_board[current_row][current_col] != " ":
                return False  # Bishop's path is obstructed
            current_row += row_step
            current_col += col_step
            
        return True  # Valid bishop move
            
    else:
        return False  # Invalid bishop move

def store_castle_conditions(rook, row, col):
    if rook == "R":
        if row == 7 and col == 0:
            white_left_rook_moved = True
        if row == 7 and col == 7:
            white_right_rook_moved = True
    
    if rook == "r":
        if row == 0 and col == 0:
            black_left_rook_moved = True
        if row == 0 and col == 7:
            black_right_rook_moved = True

def valid_rook_move(src_row, src_col, dest_row, dest_col):
    if src_row == dest_row:
        # check if there are any obstructions along the horizontal path
        col_step = 1 if dest_col > src_col else -1
        current_col = src_col + col_step
        
        while current_col != dest_col:
            # check if there is a piece at each position along the horizontal path
            if playing_board[src_row][current_col] != " ":
                return False  # rook's path is obstructed
            current_col += col_step
            
        store_castle_conditions(("R" if player == 1 else "r"), src_row, src_col)
        return True  # valid rook move
    
    elif src_col == dest_col:
        # vheck if there are any obstructions along the vertical path
        row_step = 1 if dest_row > src_row else -1
        current_row = src_row + row_step
        
        while current_row != dest_row:
            # vheck if there is a piece at each position along the vertical path
            if playing_board[current_row][src_col] != " ":
                return False  # rook's path is obstructed
            current_row += row_step
            
        store_castle_conditions(("R" if player == 1 else "r"), src_row, src_col)
        return True  # valid rook move
    
    else:
        return False  # invalid rook move


def is_square_attacked(row, col):
    # Define the possible directions for each type of piece
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Check if the square is attacked by a knight
    for move in knight_moves:
        x, y = row + move[0], col + move[1]
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            continue
        if player == 1 and playing_board[x][y] == "n":
            return True
        if player == 2 and playing_board[x][y] == "N":
            return True

    # Check if the square is attacked by a pawn
    pawn_direction = 1 if player == 1 else -1
    for move in [(pawn_direction, 1), (pawn_direction, -1)]:
        x, y = row + move[0], col + move[1]
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            continue
        if player == 1 and playing_board[x][y] == "p":
            return True
        if player == 2 and playing_board[x][y] == "P":
            return True

    # # Check if the square is attacked by a queen, rook, or bishop
    # for direction in directions:
    #     x, y = row + direction[0], col + direction[1]
    #     while 0 <= x < 8 and 0 <= y < 8:
    #         piece = board[x][y]
    #         if piece == attacking_color + "Q" or piece == attacking_color + "R":
    #             return True
    #         elif piece != " ":
    #             break
    #         x += direction[0]
    #         y += direction[1]

    # # Check if the square is attacked by a king
    # king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    # for move in king_moves:
    #     x, y = row + move[0], col + move[1]
    #     if 0 <= x < 8 and 0 <= y < 8 and board[x][y] == attacking_color + "K":
    #         return True

    return False


def valid_king_move(player, src_row, src_col, dest_row, dest_col):
    row_diff = abs(dest_row - src_row)
    col_diff = abs(dest_col - src_col)
    castle_direction = "right" if dest_col > src_col else "left"
    incremenent = 7 if player == 1 else 0

    # check castles and move the rook
    if col_diff == 2 and row_diff == 0:
        for move in moves:
            # check if the king has moved 
            if move[0] == "K" and player == 1:
                return False
            if move[0] == "k" and player == 2:
                return False
            
            if castle_direction == "right":
                # check if the right rook has moved
                if player == 1 and not white_right_rook_moved:
                    return False
                if player == 2 and not black_right_rook_moved:
                    return False
                
                if playing_board[incremenent][6] == " " and playing_board[incremenent][5] == " ":
                    playing_board[incremenent][7] = " "
                    playing_board[incremenent][5] = "R" if player == 1 else "r"
                    return True
                
                return False
                
            if castle_direction == "left":
                # check if the left rook has moved 
                if player == 1 and move[0] == "R" and move[1] == "a" and move[2] == "1":
                    return False
                if player == 2 and move[0] == "r" and move[1] == "a" and move[2] == "8":
                    return False

                if playing_board[incremenent][1] == " " and playing_board[incremenent][2] == " " and playing_board[incremenent][3] == " ":
                    playing_board[incremenent][0] = " "
                    playing_board[incremenent][3] = "R" if player == 1 else "r"
                    return True
                return False
            
    if row_diff <= 1 and col_diff <= 1 and not is_square_attacked(dest_row, dest_col):
        return True  # valid king move
    else:
        return False  # invalid king move


def check_move(player, piece, src_row, src_col, dest_row, dest_col):
    # check pawn move
    if piece == "P" or piece == "p":
        if player == 1:
            if src_col == dest_col:
                # first move can be 2 squares
                if src_row == 6:
                    if src_row - dest_row == 2: 
                        return playing_board[src_row - 1][src_col] == " " and playing_board[src_row - 2][src_col] == " "
                    if src_row - dest_row == 1:
                        return playing_board[src_row - 1][src_col] == " "
                    if src_row - dest_row > 2:
                        return False
                else:
                    if src_row - dest_row == 1:
                        return playing_board[src_row - 1][src_col] == " "
                    else:
                        return False
            elif src_row - dest_row == 1:
                return playing_board[dest_row][dest_col] != " "
            else:
                return False
            
        if player == 2:
            if src_col == dest_col:
                # first move can be 2 squares
                if src_row == 1:
                    if dest_row - src_row == 2:
                        return playing_board[src_row + 1][src_col] == " " and playing_board[src_row + 1][src_col] == " "
                    if dest_row - src_row == 1:
                        return playing_board[src_row + 1][src_col] == " "
                    if dest_row - src_row > 2:
                        return False
                else:
                    if dest_row - src_row == 1:
                        return playing_board[src_row + 1][src_col] == " "
                    else:
                        return False
            elif dest_row - src_row == 1:
                return playing_board[dest_row][dest_col] != " "
            else:
                return False
    
    # check knight move
    if piece == "N" or piece == "n":
        return ((dest_row == src_row - 2 and dest_col == src_col - 1) or
                (dest_row == src_row - 2 and dest_col == src_col + 1) or
                (dest_row == src_row - 1 and dest_col == src_col + 2) or
                (dest_row == src_row + 1 and dest_col == src_col + 2) or
                (dest_row == src_row + 2 and dest_col == src_col + 1) or
                (dest_row == src_row + 2 and dest_col == src_col - 1) or
                (dest_row == src_row + 1 and dest_col == src_col - 2) or
                (dest_row == src_row - 1 and dest_col == src_col - 2))
    
    # check bishop move
    if piece == "B" or piece == "b":
        # check if the number of rows moved is equal to the number of columns moved (diagonal move)
        return valid_bishop_move(src_row, src_col, dest_row, dest_col)
    
    # check rook move
    if piece == "r" or piece == "R":
        return valid_rook_move(src_row, src_col, dest_row, dest_col)

    # check queen move (moves like a rook or bishop)
    if piece == "q" or piece == "Q":
        return valid_bishop_move(src_row, src_col, dest_row, dest_col) or valid_rook_move(src_row, src_col, dest_row, dest_col)

    # check king move and move the rook if castles
    if piece == "k" or piece == "K":
        return valid_king_move(player, src_row, src_col, dest_row, dest_col)


def construct_move(piece, src_row, src_col, dest_row, dest_col):
    if piece == "K" or piece == "k":
        if abs(src_col - dest_col) == 2 and src_row - dest_row == 0:
            return "O-O" if dest_col > src_col else "O-O-O"
    move = piece + chr(src_col + 97) + str(abs(8 - src_row)) + chr(dest_col + 97) + str(abs(8 - dest_row))
    return move
            
            
# main game loop
while not game_over:
    clock.set_fps(FPS)

    for event in pygame.event.get():
        check_interrupt.check_user_interrupt(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            cell_col = mouse_position[0] // SQUARE_SIZE
            cell_row = mouse_position[1] // SQUARE_SIZE

            # white pieces
            if player == 1:
                if selected_piece == None:
                    if playing_board[cell_row][cell_col].isupper() and playing_board[cell_row][cell_col] != " ":
                        selected_piece = playing_board[cell_row][cell_col]
                        selected_piece_position = (cell_row, cell_col)
                else:
                    # deselect the piece
                    if (cell_row, cell_col) == selected_piece_position:
                        selected_piece_position = None
                        selected_piece = None
                    # select another piece
                    elif playing_board[cell_row][cell_col].isupper():
                        selected_piece = playing_board[cell_row][cell_col]
                        selected_piece_position = (cell_row, cell_col)
                    # move the piece
                    elif check_move(player, selected_piece, selected_piece_position[0], selected_piece_position[1], cell_row, cell_col):
                        # append move to the list
                        moves.append(construct_move(selected_piece, selected_piece_position[0], 
                                                    selected_piece_position[1], cell_row, cell_col))
                        # move the piece
                        playing_board[cell_row][cell_col] = selected_piece
                        playing_board[selected_piece_position[0]][selected_piece_position[1]] = " "
                        selected_piece_position = None
                        selected_piece = None
                        # change the player
                        player = 2
                        
            # black pieces
            else:
                if selected_piece == None:
                    if playing_board[cell_row][cell_col].islower() and playing_board[cell_row][cell_col] != " ":
                        selected_piece = playing_board[cell_row][cell_col]
                        selected_piece_position = (cell_row, cell_col)
                else:
                    # deselect the piece
                    if (cell_row, cell_col) == selected_piece_position:
                        selected_piece_position = None
                        selected_piece = None
                    # select another piece
                    elif playing_board[cell_row][cell_col].islower():
                        selected_piece = playing_board[cell_row][cell_col]
                        selected_piece_position = (cell_row, cell_col)
                    # move the piece
                    elif check_move(player, selected_piece, selected_piece_position[0], selected_piece_position[1], cell_row, cell_col):
                        # append move to the list
                        moves.append(construct_move(selected_piece, selected_piece_position[0], 
                                                    selected_piece_position[1], cell_row, cell_col))
                        # move the piece
                        playing_board[cell_row][cell_col] = selected_piece
                        playing_board[selected_piece_position[0]][selected_piece_position[1]] = " "
                        selected_piece_position = None
                        selected_piece = None
                        # change the player
                        player = 1
                        
            print(moves)
            # print(cell_row, cell_col)

    draw_board()
    draw_pieces()
    pygame.display.update()
