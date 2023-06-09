# firefighter-visualizer
A simple visualizer for solutions to instances of the firefighter problem on graphs (cloned from [this](https://github.com/nael8r/firefighter-visualizer.git) GitHub project).

# Usage

`./view_ffp_sol.py -i  <input_file>`

# Input file format

\<Number of vertices\>

\<Number of edges\>

\<Size of the set $B_{init}$\>

\<Elements of the $B_{init}$ set, space separated\>

\<Edges of the graph, onde per line, format: \<source\> \<destination\>\>

\<Number of vertices to be saved in the solution\>

\<Vertices to be saved in the solution, in form: \<vertex ID\> \<time\>\>

\<Number of vertices to be burned in the solution\>

\<Vertices to be burned in the solution, in form: \<vertex ID\> \<time\>\>

See the file **sol1.txt** for an example.

# Dependencies:

**igraph** package for python 3: http://igraph.org/python

**ffmpeg**: https://ffmpeg.org/download.html

# Example

Output example:

- **Green**: Defended
- **Gray**: Untouched
- **Blue**: Threatened
- **Red**: Burned
- **Node**: (ID/time of event)

![Exemplo de saída](https://raw.githubusercontent.com/nael8r/firefighter-visualizer/master/example.gif)
