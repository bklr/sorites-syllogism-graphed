# Visualizing Polysyllogisms using Directed Graphs

This project converts a set of logical implication rules to visualize the structures of a *polysyllogisms* (such as a Lewis Carroll sorites) as directed graphs, and computes logical consequences from the implication network.
The project paper is located within ```visualizing_polysyllogisms.pdf```


The tool enables:
- Parsing rules of the form `A -> B` and `A1 & A2 -> B`
- Constructing a directed implication graph using NetworkX
- Visualizing the graph interactively in a browser using PyVis
- Querying all consequences of any predicate
- Computing the *longest implication chain* (the sorites conclusion)

## Project Structure 
```
root/  
|- Implication_Examples/    
|- |- Soriteses_P60_E9.txt # Sorites Problem 60 of Example 9 in Book VII of Lewis Carroll's Symbolic Logic  
|- |- Soriteses_P52_E9.txt # Sorites Problem 52 of Example 9 in Book VII of Lewis Carroll's Symbolic Logic  
|- |- BC_CS_Courses_Simpl.txt # List of Boston College's Computer Science Courses with some ommissions  
|- |- Network_Permissions.txt # Mock Example Network Permissions Chain with Soriteses Structure    
|- |- other_examples and add your files here.txt  
|    
|- implgraph.py # Main Program
|- visualizing_polysyllogisms.pdf # Project Paper
```
 
## Input Format
The program reads implications from a plain .txt file following rules:
- Left side may contain one or multiple predicates joined by '&'
- Blank lines or commented ones beginning with '#' are ignored.
- Note: Contrapositives must be manually added
Example files are within the Implication_Examples folder.

## Running the Program
1. Install dependencies:
```pip install networkx pyvis```
2. Place your implication file inside `Implication_Examples/`
3. Edit the variable near the top of the script:
```RULES_FILE = "Soriteses_P60_E9.txt"```
4. Run:
```python implgraph.py```

## Output
- Running the script generates `graph.html` when opened in browser gives an interactive PyVis graph.
- The program automatically finds the longest shortest-path between any two nodes to find the Sorites Conclusion (furthest logical consequence in the system).
- The terminal prompts a starting node for reachability analysis and outputs all predicates logically implied by it and the shortest implication chain to each one.
