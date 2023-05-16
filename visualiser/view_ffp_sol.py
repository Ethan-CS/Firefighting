#!/usr/bin/python3

import getopt
import math
import os
import queue
import subprocess
import sys
import tempfile
from collections import defaultdict

from igraph import *


# Fire spread and containment simulation process
def simulate(g, n, n_e, B_init, toSave, outputfile_name):
    UNTOUCHED = "#A9A9A9"
    BURNED = "#FF0000"
    SAVED = "#00FF00"
    # create a temporary directory for the images
    tmpdir = tempfile.TemporaryDirectory()
    # queue of vertices to be visited
    q = queue.Queue()

    g.es["width"] = 2
    g.vs["color"] = UNTOUCHED
    g.vs["size"] = 50
    g.vs["label_size"] = 20
    g.vs["label"] = [v.index for v in g.vs]
    # layout of graph
    # layout = g.layout_drl(fixed=[True for v in g.vs])
    layout = g.layout_lgl()
    # layout = g.layout_reingold_tilford()

    visual_style = {}
    visual_style["layout"] = layout
    visual_style["margin"] = [30, 30, 30, 30]
    visual_style["bbox"] = (1024, 900)
    visual_style["keep_aspect_ratio"] = True
    # fire outbreak
    for v in B_init:
        g.vs[v]["color"] = BURNED
        g.vs[v]["label"] = str(v) + "/" + str(0)
        g.vs[v]["label_color"] = "#FFFFFF"
        q.put(v)
    # time iteration marker
    q.put(-1)
    # iteration
    iter = 1
    plot(g, **visual_style, target=str(tmpdir.name) + '/out0.png')
    # plot(g, **visual_style, target='out0.png')

    # fire spreading and containment
    # similar to a BFS
    while not q.empty():
        v = q.get()
        # if it is a time iteration marker
        if v == -1:
            # marks a new iteration when the vertices currently in the queue
            # are all visited
            if not q.empty():
                q.put(-1)
            # plot(g, **visual_style, target=str(tmpdir.name) + '/out' + str(iter) + '.png')
            plot(g, **visual_style, target=str(tmpdir.name) +
                                           '/out' + str(iter) + '.png')
            iter = iter + 1
        else:
            # para cada vizinho de um vértice queimado na iteração anterior
            for e_u in g.incident(v):
                u = int(g.es[e_u].target)
                if u == v:
                    u = int(g.es[e_u].source)
                # se ele deve ser salvo e ainda não foi salvo
                if toSave[u] == True and g.vs[u]["color"] == UNTOUCHED:
                    g.vs[u]["color"] = SAVED
                    g.vs[u]["label"] = str(u) + "/" + str(iter)
                    g.vs[u]["label_color"] = "#FFFFFF"
                # se não deve ser salvo e está intocado
                elif toSave[u] == False and g.vs[u]["color"] == UNTOUCHED:
                    g.vs[u]["color"] = BURNED
                    # só visita vizinhos de vértice intocados
                    q.put(u)
                    g.vs[u]["label"] = str(u) + "/" + str(iter)
                    g.vs[u]["label_color"] = "#FFFFFF"

    # For some weird reason, the resolver can save vertices that are
    # away from the fire, so that even if the fire is contained, they
    # are beyond the vertex cut formed by the firefighter barrier
    for v in range(0, n):
        if toSave[v] == True and g.vs[v]["color"] != SAVED:
            g.vs[v]["color"] = SAVED
    # plot(g, **visual_style, target=str(tmpdir.name) +
    #      '/out' + str(iter) + '.png')

    # generate video
    devnull = open(os.devnull, 'w')
    subprocess.call(["ffmpeg", "-y", "-framerate", "1/3", "-start_number", "0", "-i", str(tmpdir.name) + "/out%d.png",
                     "-c:v", "libx264", "-r", "30", "-qscale", "1", "-pix_fmt", "yuv420p", "-threads", "0",
                     outputfile_name], stdout=devnull, stderr=devnull)


def simulate2(g, n, n_e, B_init, to_save, to_burn, max_t, outputfile_name):
    UNTOUCHED = "#A9A9A9"
    BURNED = "#FF0000"
    SAVED = "#00FF00"
    THREAT = "#00CED1"
    # create temporary directory for images
    tmpdir = tempfile.TemporaryDirectory()
    g.es["width"] = 2
    g.vs["color"] = UNTOUCHED
    g.vs["size"] = 50
    g.vs["label_size"] = 20
    # tag two vertices = ID
    g.vs["label"] = [v.index for v in g.vs]
    # layout of graph
    # layout = g.layout_drl(fixed=[True for v in g.vs])
    # layout = g.layout_lgl()
    layout = g.layout_fruchterman_reingold()
    # layout = g.layout_reingold_tilford()
    visual_style = {}
    visual_style["layout"] = layout
    visual_style["margin"] = [30, 30, 30, 30]
    visual_style["bbox"] = (1000, 1000)
    visual_style["keep_aspect_ratio"] = True
    # visual_style['hovermode'] = 'closest'

    for t in range(0, max_t + 1):
        for v in to_save[t]:
            g.vs[v]["color"] = SAVED
            g.vs[v]["label"] = str(v) + "/" + str(t)
            g.vs[v]["label_color"] = "#FFFFFF"
        for v in to_burn[t]:
            g.vs[v]["color"] = BURNED
            g.vs[v]["label"] = str(v) + "/" + str(t)
            g.vs[v]["label_color"] = "#FFFFFF"
            for e_u in g.incident(v):
                u = int(g.es[e_u].target)
                if u == v:
                    u = int(g.es[e_u].source)
                if g.vs[u]["color"] == UNTOUCHED:
                    g.vs[u]["color"] = THREAT
        plot(g, **visual_style, target=str(tmpdir.name) +
                                       '/out' + str(t) + '.png')

    # Generate the video
    devnull = open(os.devnull, 'w')
    subprocess.call(
        ["ffmpeg", "-y", "-framerate", "1/5", "-start_number", "0", "-i", str(tmpdir.name) + "/out%d.png", "-filter:v",
         "scale=1000:-1",
         "-c:v", "libx264", "-r", "30", "-qscale", "1", "-pix_fmt", "yuv420p", "-threads", "0", outputfile_name],
        stdout=devnull, stderr=devnull)


def main(argv):
    input_file_name = ''
    src = 0
    dst = 0
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile="])
    except getopt.GetoptError:
        print('view_instance.py -i <input_file_name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('view_instance.py -i <input_file_name>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file_name = arg
    g = Graph(directed=None)
    input_f = open(file=input_file_name, mode='r')
    # number of vertices
    n = int(input_f.readline())
    # number of edges
    n_e = int(input_f.readline())
    # number of vertices that are "focuses" of fire
    n_B_init = int(input_f.readline())
    # "focus" of fire
    B_init = map(int, input_f.readline().split())

    # create vertices from 0 to n-1
    g.add_vertices(n)

    # read the edges
    for e in range(0, n_e):
        src, dst = map(int, input_f.readline().split())
        g.add_edges([(src, dst)])

    max_t = -1
    n_to_save = int(input_f.readline())
    to_save = defaultdict(list)
    v = 0
    t = 0
    for e in range(0, n_to_save):
        v, t = map(int, input_f.readline().split())
        max_t = max(max_t, t)
        to_save[t].append(v)

    n_to_burn = int(input_f.readline())
    to_burn = defaultdict(list)
    v = 0
    t = 0
    for e in range(0, n_to_burn):
        v, t = map(int, input_f.readline().split())
        max_t = max(max_t, t)
        to_burn[t].append(v)

    input_f.close()
    # simulate(g, n, n_e, B_init, toSave, outputfile_name)
    simulate2(g, n, n_e, B_init, to_save, to_burn, max_t,
              os.path.splitext(input_file_name)[0] + ".mp4")


if __name__ == "__main__":
    main(sys.argv[1:])
