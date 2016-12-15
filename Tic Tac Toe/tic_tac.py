
# coding: utf-8

# In[1]:

import numpy as np
import copy

# In[2]:

def is_board_full(board):
    flat_board = np.ndarray.flatten(board)
    for cell in flat_board:
        if cell not in ['X','O']:
            return False
    return True


# In[5]:

def map_input(ip):
    
    if ip == 1:
        return (0,0)
    if ip == 2:
        return (0,1)
    if ip == 3:
        return (0,2)
    
    if ip == 4:
        return (1,0)
    if ip == 5:
        return (1,1)
    if ip == 6:
        return (1,2)
    
    if ip == 7:
        return (2,0)
    if ip == 8:
        return (2,1)
    if ip == 9:
        return (2,2)
    
    else:
        return (-1,-1)


# In[20]:

def get_empty_indices(board):
    rows = board.shape[0]
    cols = board.shape[1]
    
    empty_indices = []
    for r_id in range(rows):
        for c_id in range(cols):
            if board[r_id,c_id] not in ['X','O']:
                empty_indices.append((r_id,c_id))    
    return empty_indices


# In[15]:

def get_other_type(_type):
    if _type == 'X':
        return 'O'
    else:
        return 'X'


# In[16]:

def get_cnt(arr,char):
    cnt = 0
    for x in arr:
        if x == char:
            cnt += 1
    return cnt


# In[17]:

def get_utility(board):
    ''' if   X won and O not won => +1
        elif O won => -1
        else draw  =>  0
    '''
    rows = board.shape[0]
    cols = board.shape[1]    
    
    #Loss row check
    for r in range(rows):     
        if get_cnt(board[r],'O') == rows:
            return -1

    #Loss col check
    for c in range(cols):             
        if get_cnt(board[:,c:c+1],'O') == cols:
            return -1    
    
    
    #Loss left diag check
    ld = board.diagonal()
    if get_cnt(ld,'O') == cols:
        return -1
    
    #Loss right diag check
    rd = np.fliplr(board).diagonal()
    if get_cnt(rd,'O') == cols:
        return -1
    
    
    
    #Win row check
    for r in range(rows):     
        if get_cnt(board[r],'X') == rows:
            return +1

    #Win col check
    for c in range(cols):             
        if get_cnt(board[:,c:c+1],'X') == cols:
            return +1        
    
    #Win left diag check
    ld = board.diagonal()
    if get_cnt(ld,'X') == cols:
        return +1
    
    #Win right diag check
    rd = np.fliplr(board).diagonal()
    if get_cnt(rd,'X') == cols:
        return +1
    
    return 0


# In[18]:

def fill_board(orig_board,_type):
    
    board = copy.deepcopy(orig_board)
    utility = get_utility(board)    
    
    if utility in [1,-1] or is_board_full(board) :
        #print get_utility(board), board, '\n'               
        return utility,0
    else:
        empty_indices = get_empty_indices(board)
        
        util_queue = []
        for empty_idx in empty_indices:
            r = empty_idx[0]
            c = empty_idx[1]
            board[r,c] = _type            
            other_type = get_other_type(_type)            
            util,idx = fill_board(board,other_type)
            util_queue.append(util)
            board[r,c] = ''            
        
        #if len(util_queue) == 1:
         #   util_queue.append(util_queue[0])
        if _type == 'X':
            _max = max(util_queue)
            return _max, util_queue.index(_max)
        else:
            _min = min(util_queue)
            return _min, util_queue.index(_min)


# In[28]:

def think_and_play(orig_board):
    
    util,pos = fill_board(orig_board,'X')

    if len(get_empty_indices(orig_board)) != 0:        
        row = get_empty_indices(orig_board)[pos][0]
        col = get_empty_indices(orig_board)[pos][1]

        orig_board[row,col] = 'X'
        return orig_board
    else:
        return orig_board


# In[31]:

def main():
    
    orig_board = np.array(
    [['','',''],
     ['','',''],
     ['','','']])
    
    print('3*3 TIC TAC TOE\n')    
    print(orig_board)

    while(get_utility(orig_board) not in [1,-1] and is_board_full(orig_board) == False):    
        try:
            ip=int(input('Enter the position of \'O\' between 1-9 \n'))
            if ip == -1:
                break
            mat_pos = map_input(ip)    
            if orig_board[mat_pos[0],mat_pos[1]] in ['X','O']:
                print('Position not empty. Enter a valid empty position\n')
                continue
            orig_board[mat_pos[0],mat_pos[1]] = 'O'
            print('Your move :\n',orig_board,'\n')
            orig_board = think_and_play(orig_board)
            print('Comp move :\n',orig_board,'\n')
        except ValueError:
            print("Enter a valid num b/w 1-9\n")

    if get_utility(orig_board) == 1:
        print('GAME OVER. AI Won!')
    elif get_utility(orig_board) == -1:
        print('GAME OVER. You Won!')
    else:
        print('GAME OVER. Draw!')


# In[32]:

if __name__ == "__main__":
    main()


# In[ ]:



