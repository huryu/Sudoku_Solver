#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


# Define all point
PointTuple = [(i, j) for i in range(9) for j in range(9)]
#PointTuple


# In[3]:


Sudoku_array_Ans = np.array([0 for elm in range(81)]).reshape(9,9)


# In[4]:


Sudoku_array_Cand = np.array([None for elm in range(81)]).reshape(9,9)


# In[5]:


FilledPos = int(input("The num of filled position :"))


# In[6]:


print("Row is from 0 to 8. Col is from 0 to 8.")


# In[7]:


#for i in range(FilledPos):
#    Row_Col_FilledNum = input("Input the row_num col_num filled_num with space (e.g. 0 0 8)")
#    Row, Col, FilleNum = list(map(int, Row_Col_FilledNum.split(" ")))


# In[8]:


for i in range(FilledPos):
    Row_Col_FilledNum = input("Input the row_num col_num filled_num with space (e.g. 0 0 8)")
    Row, Col, FilledNum = list(map(int, Row_Col_FilledNum.split(" ")))
    Sudoku_array_Ans[Row,Col] = FilledNum


# In[12]:


# candidate of number on each position
for elm in PointTuple:
    Ans = Sudoku_array_Ans[elm]
    if Ans == 0:
        Cand = [k for k in range(1,10) if k != Ans]
        Sudoku_array_Cand[elm] = Cand
    else:
        Sudoku_array_Cand[elm] = [Ans]


# In[13]:


TileNum = sorted(list(set([(i // 3, j // 3) for i in range(9) for j in range(9)])))
TileNumDict = {ind:elm for ind, elm in enumerate(TileNum)}


# In[14]:


#TileNumDict


# In[15]:


SudokuTile = {}
SudokuTile[0] = [[i, j] for i in range(3) for j in range(3)]
SudokuTile[1] = [[i, j] for i in range(3) for j in range(3,6)]
SudokuTile[2] = [[i, j] for i in range(3) for j in range(6,9)]
SudokuTile[3] = [[i, j] for i in range(3,6) for j in range(3)]
SudokuTile[4] = [[i, j] for i in range(3,6) for j in range(3,6)]
SudokuTile[5] = [[i, j] for i in range(3,6) for j in range(6,9)]
SudokuTile[6] = [[i, j] for i in range(6,9) for j in range(3)]
SudokuTile[7] = [[i, j] for i in range(6,9) for j in range(3,6)]
SudokuTile[8] = [[i, j] for i in range(6,9) for j in range(6,9)]


# In[16]:


# CountZero means the number of not-decided position in Sudoku_array_Ans.
CountZero = len(Sudoku_array_Ans.flatten()) - np.count_nonzero(Sudoku_array_Ans.flatten())


# In[21]:


print("Blank on the start.")
print("")
print(Sudoku_array_Ans)


# In[22]:


print("")
print("The position to be filled is ",CountZero)


# In[19]:


#for Pos in [(0,7)]:
while CountZero > 0:
    # Restrict the candidate the number on each position from other postion numbers of same tile/row/column. 
    for Pos in PointTuple:
        if Sudoku_array_Ans[Pos] != 0:
            continue
        #continue

        TilePosVal = (Pos[0] // 3, Pos[1] // 3)
        #print(TilePosVal)

        TilePosKey = [key for key in TileNumDict.keys() if TileNumDict[key] == TilePosVal][0]
        #print(TilePosKey)
        #continue

        TileForPos = np.array([Sudoku_array_Ans[elm[0], elm[1]] for elm in SudokuTile[TilePosKey]])

        RawForPos = Sudoku_array_Ans[Pos[0],:]
        ColForPos = Sudoku_array_Ans[:,Pos[1]]

        Set_Cand = set(np.arange(1, 10)) - set(np.append(np.append(RawForPos, ColForPos), TileForPos))
        Cand_List = sorted(Set_Cand)

        Sudoku_array_Cand[Pos] = Cand_List
        #print(Cand_List)
        
        # if the number of candidate is only one (= unique), that is the answer.
        if len(Cand_List) == 1:
            Sudoku_array_Ans[Pos] = Cand_List[0]
            #print(Pos, Cand_List)

    #If the position is the only one that can accept one of the candidate's numbers, that number is the answer for that position. 
    #for Pos in [(1,7)]: # this point is just the test case
    for Pos in PointTuple:
        if Sudoku_array_Ans[Pos] != 0:
            continue
        #continue

        TilePosVal = (Pos[0] // 3, Pos[1] // 3)
        #print(TilePosVal)

        TilePosKey = [key for key in TileNumDict.keys() if TileNumDict[key] == TilePosVal][0]
        #print(TilePosKey)


        CandForPos = set(Sudoku_array_Cand[Pos])
        #print(CandForPos)
        #continue


        #Cand_TileForPos = np.array([Sudoku_array_Cand[elm[0], elm[1]] for elm in SudokuTile[TilePosKey]])
        Cand_TileForPos = [num for elm in SudokuTile[TilePosKey] for num in Sudoku_array_Cand[elm[0], elm[1]]]
        #print(Cand_TileForPos)

        Cand_RawForPos = [num for elm in Sudoku_array_Cand[Pos[0],:] for num in elm]
        Cand_ColForPos = [num for elm in Sudoku_array_Cand[:,Pos[1]] for num in elm]

        #Cand_Uniqueness
        Cand_num = [elm for elm in CandForPos if (Cand_TileForPos.count(elm) == 1) 
                                               or (Cand_RawForPos.count(elm) == 1) 
                                               or (Cand_ColForPos.count(elm) == 1)]

        #print(Cand_num)
        if len(Cand_num) == 1:
            #print(Pos, Cand_num)
            Sudoku_array_Cand[Pos] = Cand_num
            Sudoku_array_Ans[Pos] = Cand_num[0]
        # If there are more than 2 number for one position, something wierd occurs, so the code or input should be checked.
        if len(Cand_num) >= 2:
            print("ErrorCand2", Pos, Cand_num)
            
    CountZero = len(Sudoku_array_Ans.flatten()) - np.count_nonzero(Sudoku_array_Ans.flatten())


# In[27]:


print("The answer")
print("")
print(Sudoku_array_Ans)


# In[ ]:




