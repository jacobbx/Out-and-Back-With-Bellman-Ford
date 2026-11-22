from edgegraph2 import *


def bellman_ford(graph, start, remote):
    if graph is None or start is None or remote is None:
        raise ValueError
    
    if not isinstance(graph, GraphEL):
        raise ValueError
    
    if not isinstance(start, VertexEL) or not isinstance(remote, VertexEL):
        raise ValueError
    
    if start not in graph.vertices() or remote not in graph.vertices():
        raise ValueError
    
    if any(edge.get_value() <= 0 for edge in graph.edges()):
        raise ValueError
    
    if start == remote:
        raise ValueError
        
    def bellman_path(graph, source, destination, visited):
        # set every entry to positive infinity
        # length = total number of vertices 
        distance = {vertex: float("inf") for vertex in graph.vertices()}
        
        # start at None
        # vertex to edge mapping
        vertex_came_from = {vertex: None for vertex in graph.vertices()}

        # set the distance to start to 0
        # we are here
        distance[source] = 0
        
        # loop through every edge in graph toatl vertices - 1 times
        for _ in range(len(graph.vertices()) - 1):
            # loop through every edge in graph
            for edge in graph.edges():
                if edge in visited:
                    continue
                
                tail = edge.tail()
                head = edge.head()
                edge_value = edge.get_value()
                # relaxation
                if distance[tail] + edge_value < distance[head]:
                    distance[head] = distance[tail] + edge_value
                    # print
                    # print(f"head: {distance[head]}")
                    vertex_came_from[head] = edge
                    # print
                    # print(f"vertex_came_from[head]: {vertex_came_from[head]}")

                if distance[head] + edge_value < distance[tail]:
                    distance[tail] = distance[head] + edge_value
                    # print
                    # print(f"tail: {distance[tail]}")
                    vertex_came_from[tail] = edge
                    # print
                    # print(f"vertex_came_from[tail]: {vertex_came_from[tail]}")
                    
        if distance[destination] == float("inf"):
            return None
        
        edge_list = []
        current_vertex = destination
        while current_vertex != source:
            edge_we_came_from = vertex_came_from[current_vertex]
            edge_list.append(edge_we_came_from)
            if edge_we_came_from.head() == current_vertex:
                current_vertex = edge_we_came_from.tail()
            else:
                current_vertex = edge_we_came_from.head()
                
        edge_list.reverse()
        
        return edge_list
    
    # start to remote
    edges_used = set()
    start_to_remote = bellman_path(graph, start, remote, edges_used)
    
    edges_used = set(start_to_remote)
    remote_to_start = bellman_path(graph, remote, start, edges_used)
    if remote_to_start is None:
        return tuple(start_to_remote), None
    
    return tuple(start_to_remote), tuple(remote_to_start)
    
    # https://www.youtube.com/watch?v=lyw4FaxrwHg
    # https://www.geeksforgeeks.org/dsa/bellman-ford-algorithm-dp-23/
    # https://coddy.tech/visualize/graphs/bellman-ford-algorithm
    # I did use Claude to help me with walking through the steps of the algorithm and understanding
    # what each step is doing and how the dictionaries are working, and to help me with testing and understanding 
    # how the outputs should look and why they are that way

if __name__ == "__main__":
    file_graph = parse_graph_file("simple_graph.txt")
    # vertexA = file_graph.vertices()[0]
    # vertexB = file_graph.vertices()[1]
    # vertexC = file_graph.vertices()[2]
    # vertexD = file_graph.vertices()[3]
    # start4 = 10
    # print(bellman_ford(file_graph, vertexA, vertexD))
    
    file_graph2 = parse_graph_file("sample_graph.txt")
    vertexA = file_graph2.vertices()[0]
    vertexB = file_graph2.vertices()[1]
    vertexC = file_graph2.vertices()[2]
    print(bellman_ford(file_graph2, vertexA, vertexC))
