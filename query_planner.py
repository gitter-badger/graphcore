"""
This QueryPlanner will be very nieve.  Its role is to convert a CallGraph into
a QueryPlan
"""

from .query_plan import QueryPlan


class CallGraphIterator(object):
    def __init__(self, call_graph):
        self._call_graph = call_graph

        # contains the python object id of nodes which have been grounded
        self._grounded = set() 

    def _is_grounded(self, node):
        """ Retursn true if node is in _grounded or if all incoming nodes
        are """

        if id(node) in self._grounded:
            return True

        nodes = node.incoming_nodes()
        print 'incoming', node.name, [n.name for n in nodes]
        if len(nodes) == 0:
            print 'no incoming', node.name
            return True
        else:
            return all(id(n) in self._grounded for n in nodes)

    def _ground(self, node):
        """ Add node to the _grounded set """
        self._grounded.add(id(node))

    def __iter__(self):
        # local copy of set that we can modify
        nodes = self._call_graph.nodes.copy()

        # if a node is grounded, add it to the plan
        # iterate over a copy so that we can remove while we go
        while len(nodes):
            grounded_node = False
            for node in nodes.copy():
                if self._is_grounded(node):
                    grounded_node = True
                    yield node
                    nodes.remove(node)
                    self._ground(node)

            if not grounded_node:
                raise ValueError(
                    'call graph iterator infinite loop: {nodes}'.format(
                        nodes=nodes
                    )
                )


class QueryPlanner(object):
    def __init__(self, call_graph, query):
        """
        query is necessary becuase the QueryPlan execution uses it to seed the
        state of the ResultSet object.
        """
        self.call_graph = call_graph
        self.plan = QueryPlan(query, call_graph.output_paths())

    def plan_query(self):
        for node in CallGraphIterator(self.call_graph):
            self.plan.append(node)

        return self.plan