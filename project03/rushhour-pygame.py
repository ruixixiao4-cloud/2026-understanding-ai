# ------------------------ FILL HERE ----------------------------------
from simpleai.search import astar, SearchProblem

class RushHour(SearchProblem):
    def __init__(self, initial_state):
        self.initial_state = initial_state

    def actions(self, state):
        tmp = state

        # ========= 게임판 생성 ====================================================
        
        # state가 문자열로 들어오기 때문에 보드판을 생성해 각 차들의 수직 수평 방향 구분 
        board = [[], [], [], [], [], []]
        
        for i in range(6):
            for j in range(6):
                if len(board[i]) == 6:
                    continue
                board[i].append(state[j])
            state = state[j+1:]
        
        horizontal = {} # 가로로 움직이는 차들의 딕셔너리
        vertical = {} # 세로로 움직이는 차들의 딕셔너리

        # ================ 각 차들이 수평, 수직 방향인지 나눠 주는 코딩 ==============

        # 수평 방향(가로)으로 움직이는 차들을 horizontal 딕셔너리에 추가
        # ex) horizontal = {"A" : [[0,1], [0,2]]....}
        for row in range(6):
            for col in range(5):
                char = board[row][col]
                if char == 'o':
                    continue
                if char == board[row][col + 1]:
                    if char in horizontal:
                        horizontal[char].append([row, col + 1])
                    else:
                        horizontal[char] = [[row, col], [row, col + 1]]            

        # 수직 방향(세로)으로 움직이는 차들을 vertical 딕셔너리에 추가
        # ex) vertical = {"B": [[0,1], [1,1]]...}
        for col in range(6):
            for row in range(5):
                char = board[row][col]
                if char == 'o':
                    continue
                if char == board[row+1][col]:
                    if char in vertical: 
                        vertical[char].append([row+1, col])
                    else:
                        vertical[char] = [[row, col], [row + 1, col]]


        # ========== 차가 이동할 수 있는 모든 경우의 수에 관한 코딩 ================

        # 각 문자들이 움직일 수 있는 경우의 수를 can_move리스트에 ("char", "이동 가능한 칸 수")같은 튜플 형태로 추가
        can_move = []

        # 수평 방향(가로)으로 움직일 수 차들의 action에 추가  
        for kr, rloc in horizontal.items():

            r = rloc[0][0] # 하나의 차가 공통적으로 가지는 row의 위치
            left_col = rloc[0][1] # 가장 왼쪽 column
            right_col = rloc[-1][1] # 가장 오른쪽 column

            for step in range(1, 5):
                if left_col - step < 0 or board[r][left_col-step] != 'o': # 보드판을 벗어나거나 빈칸이 아닌 경우 True
                    break
                can_move.append((kr, -step)) # 왼쪽으로 움직일 수 있는 경우의 수

            for step in range(1,5):
                if right_col + step > 5 or board[r][right_col+step] != 'o':
                    break
                can_move.append((kr, step)) # 오른쪽으로 움직일 수 있는 경우의 수

        # 수직 방향(세로)으로 움직일 수 있는 차들의 action
        for kc, cloc in vertical.items():

            c = cloc[0][1] # 하나의 차가 공통적으로 가지는 column의 위치
            top_col = cloc[0][0] # 가장 위의 위치
            bottom_col = cloc[-1][0] # 가장 아래의 위치

            for step in range(1, 5):
                if top_col - step < 0 or board[top_col-step][c] != 'o': # 수평방향에 조건과 거의 비슷
                    break
                can_move.append((kc, -step)) # 위로 움직일 수 있는 경우의 수

            for step in range(1, 5):
                if bottom_col + step > 5 or board[bottom_col+step][c] != 'o':
                    break
                can_move.append((kc, step)) # 아래로 움직일 수 있는 경우의 수
            
        state = tmp
        return can_move
        # 결과 예시 : can_move = [("A", 2), ("B", 1)....] -> ("막대의 문자", 이동가능한 칸수)의 튜플로 이루어진 리스트가 can_move가 됨.

    def result(self, state, action):
        pass

    def is_goal(self, state):
        pass

    def heuristic(self, state):
        pass
# ---------------------------------------------------------------------



import pygame, sys
pygame.init()

import numpy as np

# global variables (should be multiples of 6)
WIDTH, HEIGHT = 540, 540
MESSAGE_MARGIN = 40
red = (180, 10, 0)
blue = (0, 20, 245)
yellow = (255, 227, 56)
green = (0, 128, 0)
gray = (105, 105, 105)
purple = (160, 32, 240)
brown = (165,42,42)
scarlet = (17, 169,1)
white = (255, 255, 255)
black = (0, 0, 0)
boardcolor = [white, black]
playercolor = [ None, red, blue, yellow, green ] # border color of selected cells
font = pygame.font.SysFont("comicsans",18)
linecolor = white
prime_car = red
second_car = blue

# create window
screen = pygame.display.set_mode((WIDTH, HEIGHT+MESSAGE_MARGIN*3))
pygame.display.set_caption("RUSH HOUR")

state_input = "EBBCCCEooFGHAAoFGHooooGIoooooIoooDDI"

#with open("rush12.txt", "r") as f:
#    with open("rush12nox.txt", "w") as o:
#        lines = f.readlines()
#        for line in lines:
#            if 'x' not in line:
#                o.write(line)

import random
with open("rush10nox.txt", "r") as f:
    lines = f.readlines()
    min_move, state_input, _ = random.choice(lines).split()
    min_move = int(min_move)
    print("min move: {}, board: {}".format(min_move, state_input))


# game state
# 0: empty
# 1/2: red/blue of player 1
# 3/4: yellow/green of player 2
state = np.array([
    [  0,  0,  0,  0,  0,  0  ],
    [  0,  0,  0,  0,  0,  0  ],
    [  0,  0,  0,  0,  0,  0  ],
    [  0,  0,  0,  0,  0,  0  ],
    [  0,  0,  0,  0,  0,  0  ],
    [  0,  0,  0,  0,  0,  0  ],
], dtype=np.int16)

car_alphabet = [ 'o', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R' ]
car_idx      = { c:idx for idx, c in enumerate(car_alphabet) }
car_info     = {} # dictionary of car_num:{"cells":list of cell positions, "direction":tuple, "len":int }
red_car      = 1
selected_car = None

# winner at game over
winner = None
is_gameover = False
move_cnt = 0

# create a surface object, image is drawn on it.
CELL_WIDTH, CELL_HEIGHT = WIDTH/6, HEIGHT/6
hint_action = None
button_rect = None  # 버튼 영역을 저장할 변

def _button(txt, backgr, butcol, textcol):
    # button background
    rect = pygame.Rect( (0, HEIGHT), (WIDTH, MESSAGE_MARGIN) )
    pygame.draw.rect(screen, backgr, rect)
    # draw a rect button
    rect = pygame.Rect( (0 + 4, HEIGHT + 4), (WIDTH-8, MESSAGE_MARGIN-8))
    pygame.draw.rect(screen, butcol, rect, border_radius=8)
    # button message
    pos_text = font.render(txt, True, textcol)
    pos_rect = pos_text.get_rect()
    pos_rect.center = ( WIDTH/2, HEIGHT + MESSAGE_MARGIN/2 )
    screen.blit(pos_text, pos_rect)
    # 버튼 영역 반환
    button_rect = pygame.Rect( (0 + 4, HEIGHT + 4), (WIDTH - 8, MESSAGE_MARGIN - 8))
    return button_rect

def _message_margin(txt, backgr, textcol, y_offset=None):
    if y_offset is None:
        y_offset = HEIGHT + MESSAGE_MARGIN
    rect = pygame.Rect( (0, y_offset), (WIDTH, MESSAGE_MARGIN) )
    pygame.draw.rect(screen, backgr, rect)
    pos_text = font.render(txt, True, textcol)
    pos_rect = pos_text.get_rect()
    pos_rect.center = ( WIDTH/2, y_offset + MESSAGE_MARGIN/2 )
    screen.blit(pos_text, pos_rect)

def show_msg():
    global button_rect
    txt = "Show me the solution"
    button_rect = _button(txt, black, white, black)

    if is_gameover:
        txt = "Game over ({} moves / min move = {})".format(move_cnt, min_move)
    else:
        txt = "# of moves = {} (min move = {})".format(move_cnt, min_move)
    _message_margin(txt, black, white, y_offset=HEIGHT + MESSAGE_MARGIN)

    if hint_action is not None:
        car_char, delta = hint_action
        txt = f"Hint: Move car {car_char} by {delta} step(s)"
        _message_margin(txt, black, white, y_offset=HEIGHT + MESSAGE_MARGIN * 2)

def decode_board(code: str):
    state = np.zeros(shape=(6, 6), dtype=np.int16)
    car_info = dict()

    # translate the code string to 6x6 board
    for idx, c in enumerate(code):
        state[(idx // 6), (idx % 6)] = car_idx[c]
        if car_idx[c] > 0:
            if car_idx[c] in car_info.keys():
                car_info[car_idx[c]]["cells"].append(np.array(((idx // 6), (idx % 6)), dtype=np.int64))
            else:
                car_info[car_idx[c]] = dict()
                car_info[car_idx[c]]["cells"] = [ np.array(((idx // 6), (idx % 6)), dtype=np.int64) ]
    # compute the direction of cars ((1, 0): vertical, (0, 1): horizontal)
    # and their length
    for c, info in car_info.items():
        delta = np.array(info["cells"][1], dtype=np.int64) - np.array(info["cells"][0], dtype=np.int64)
        info["len"] = len(info["cells"])
        info["direction"] = delta
    
    return state, car_info

def encode_board(_state):
    ret = ''
    for i in range(6):
        for j in range(6):
            ret += car_alphabet[_state[i][j]]
    return ret

def draw_board(surf):
    # black background
    rect = pygame.Rect((0, 0), (WIDTH, HEIGHT))
    pygame.draw.rect(surf, black, rect)

    for i in range(6):
        for j in range(6):
            rect = pygame.Rect(
                (j * CELL_WIDTH, i * CELL_HEIGHT), (CELL_WIDTH, CELL_HEIGHT))
            pygame.draw.rect(surf, gray, rect, width=1)

    for c, info in car_info.items():
        # 빈 셀인지 체크
        if c > 0:
            col = prime_car if c == 1 else second_car
            # 힌트 차라면 다른 색으로 표시
            if hint_action is not None and c == car_idx[hint_action[0]]:
                col = purple
            # vertical
            if info["direction"][0] == 1:
                rect = pygame.Rect(
                        (info["cells"][0][1] * CELL_WIDTH + 5, info["cells"][0][0] * CELL_HEIGHT + 5), 
                        (CELL_WIDTH - 10, CELL_HEIGHT * info["len"] - 10))
                pygame.draw.rect(surf, col, rect, border_radius=8)
            # horizontal
            else:
                rect = pygame.Rect(
                        (info["cells"][0][1] * CELL_WIDTH + 5, info["cells"][0][0] * CELL_HEIGHT + 5), 
                        (CELL_WIDTH * info["len"] - 10, CELL_HEIGHT - 10))
                pygame.draw.rect(surf, col, rect, border_radius=8)
    
    if selected_car is not None:
        # vertical
        if car_info[selected_car]["direction"][0] == 1:
            rect = pygame.Rect(
                    (car_info[selected_car]["cells"][0][1] * CELL_WIDTH, car_info[selected_car]["cells"][0][0] * CELL_HEIGHT), 
                    (CELL_WIDTH, CELL_HEIGHT * car_info[selected_car]["len"]))
            pygame.draw.rect(surf, yellow, rect, width=3)
        # horizontal
        else:
            rect = pygame.Rect(
                    (car_info[selected_car]["cells"][0][1] * CELL_WIDTH, car_info[selected_car]["cells"][0][0] * CELL_HEIGHT), 
                    (CELL_WIDTH * car_info[selected_car]["len"], CELL_HEIGHT))
            pygame.draw.rect(surf, yellow, rect, width=3)

# given the selected car and clicked target cell,
# move the car
# return false if it is an invalid move
def make_move(selected_car: int, cell_pos: tuple):
    global state, car_info, move_cnt

    if state[tuple(cell_pos)] > 0:
        return False
    
    tar_pos = np.array(cell_pos, dtype=np.int64)
    car_pos, direction, car_len = car_info[selected_car]["cells"][0], \
                                  car_info[selected_car]["direction"], \
                                  car_info[selected_car]["len"]
    delta = tar_pos - car_pos

    # if tar_pos is not aligned with the car (horizontally or vertically)
    if delta[0] != 0 and delta[1] != 0:
        return False
    if delta[0] != 0 and direction[0] == 0:
        return False
    if delta[1] != 0 and direction[1] == 0:
        return False
    
    # if vertically downward,
    if delta[0] > 0:
        for i in range(car_len, delta[0]+1):
            if state[tuple(car_pos + i * direction)] > 0:
                return False
        for car_cell in car_info[selected_car]['cells']:
            state[tuple(car_cell)] = 0
        for car_cell in car_info[selected_car]['cells']:
            car_cell += direction * (delta[0] - car_len + 1)
            state[tuple(car_cell)] = selected_car
    # if vertically upward
    elif delta[0] < 0:
        for i in range(-1, delta[0]-1, -1):
            if state[tuple(car_pos + i * direction)] > 0:
                return False
        for car_cell in car_info[selected_car]['cells']:
            state[tuple(car_cell)] = 0
        for car_cell in car_info[selected_car]['cells']:
            car_cell += direction * delta[0]
            state[tuple(car_cell)] = selected_car
    # if horizontally rightward
    elif delta[1] > 0:
        for i in range(car_len, delta[1]+1):
            if state[tuple(car_pos + i * direction)] > 0:
                return False
        for car_cell in car_info[selected_car]['cells']:
            state[tuple(car_cell)] = 0
        for car_cell in car_info[selected_car]['cells']:
            car_cell += direction * (delta[1] - car_len + 1)
            state[tuple(car_cell)] = selected_car
    # if horizontally leftward
    elif delta[1] < 0:
        for i in range(-1, delta[1]-1, -1):
            if state[tuple(car_pos + i * direction)] > 0:
                return False
        for car_cell in car_info[selected_car]['cells']:
            state[tuple(car_cell)] = 0
        for car_cell in car_info[selected_car]['cells']:
            car_cell += direction * delta[1]
            state[tuple(car_cell)] = selected_car
    move_cnt += 1
    return True


def cell_coord(pos: tuple):
    # get row and col & return
    # note that y -> row number, x -> col number
    return (int(pos[1] / CELL_HEIGHT), int(pos[0] / CELL_WIDTH))

# game over if there is a 3 combo and each piece cannot be flipped anymore
def game_over():
    # last cell of red car is on the rightmost column of the board
    if car_info[red_car]['cells'][car_info[red_car]['len']-1][1] == 5:
        return True
    return False

state, car_info = decode_board(state_input)

running = True
while running:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if button_rect is not None and button_rect.collidepoint(pos):
                # 버튼이 클릭되었을 때
                current_state_str = encode_board(state)
                problem = RushHour(current_state_str)
                result = astar(problem)
                solution_actions = result.path()
                if len(solution_actions) > 1:
                    next_action = solution_actions[1][0]
                    hint_action = next_action
                else:
                    hint_action = None
            elif not is_gameover:
                if selected_car is None:
                    # calculate the clicked piece
                    cell_pos = cell_coord(pygame.mouse.get_pos())

                    # clicked out of board such as message box
                    if (cell_pos[0] <  0 or cell_pos[0] >= 6) or (cell_pos[1] < 0 or cell_pos[1] >= 6):
                        continue
                    selected_car = state[cell_pos] if state[cell_pos] != 0 else None
                    # 힌트 액션이 있고, 플레이어가 움직였다면 힌트 초기화
                    if hint_action is not None:
                        hint_action = None
                break
        elif event.type == pygame.MOUSEBUTTONUP and not is_gameover:
            if selected_car is not None:
                 # calculate the clicked piece
                cell_pos = cell_coord(pygame.mouse.get_pos())

                # clicked out of board such as message box
                if (cell_pos[0] <  0 or cell_pos[0] >= 6) or (cell_pos[1] < 0 or cell_pos[1] >= 6):
                    continue
                
                if make_move(selected_car, cell_pos):
                    if game_over():
                        is_gameover = True
                selected_car = None
                # 힌트 액션이 있고, 플레이어가 움직였다면 힌트 초기화
                if hint_action is not None:
                    hint_action = None
                break

    draw_board(screen)
    show_msg()
    pygame.display.update()


pygame.quit()
sys.exit()