from grammarUtils import (
  getGrammar,
  cleanGrammar,
  printGrammar,
  
  toChumsky,
  toGreibach,
  toAutomaton,
)

grammarFilename = input('Cual es el nombre del Archivo?: ')

grammarFilename, grammar = getGrammar("chomsky.txt")
cleanGrammar(grammar)

toChumsky(grammar)
printGrammar(grammar, grammarFilename+'-Chomsky.txt')

toGreibach(grammar)
printGrammar(grammar, grammarFilename+'-Greibach.txt')

toAutomaton(grammar, grammarFilename+'-Automaton')
