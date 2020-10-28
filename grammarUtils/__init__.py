from graphviz import Digraph

newSymbolCounter = 1

def getGrammar(filename):
  #Open File
  with open(filename) as file:
    stream = file.readlines()
    stream = [elem.replace('\n', '') for elem in stream]

    #Save Generators and Productions
    grammarProd = {}
    for elem in stream:
      gen, product = elem.split('->')
      productions = product.split('|')
      grammarProd[gen] = productions
  return filename[:-4], grammarProd

def deleteUnusefulProductions(grammar):
  terminals = []
  #Find terminal Gens
  for gen, prods in grammar.items():
    for prod in prods:
      terminal = True
      for key in grammar.keys():
        if key in prod:
          terminal = False
      if terminal:
        terminals.append(gen)

  for gen, prods in grammar.items():
    for prod in prods:
      for elem in terminals:
        if elem in prod and gen not in terminals:
          terminals.append(gen)

  #Delete Non Terminal generators
  terminalGens = set(terminals)
  generators = set(grammar.keys())
  nonTerminalGens = generators-terminalGens
  for gen in nonTerminalGens:
    for k, v in grammar.items():
      for prod in v:
        if gen in prod:
          v.remove(prod)
    del(grammar[gen])

  # Delete unreachable productions
  reachable = set(['S'])
  for gen, prods in grammar.items():
    for prod in prods:
      for char in prod:
        if char in grammar.keys() and char != gen:
          reachable.add(char)
  generators = set(grammar.keys())
  unreachable = generators - reachable
  for gen in unreachable:
    del(grammar[gen])
  
  # Delete unexistent productions:
  for gen, prods in grammar.items():
    for prod in prods:
      for char in prod:
        if char in grammar.keys() and grammar[char] == ['']:
          prods.remove(prod)

def getEpsilonGens(grammarProd):
  #Chech unitary Productions
  replaceGens = {}
  for gen, prods in grammarProd.items():
    for prod in prods:
      if len(prod) == 0 and prod not in grammarProd.keys():
        if replaceGens.get(gen, None):
          replaceGens[gen].append(prod)
        else:
          replaceGens[gen] = [prod]
  #Delete Unitary Productions from Generator
  for replaceGen in replaceGens.keys():
    for prod in replaceGens[replaceGen]:
      grammarProd[replaceGen].pop(grammarProd[replaceGen].index(prod))
  return replaceGens

def getUnitaryGens(grammarProd):
  #Chech unitary Productions
  replaceGens = {}
  for gen, prods in grammarProd.items():
    for prod in prods:
      if len(prod) == 1 and prod not in grammarProd.keys() and gen != 'S':
        if replaceGens.get(gen, None):
          replaceGens[gen].append(prod)
        else:
          replaceGens[gen] = [prod]

  #Skip if not unitary
  gensToSkip = []
  for replaceGen in replaceGens.keys():
    for prod in grammarProd[replaceGen]:
      for char in prod:
        if len(prod) > 1 and char in grammarProd.keys() and replaceGen not in gensToSkip:
          gensToSkip.append(replaceGen)
  for gen in gensToSkip:
    del(replaceGens[gen])
  #Delete Unitary Productions from Generator
  for replaceGen in replaceGens.keys():
    for prod in replaceGens[replaceGen]:
      grammarProd[replaceGen].pop(grammarProd[replaceGen].index(prod))
  return replaceGens

def replaceProd(grammarProd, replaceGens):
  toDelete = []
  for replaceGen in replaceGens.keys():
    while len(replaceGens[replaceGen]) > 0:
      replaceProd = replaceGens[replaceGen][0]

      for gen, prods in grammarProd.items():
        if replaceGen in prods:
          prods.append(replaceProd)
          continue
        
        for prod in prods:
          doReplace = False
          for char in prod:
            if char == replaceGen:
              doReplace = True
          if doReplace:
            newProd = prod.replace(replaceGen, replaceProd)
            prods.append(newProd)

      replaceGens[replaceGen].pop(0)
      if len(replaceGens[replaceGen]) == 0:
        toDelete.append(replaceGen)
  for elem in toDelete:
    del(replaceGens[elem])

def deleteEmptyGens(grammarProd):
  toDelete = []
  #Detect empty gens
  for gen, prod in grammarProd.items():
    if len(prod) == 0:
      toDelete.append(gen)
  #Delete empty gens
  for elem in toDelete:
    for gen, prod in grammarProd.items():
      if elem in prod:
        prod.pop(prod.index(elem))
    del(grammarProd[gen])

def deleteEpsilonAndDuplicates(grammarProd):
  for gen, prod in grammarProd.items():
    if '' in prod:
      prod.pop(prod.index(''))
    else:
      duplicates = []
      for i in range(len(prod)):
        for j in range(i+1, len(prod)):
          if prod[i] == prod[j]:
            duplicates.append(j)
      for elem in duplicates:
        prod.pop(elem)

def cleanGrammar(grammar):
  # Get epsilon productions
  epsilonGens = getEpsilonGens(grammar)
  # Replace epsilon productions
  replaceProd(grammar, epsilonGens)
  # Get unitary productions
  unitaryGens = getUnitaryGens(grammar)
  # Replace unitary productions
  replaceProd(grammar, unitaryGens)
  # Check for epsilon productions again
  epsilonGens = getEpsilonGens(grammar)
  # Replace epsilon productions if found
  replaceProd(grammar, epsilonGens)
  # Delete empty productions
  deleteUnusefulProductions(grammar)
  # Delete duplicate productions and epsilon productions
  deleteEpsilonAndDuplicates(grammar)
  # Return Clean Grammar
  return grammar

def printGrammar(grammar, name):
  with open(name, 'w') as f:
    for gen, prods in grammar.items():
      f.write('{}->'.format(gen))
      for prod in prods:
        if prod == prods[-1]:
          f.write(prod+'\n')
        else:
          f.write('{}|'.format(prod))

def toChumsky(grammar):
  newProd = {}
  #Step 1
  for gen, prods in grammar.items():
    for prod in prods:
      for char in prod:
        if char not in grammar.keys() and char not in newProd.keys():
          newProd[char] = str(len(newProd.keys()))
  for gen, prods in grammar.items():
    toRemove = []
    for prod in prods:
      for char in prod:
        if char in newProd.keys():
          new = prod.replace(char, newProd[char])
          if new not in prods:
            prods.append(new)
          toRemove.append(prod)
    for prod in toRemove:
      if prod in prods:
        prods.remove(prod)
  for nProd, nGen in newProd.items():
    grammar[nGen] = [nProd]

  newProd = {}
  #Step 2
  for gen, prods in grammar.items():
    for prod in prods:
      
      if len(prod) > 2:
        while len(prod) > 2:
          newProd['C_'+str(len(newProd.items()))] = prod[1:]
          prod = newProd['C_'+str(len(newProd.items())-1)]
  
  inorderNewGens = list(newProd.keys())
  inorderNewGens.reverse()

  for nGen in inorderNewGens:
    for gen in newProd.keys():
      if newProd[nGen] in newProd[gen] and nGen != gen:
        newProd[gen] = newProd[gen].replace(newProd[nGen], nGen)
  
  for nGen, nProd in newProd.items():
    for gen, prods in grammar.items():
      toRemove = []
      for prod in prods:
        if nProd in prod:
          prods.append(prod.replace(nProd, nGen))
          toRemove.append(prod)
      for elem in toRemove:
        prods.remove(elem)
    grammar[nGen] = [nProd]

def deleteRecursivity(grammar):
  global newSymbolCounter
  newProds = {}

  for gen, prods in grammar.items():
    alphaProds = []
    betaProds = []
    
    for prod in prods:
      if prod != '' and prod[0] == gen:
        alphaProds.append(prod.replace(gen,'',1))
      else:
        betaProds.append(prod)

    if len(alphaProds) > 0:
      betaProdsTmp = [i for i in betaProds]
      newSymbol = 'Z_'+str(newSymbolCounter)
      for elem in betaProdsTmp:
        betaProds.append(elem+newSymbol)

      for elem in alphaProds:
        if newProds.get(newSymbol, None):
          newProds[newSymbol].append(elem)
          newProds[newSymbol].append(elem+newSymbol)
        else:
          newProds[newSymbol] = [elem, elem+newSymbol]
      
      for elem in betaProds:
        if newProds.get(gen, None):
          newProds[gen].append(elem)
        else:
          newProds[gen] = [elem]

      newSymbolCounter+=1

  for gen in newProds.keys():
    grammar[gen] = newProds[gen]

def replace(grammar, genNum):
  for gen, prods in grammar.items():
    needReplace = True 
    actualPos = 0

    while needReplace:
      toAdd = []
      toRemove = []
      actualProds = [i for i in grammar[gen]]
      prod = actualProds[0]

      if prod[0] in genNum.keys() and genNum[prod[0]]<genNum[gen]:
        toRemove.append(prod)
        for newProd in grammar[prod[0]]:
          toAdd.append(prod.replace(prod[0], newProd, 1))

        oldProds = [i for i in actualProds]
        grammar[gen] = []
        for elem in toRemove:
          if elem in oldProds:
            oldProds.remove(elem)


        for elem in toAdd:
          grammar[gen].append(elem)
        for elem in oldProds:
          grammar[gen].append(elem)
        
              
      else:
        needReplace = False

def substitution(grammar):
  queue = []
  for gen, prods in grammar.items():
    isComplete = True
    for prod in prods:
      if prod[0] in grammar.keys():
        isComplete = False
    if isComplete:
      queue.append(gen)
  
  index = 0
  
  while index < len(queue):
    for gen, prods in grammar.items():
      toAdd = []
      toRemove = []
      for prod in prods:
        if prod[0] == queue[index]:
          toRemove.append(prod)
          for elem in grammar[queue[index]]:
            toAdd.append(prod.replace(queue[index], elem, 1))
      
      oldProds = grammar[gen]
      grammar[gen] = []

      for elem in toAdd:
        grammar[gen].append(elem)
      for elem in oldProds:
        grammar[gen].append(elem)
      
      for elem in toRemove:
        if elem in grammar[gen]:
          grammar[gen].remove(elem)
      
      for gen, prods in grammar.items():
        isComplete = True
        for prod in prods:
          if prod[0] in grammar.keys():
            isComplete = False
        if isComplete and gen not in queue:
          queue.append(gen)
      
    index += 1

def toGreibach(grammar):
  genNum = { v:k+1 for k,v in enumerate(grammar.keys())}
  replace(grammar, genNum)
  deleteRecursivity(grammar)
  substitution(grammar)

def toAutomaton(grammar, filename):

  transitions = ''

  for gen, prods in grammar.items():
    for prod in prods:
      if prod[1:] != '':
        transitions += '{0},{1}/{2}\n'.format(prod[0], gen, prod[1:])
      else:
        transitions += '{0},{1}/{2}\n'.format(prod[0], gen, 'ε')

  dot = Digraph(comment='Automaton')
  dot.node('S', 'q0')
  dot.node('A', 'q1')
  dot.attr('node', shape='doublecircle')
  dot.node('B', 'qf')
  
  dot.edge('S', 'A', label='ε,┴/S┴')
  dot.edge('A', 'A', label=transitions)
  dot.edge('A', 'B', label='ε,┴/ε')

  dot.render(filename, view=False)
