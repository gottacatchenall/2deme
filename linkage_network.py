#! /usr/bin/env python

from webweb import Web
import csv, sys, os, pandas



def main(ld_file, loci_file):
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

    thres = 0.05

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

#edge_list = [[1, 2], [2, 3], [3, 4]]

# instantiate webweb and show the result
#Web(edge_list).show()


if __name__ == '__main__':
    file = sys.argv[1]
    loci_file = sys.argv[2]
    main(file, loci_file)
