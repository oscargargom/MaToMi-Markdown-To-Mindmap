
# Github @oscargargom
# Version 1.0-

import sys
import graphviz

def parse_markdown(markdown):
    lines = markdown.strip().split('\n')
    data = []
    stack = []
    
    for line in lines:
        if not line.strip():
            continue  # Ignore empty lines
        level = line.count('#')
        title = line.lstrip('# ').strip()
        
        if level > 0:
            node = {'title': title, 'children': []}
            
            # Adjust the stack based on the level
            while len(stack) >= level:
                stack.pop()
            
            if stack:
                stack[-1]['children'].append(node)
            else:
                data.append(node)
            
            stack.append(node)
    
    return data

def add_nodes_edges(graph, parent, children):
    for child in children:
        # Add link from parent to child
        graph.edge(parent, child['title'])
        # Recursively add the current child's children
        if child['children']:
            add_nodes_edges(graph, child['title'], child['children'])

def build_graph(data):
    graph = graphviz.Digraph(format='svg', engine='dot')
    graph.attr('node', shape='box', style='filled', color='lightblue', fontname='Helvetica')
    graph.attr('edge', color='gray')

    for node in data:
        graph.node(node['title'])
        if node['children']:
            add_nodes_edges(graph, node['title'], node['children'])
    
    return graph

def main():
    if len(sys.argv) != 3:
        print("Usage: python mindmap.py <markdown_file.md> <output_file.svg>")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown = f.read()
        
        mindmap_data = parse_markdown(markdown)
        graph = build_graph(mindmap_data)
        graph.render(output_file, cleanup=True)
        print(f"Mindmap saved to {output_file}.svg")
    
    except FileNotFoundError:
        print(f"Error: File {markdown_file} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
        main()
