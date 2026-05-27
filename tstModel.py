from model.model import Model

myModel = Model()
myModel.buildGraph(7, '2016-01-01', '2018-12-28')
nodes, edges = myModel.getGraphDetails()

print(f"Grafo con {len(nodes)} nodi e {len(edges)} archi")