#! /usr/bin/env python

from webweb import Web
import csv, sys, os, pandas
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities, modularity
import numpy as np

def net_vis(ld_file, loci_file):
    web = Web(title='webweb')

    loci_path = os.path.abspath(loci_file)
    loci = pandas.read_csv(loci_path)
    def get_ef(l):
        q = 'locus ==' + str(l)
        r = loci.query(q)
        return r.iloc[0]['ef']
    def get_chr(l):
        q = 'locus ==' + str(l)
        r = loci.query(q)
        return r.iloc[0]['chromo']

    path = os.path.abspath(ld_file)
    df = pandas.read_csv(path)

    gens = df['generation'].unique()

    thres = 0.005

    max_locus = df['locus2'].max()
    metadata = {
        'ef': {
            'values': [get_ef(x) for x in range(max_locus)]
        },
        'chromo': {
            'values': [get_chr(x) for x in range(max_locus)]
        },
    }

    for gen in gens:
        q = 'generation == ' + str(gen)
        this_gen = df.query(q)
        max = this_gen['D'].max()

        edge_list = []

        for row in this_gen.itertuples():
            L1 = row[2]
            L2 = row[3]
            D = row[4]
            Gen = row[1]

            if D > thres:
                edge = [L1, L2, 0.1]
                edge_list.append(edge)
            else:
                edge = [L1, L2, 0]
                edge_list.append(edge)


        web.networks.webweb.add_layer(adjacency=edge_list, metadata=metadata)
    #web.display.scaleLinkWidth = True
    web.show()

def write_data(thr, gen, mean_deg, clus, mod, file_name):
    write_line = '%f,%f,%f,%f,%f\n' % (thr, gen, mean_deg, clus, mod)
    with open(file_name, 'a') as f:
        f.write(write_line)



def mod_over_time(ld_file, data_file):
    path = os.path.abspath(ld_file)
    df = pandas.read_csv(path)
    gens = df['generation'].unique()
    max_locus = int(df['locus2'].max())

    thres_space = np.linspace(0.01, 1.0, 100)
    print thres_space
    for thr in thres_space:
        for gen in gens:
            q = 'generation == ' + str(gen)
            this_gen = df.query(q)

            G = nx.Graph()
            for i in range(max_locus):
                G.add_node(i)

            edge_list = []
            for row in this_gen.itertuples():
                L1 = int(row[2])
                L2 = int(row[3])
                D = row[4]
                Gen = row[1]

                if D > thr:
                    edge = [L1, L2]
                    edge_list.append(edge)

            G.add_edges_from(edge_list)

            # clus coef
            # modularity
            # avg deg
            clus = nx.average_clustering(G)

            degrees = G.degree
            s = 0
            ct = 0

            for node, deg in degrees:
                s += deg
                ct += 1

            mean_deg = float(s)/float(ct)

            try:
                com = greedy_modularity_communities(G)
                mod = modularity(G, com)
            except:
                mod = 0

            write_data(thr, gen, mean_deg, clus, mod, data_file)


def main(ld_file, loci_file):
    #net_vis(ld_file, loci_file)
    file_name = './output.csv'
    path = os.path.abspath(file_name)
    print path
    write_line = 'threshold,generation,mean_degree,clustering,modularity\n'
    with open(file_name, 'a') as f:
        f.write(write_line)

    mod_over_time(ld_file, path)


if __name__ == '__main__':
    file = sys.argv[1]
    loci_file = sys.argv[2]
    main(file, loci_file)
