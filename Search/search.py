# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
import sys
class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  from util import Stack
  start = problem.getStartState()
  s = Stack()
  visited=[]
  directions=[]
  v=None
  path=None
  for successor in problem.getSuccessors(start):
    s.push((successor,[successor]))
  while(not s.isEmpty()):
    v,path = s.pop()
    if problem.isGoalState(v[0]):
      break
    if v[0] not in visited:
      visited.append(v[0])
      neighbours = problem.getSuccessors(v[0])
      for neighbour in neighbours:
        if neighbour[0] not in visited:
          s.push((neighbour,path+[neighbour]))
  if v!=None:
    if problem.isGoalState(v[0]):
      for item in path:
        directions.append(item[1])

  

  return directions
  #util.raiseNotDefined()

def breadthFirstSearch(problem):
  from util import Queue
  start = problem.getStartState()
  q = Queue()
  visited = []
  directions = []
  v=None
  path=None
  for successor in problem.getSuccessors(start):
    q.push((successor,[successor]))
  while (not q.isEmpty()):
    v,path = q.pop()
    if problem.isGoalState(v[0]):
      break
    if v[0] not in visited:
      visited.append(v[0])
      neighbours = problem.getSuccessors(v[0])
      for neighbour in neighbours:
        if neighbour[0] not in visited:
          q.push((neighbour,path+[neighbour]))
  if v!=None:
    if problem.isGoalState(v[0]):
      for item in path:
        directions.append(item[1])
  return directions

      
def uniformCostSearch(problem):
  start = problem.getStartState()
  closednodes=[]
  opennodes=[]
  directions=[]
  v=None
  path=None
  for successor in problem.getSuccessors(start):
    opennodes.append((successor,[successor]))
  while (len(opennodes)>0):
    v=None
    path=None
    minn = sys.maxint
    for item in opennodes:
      if item[0][2]<minn:
        minn = item[0][2]
        v=item[0]
        path =item[1]
    opennodes.remove((v,path))
    if problem.isGoalState(v[0]):
      break
    if v[0] not in closednodes:
      closednodes.append(v[0])
      neighbours = problem.getSuccessors(v[0])
      for neighbour in neighbours:
        if neighbour[0] not in closednodes:
          check =False
          node = None
          for item in opennodes:
            if neighbour[0] == item[0][0]:
              check=True
              node=item      
          if (check==True):
            if node[0][2]>neighbour[2]:
              opennodes.append((neighbour,path+[neighbour]))
              opennodes.remove(node)
          else:
            opennodes.append((neighbour,path+[neighbour]))
  if v!=None:
    if problem.isGoalState(v[0]):
      for item in path:
        directions.append(item[1])
  return directions

def nullHeuristic(state, problem=None):
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  start = problem.getStartState()
  closednodes=[]
  opennodes=[]
  directions=[]
  v=None
  path=None
  for successor in problem.getSuccessors(start):
    tuple = (successor[0], successor[1], successor[2], heuristic(successor[0],problem))
    opennodes.append((tuple,[successor[1]]))
  while (len(opennodes)>0):
    v=None
    path=None
    minn = sys.maxint
    for item in opennodes:

      if item[0][2]+item[0][3]<minn:
        minn = item[0][2] + item[0][3]
        v=item[0]
        path =item[1]
    opennodes.remove((v,path))
    if problem.isGoalState(v[0]):
      break
    if v[0] not in closednodes:
      closednodes.append(v[0])
      neighbours = problem.getSuccessors(v[0])
      for neighbour in neighbours:
        if neighbour[0] not in closednodes:
          check =False
          node = None
          for item in opennodes:
            if neighbour[0] == item[0][0]:
              check=True
              node=item      
          if (check==True):
            if node[0][2]>neighbour[2]:
              opennodes.append(((neighbour[0],neighbour[1],v[2]+neighbour[2],heuristic(neighbour[0],problem)),path+[neighbour[1]]))
              opennodes.remove(node)
          else:
            opennodes.append(((neighbour[0],neighbour[1],v[2]+neighbour[2],heuristic(neighbour[0],problem)),path+[neighbour[1]]))
  if v!=None:
    if problem.isGoalState(v[0]):
      for item in path:
        directions.append(item)
  return directions
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch