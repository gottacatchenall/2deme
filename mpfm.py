#! /usr/bin/env python3

from src.start_run import start_run, print_info, print_run, create_batch_run_file
from src.parse_args import setup_arg_parser, read_param_table, read_batch_file
import os, copy, multiprocessing
import numpy as np

def main():
    this_dir = os.path.abspath('.')

    param_table = read_param_table()
    parser = setup_arg_parser(param_table)
    args = vars(parser.parse_args())
    print_info()
    i = 0
    if (args['BATCH']):
        mig_space = [0.001, 0.0005]
        locus_space = [0.1, 0.2, 0.3]
        k_space = [1000,2000,3000]
        n_rep = 30

        print('Num runs: %d' % (len(mig_space)*len(locus_space)*len(k_space)*n_rep))

        treatment_ct = 0
        for mig_rate in mig_space:
            for locus_weight in locus_space:
                for k_mean in k_space:
                        path = 'prod3_K%d_LW%.2f_MR%.3f_rep' % (k_mean, locus_weight, mig_rate)
                        treatment_ct += 1
                        for rep in range(n_rep):
                            params = {}
                            for param in param_table:
                                params[param] = param_table[param]['default']


                            params["MIGRATION_RATE"] = mig_rate
                            params["MEAN_LOCUS_WEIGHT"] = locus_weight
                            params["PATCH_K_MEAN"] = k_mean

                            params["NUM_GENERATIONS"] = 2000
                            params["CENSUS_FREQ"] = 50
                            params["NUM_OF_LOCI"] = 100
                            params["NUM_LOCI_PER_EF"] = 50
                            params["DATA_DIRECTORY"] = path + str(rep)
                            params["RANDOM_SEED"] = np.random.randint(0, 100000000)
                            params["EF_RANDOM_SEED"] = np.random.randint(0, 100000000)
                            params["PATCH_RANDOM_SEED"] = np.random.randint(0, 100000000)
                            params["GENOME_RANDOM_SEED"] = np.random.randint(0, 100000000)

                            create_batch_run_file(this_dir, params, treatment_ct)

    else:
        params = {}
        for param in param_table:
            if args[param]:
                params[param] = args[param][0]
            else:
                params[param] = param_table[param]['default']
        run = start_run(params)


if __name__ == '__main__':
    main()
