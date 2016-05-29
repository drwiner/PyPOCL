from Graph import *
import copy

class ElementGraph(Graph):
	"""An element graph is a graph with a root element"""
	
	def __init__(self,id,type,name=None, Elements = set(), root_element = None, Edges = set(), Constraints = set()):
		super(ElementGraph,self).__init__(\
											id,\
											type,\
											name,\
											Elements,\
											Edges,\
											Constraints\
										)
		self.root = root
		
	def copyGen(self):
		yield copy.deepcopy(self)
		
	def getElementGraphFromElement(self, element, Type=ElementGraph):
		if self.root is element:
			return self
		
		return Type(element.id, \
					type='element %s' %subgraph, \
					name=self.name\
					self.rGetDescendants(element)\#Needs a set
					root=element\
					self.rGetDescendantEdges(element)\
					self.rGetDescendantConstraints(element)\
					)
			
	def mergeEdgesFromSource(self, other, edge_source = self.root, mergeable_edges):
		""" Treats all edges as unique, does not merge the edges, merges FROM edges"""
		if edge_source.merge(other.root) is None:
			return None
		new_incident_edges = {Edge(\
									edge_source, \
									edge.sink, \
									edge.label\
									) \
									for edge in mergeable_edges\
							}
		self.edges.union_update(new_incident_edges)
		for new_edge in new_incident_edges:
			self.elements.add(new_edge.sink)
			self.elements.union_update(other.rGetDescendants(new_edge.sink)) #Try using Generator
			
			self.edges.union_update(other.rGetDescendantEdges(new_edge.sink))
			self.constraints.union_update(other.rGetDescendantConstraints(new_edge.sink)
	
		return self	
			
	def mergeAt(self, other, edge_source = self.root):		
		return self.mergeFromEdges(other, edge_source, other.getIncidentEdges(other.root))
		
	def getConsistentEdgePairs(self, incidentEdges, otherEdges):
		return {(edge,other_edge) \
									for edge in incidentEdges \
									for other_edge in otherEdges \
												if edge.isCoConsistent(other)\
				}
				
	def getInconsistentEdges(self, other_edges, consistent_edge_pairs):
		"""Returns set, because parameter mergeable edges in mergeEdgesFromSource takes set"""
		return {other_edge \
					for other_edge in otherEdges \
						if other_edge not in \
							(oe for (e,oe) in consistent_edge_pairs\
						)\
				}
			
	def rMerge(self, other, self_element = self.root, other_element = other.root, consistent_merges = set()):
		""" Returns set of consistent merges, which are Edge Graphs of the form self.merge(other)""" 
		#self_element.merge(other_element)
		
		otherEdges = other.getIncidentEdges(other_element)
		
		#BASE CASE
		if len(otherEdges) == 0:
			return consistent_merges.add(self)
			
		
		consistent_edge_pairs = self.getConsistentEdgePairs(self.getIncidentEdges(self_element), \
															otherEdges\
															)

		#If they're all inconsistent, then let's just get to den, aye?
		if len(consistent_edge_pairs) == 0:
			to_merge = other.getElementGraphFromElement(other_element)
			if self.mergeAt(self_element,to_merge) is None:
				return consistent_merges
			return consistent_merges.add(self)
			
		#INDUCTION	
		
		#First, merge inconsistent other edges, do this on every path
		mergeEdgesFromSource(other, \
							self.element, \
							other_element, \
							getInconsistentEdges(\
												otherEdges,\
												consistent_edge_pairs\
												)\
							) 
		
		#Assimilation Merge: see if we can merge the sinks.
		num_copies = len(consistent_edge_pairs) #
		consistent_merges.union_update({\
										self.copyGen().rMerge(\
																other, \
																e.sink, \
																o.sink, \
																consistent_merges\
															) \
															for (e,o) in consistent_edge_pairs \
										})

		#Accomodation Merge: see if we can add the sink's element graph
		for (e,o) in consistent_edge_pairs:
			take_other = self.copyGen().mergeEdgesFromSource(other, \
															self_element, \
															other_element, \
															{o}\
															)
			consistent_merges = take_other.rMerge(\
													other, \
													e.sink, \
													o.sink, \
													consistent_merges\
												)
	
		return consistent_merges
		

def extractElementsubGraphFromElement(G, element, Type):
	Edges = G.rGetDescendantEdges(element)
	Elements = G.rGetDescendants(element)
	Constraints = G.rGetDescendantConstraints(element)
	return Type(element.id,\
				type = element.type, \
				name=element.name, \
				Elements, \
				root_element = element\
				Edges, \
				Constraints\
				)
	
def getElementGraphMerge(one,other):
	
	if not one.isCoConsistent(other):
		return set()
		
	
	possible_worlds = {element_graph for element_graph in {}}
		
	if one.root.name is None:
		if other.root.name is None:
			print('if this were a literal, needs a name')
		else:
			one.root.name = other.root.name	

	if type(one.root) == 'Literal':
		if one.root.num_args is None:
			if other.root.num_args is None:
				print('need to put num_args in literals')
				return None
			else:
				self.root.num_args = other.root.num_args
				
	if type(one.root) == 'Operator':
		preconditions = {edge for edge in }
		#For each pair of co-consistent preconditions (one.precondition, other.precondition), 
			#If they both have the same name,
				#Create new ElementGraphs EG1,EG2, where EG1 makes them the same precondition, and EG2 keeps them separated
		#Do same for each pair of effects.
			#Don't need to do this for consenting actor
	#Action, Condition, 
		""" BUT, then there will be a combinatorial explosion of different ElementGraphs for each permuation,
			especially more complex ElementGraphs.
			What if, for each element in an ElementGraph, we store a set of possible mergers?"""
				
				
		"""TODO: with literals, there are no edges with same label. With steps, there are. 
			With steps, consider the unnamed step which contains two same-named literals. (e.g. to preconditions (at x loc) and (at y loc))
			Where self has (at arg1 loc) and other has (at None loc). 
			Two options, combine the literals or let there be two preconditions in merged Condition.
			Ought we store a list of alternatives? Ought this method not be a class method?"""