
	
from pddlToGraphs import *
from Planner import *
domain_file = 'domains/mini-indy-domain.pddl'
problem_file = 'domains/mini-indy-problem.pddl'



operators, objects, initAction, goalAction = parseDomainAndProblemToGraphs(domain_file, problem_file)
planner = PlanSpacePlanner(operators, objects, initAction, goalAction)
graph = planner[0]
flaw = graph.flaws.pop()


results = planner.newStep(graph, flaw)


graph = results.pop()