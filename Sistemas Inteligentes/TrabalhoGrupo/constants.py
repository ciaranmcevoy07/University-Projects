SERVER = 'desktop-hstrf6b.home'
PASSWORD = 'NOPASSWORD'

X_MAX = 100
Y_MAX = 100

EXAMPLE = 6
# 0: Parados;
# 1: Movimentos Aleatórios;
# 2: Score Attack (com Procura Aleatória);
# 3: Score Strategy (Ataque + Procura);
# 4: Score Strategy (Ataque + Procura), posições iniciais pré-definidas, as 2 equipas a procurar em cantos opostos;
# 5: Score Strategy (Ataque + Procura), posições iniciais pré-definidas, as 2 equipas a procurar nos outros cantos;
# 6: Score Strategy (Ataque + Procura), posições iniciais pré-definidas, ataque e procura;
# 7: Score Strategy (equipa 1) vs. Parados;
# 8: Score Strategy (equipa 1) vs. Movimentos Aleatórios;

TEAM_NAMES = ["red", "blue"]
N_SOLDIERS = 5

# Display
WIDTH, HEIGHT = 1000, 1000
SQUARE_SIZE = WIDTH // X_MAX
FPS = 60

WHITE = (255, 255, 255)
GREY = (150, 150, 150)
DARK_GREY = (100, 100, 100)
BLACK = (0, 0, 0)

GRID_COLOUR = DARK_GREY
BACK_COLOUR = BLACK

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

TEAMS = {0: RED, 1: BLUE, 2: GREEN}
