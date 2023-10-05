import streamlit as st
import ast
import pandas as pd
def myprint(x):
    st.write(x)
    
type_names   = {
    ast.AST : "ast",
    list : "list",
    str : "str",
    int : "int",
}
    
def get_name_of_type(node):
    # lookups up a type name
    for t in type_names :
        if isinstance(node, t):
            return type_names[t]
    return None

lookups = {} # will be pop

class Task:
    NEXT=1
    
    def __init__(self, name, example):
        self.number = self.NEXT
        self.NEXT=self.NEXT+1
        self.name = name
        self.example = example
    def __repr__(self):
        return f"Task[{self.number}]({self.name})={self.example};"


def register_node_type(node_type):
    """Decorator to register a visit function for a specific node type."""
    def decorator(func):
        lookups[func.__name__] = func
        return func
    return decorator

class Context:
    def __init__(self,data):
        self.data= data
        
    def streamlit(self):
        ret = {}
        for x in self.data:
            y = self.data[x]
            if hasattr(y,"streamlit"):
                ret[x] = y.streamlit()
            else:
                #now we want to pull in hierarchy around this. 
                ret[x] = "std:" + self.rec_context() + str(y) # +str(dir(y))
        return ret
    
    def rec_context(self):

        parent = ""
        if "context" in self.data:
            parent= str(self.data["context"])
            #.rec_context()

        return f"Recursive context around node {self} self:{str(self)} data:{str(self.data)} parent:{parent}"
    
    def depth(self):
        if "depth" in self.data:
            return self.data["depth"]
        if "context" in self.data:
            return self.data["context"]["depth"]
        else:
            raise Exception(self.data)
        
    def node(self):
        if "node" in self.data:
            return self.data["node"]
        
class Enum(Context):
    def __init__(self,data):
        super().__init__(data)
        
    def streamlit(self):
        ret = super().streamlit()
        # value = ret[]
        return ret
        
def create_enum(count, value, depth, context):
    return Enum({
        "depth" : depth,
        "count": count,
        "context": context,
        "value" : value
    })
    
@register_node_type(list)
def visit_node_list(context):
    ret = {
        "type":"list",
        "elements":[]
    }
    node_list = context.node()    
    
    for c,node in enumerate(node_list):
        c1 = Context({
            "context":context,
            "enumerate":create_enum(
                c,
                node,
                depth=context.depth()+1,
                context=context
            )
        }
                     )
        r = visit_ast_context(c1, depth=context.depth())
        ret["elements"].append([c1.streamlit(),r])
    return ret
    
        
tasks = {}
def task(name,example):
    if name not in tasks:
        tasks[name] = Task(name, example)
        st.write("task:", name, tasks[name])
    return tasks[name]

def dispatch(data):
    operation= data["operation"]
    match = data["match"]
    target = operation + "_" +match
    if target in lookups:
        context = Context(data)
        return lookups[target](context)
    else:
        return  task(f"Design an implementation of dispatch for op {operation} to do on {target} as standalone function named {target} registered in lookup dictonary",
                     f"for example with {parent} at pos {pos} wtih node {node} ")
    
def visit_field_abstract(parent, pos, name, node, depth, match):
    indent = "  " * depth
    #myprint(f"{indent}Type: {type(parent).__name__} field={pos}  name={name} node={node} match={match}")
    context = dict(
        parent=parent,
        id_parent = id(parent),
        pos       = pos,
        name      = name,
        id_node   = id(node),
        nodestr   = str(node),
        node_type = str(type(node)),
        depth     = depth,
        match     = match
    )
    
    # now execute the dispatch
    node_recurse   = dispatch(
        {
            "operation":"visit_node",
            "match":match,
            "node": node,
            "context":context
        }
    )
    # now add in the recursive result
    context["node_recurse"] =node_recurse
    return context
    
def visit_field_template(parent, pos, name, node, depth):
    # switch on type of node and dispatch
    #select the function based on type of node
    maybe_name = get_name_of_type(node)
    return visit_field_abstract(parent, pos, name, node, depth, maybe_name)

def visit_ast_context(cnode, depth):
    node = cnode.node()
    if node:
        return visit_ast(node, depth=depth)
    else:
        return {"None":1}
    
def visit_ast(node, depth=0):
    position = 0
    frame = []
    for field_name, field_value in ast.iter_fields(node):
        position = position + 1
        data = visit_field_template(node, position, field_name, field_value, depth)
        frame.append(data)

    #st.dataframe(df)
    ##now group by parent
    #st.dataframe(df.groupby(["id_parent"]))
    return frame

expression = st.text_area("Enter an expression:")

# Interpret and display the result when the user clicks a button
if st.button("Interpret"):
    tree = ast.parse(expression)
    result =   visit_ast(tree)
    st.write("Interpreted Result:", result)
