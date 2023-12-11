import pygame


pieces_image = pygame.image.load("./chess_pieces/chess.png")
piece_size = (128, 128)
rows = 2
columns = 6
pieces = []

for row in range(rows):
    for col in range(columns):
        x = col * piece_size[0]
        y = row * piece_size[1]
        piece_rect = pygame.Rect(x, y, piece_size[0], piece_size[1])
        piece = pieces_image.subsurface(piece_rect)
        pieces.append(piece)

black_pawn = pieces[0]
black_knight = pieces[1]
black_bishop = pieces[2]
black_rook = pieces[3]
black_queen = pieces[4]
black_king = pieces[5]
white_pawn = pieces[6]
white_knight = pieces[7]
white_bishop = pieces[8]
white_rook = pieces[9]
white_queen = pieces[10]
white_king = pieces[11]
