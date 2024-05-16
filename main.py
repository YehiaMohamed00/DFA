from pyvis.network import Network

graph = {}
# stores the number of vertices in the graph
vertices_no = 0
# Construct DFA
def DFA(M: tuple, string: str):
    # Print out the machine description
    print("Machine =", M)
    # Print out the input string
    print("Input string =", string, end="\n\n")
    # Instantiate all DFA's vertices
    for i in M[0]:
        add_vertex(i)

    # Instantiate all edges in DFA
    for i in M[2].keys():
        add_edge(i, M[2][i][0], M[1][0])
        add_edge(i, M[2][i][1], M[1][1])

    # Preview edges in the DFA
    #print_graph()
    # Typecast the string to list type to used append function
    string = list(string)
    # List of states visited along string evaluation
    route = []
    # NOTE: for debugging only
    #print("for debugging, the DFA structure->\n", graph, end="\n\n")
    # Append the initial state to the route
    route.append(M[3])
    # Follows along the DFA to reach last state
    while len(string) != 0:
        x = string.pop(0)
        y = route[-1]
        now = graph[y]
        for i in now:
            if i[-1] == x:
                route.append(i[0])

    print("trace route: \n", route, end="\n\n")
    # Checks whether the last state visited is a final state
    print("Acceptability: ")
    if route[-1] in M[4]:
        print("accepted")
    else:
        print("rejected")

    graph.clear()
    print("___________________________________________________________")
    return

# Add a vertex to the dictionary
def add_vertex(v):
    global graph
    global vertices_no
    if v in graph.keys():
        print("Vertex ", v, " already exists.")
    else:
        vertices_no += 1
        graph[v] = []

# Add an edge between vertex v1 and v2 with edge weight e
def add_edge(v1, v2, e):
    global graph
    # Check if vertex v1 is a valid vertex
    if v1 not in graph.keys():
        print("Vertex ", v1, " does not exist.")
    # Check if vertex v2 is a valid vertex
    elif v2 not in graph.keys():
        print("Vertex ", v2, " does not exist.")
    else:
        temp = [v2, e]
        graph[v1].append(temp)

# Print the graph
def print_graph():
    global graph
    print("DFA: ")
    for vertex in graph:
        for edges in graph[vertex]:
            # print(vertex, " -> ", edges[0], " transition on: ", edges[1])
            print(vertex, " --", edges[1], "--> ", edges[0])
    print()

def input_formatter(inp: str):
    inp = inp.replace(" ", "")
    inp = inp[1:-1].split(",")
    return tuple(inp)


m0 = "{q0, q1, q2, q3}"
#m1 = "{0,1}"
m1 = "{a,b}"
m3 = "q0"
m4 = "{q0}"

#machine1 = (("q0", "q1", "q2", "q3"), (0, 1), {"q0": ("q2", "q1"), "q1": ("q3", "q0"), "q2": ("q0", "q3"), "q3": ("q1", "q2")},  "q0", ("q0"))
machine1 = (input_formatter(m0), input_formatter(m1), {"q0": ("q2", "q1"), "q1": ("q3", "q0"), "q2": ("q0", "q3"), "q3": ("q1", "q2")},  m3, input_formatter(m4))
#in_string1 = "10011100"
#in_string1 = "abbaaabb"
in_string1 = "baabbbaa"
# Create DFA and evaluate acceptability of string
DFA(machine1, in_string1)

# _________________________________________________ #
# visualization
net = Network(height="60%", width="50%", directed=True)
net.set_edge_smooth('dynamic')

i = 0
for i in machine1[0]:
    if i in machine1[4]:
        net.add_node(i, label=str(i), color="blue")
    else:
        net.add_node(i, label=str(i), color="lightblue")

for i in machine1[2].keys():
    tmp = list(machine1[1])
    for j in machine1[2][i]:
        for k in machine1[1]:
            symb = tmp.pop(0)
            net.add_edge(i, j, label=symb, color="black")
            break

net.add_node("hidden", hidden=True)
net.add_edge("hidden", machine1[-2], color="black")
net.barnes_hut(gravity=-2000, central_gravity=0.3, spring_length=120, spring_strength=0.04, damping=0.09, overlap=1)
net.show("basic.html")
