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
        mig_space = [0.01, 0.03, 0.05]
        locus_space = [0.2, 0.35, 0.5]
        k_space = [300, 600, 900]
        n_rep = 10

        print('Num runs: %d' % (len(mig_space)*len(locus_space)*len(k_space)*n_rep))

        for mig_rate in mig_space:
            for locus_weight in locus_space:
                for k_mean in k_space:
                    path = 'K%d_LW%.2f_MR%.2f_rep' % (k_mean, locus_weight, mig_rate)

                    for rep in range(n_rep):
                        params = {}
                        for param in param_table:
                            params[param] = param_table[param]['default']


                        params["MIGRATION_RATE"] = mig_rate
                        params["MEAN_LOCUS_WEIGHT"] = locus_weight
                        params["PATCH_K_MEAN"] = k_mean

                        params["DATA_DIRECTORY"] = path + str(rep)
                        params["RANDOM_SEED"] = np.random.randint(0, 100000000)
                        params["EF_RANDOM_SEED"] = np.random.randint(0, 100000000)
                        params["PATCH_RANDOM_SEED"] = np.random.randint(0, 100000000)
                        params["GENOME_RANDOM_SEED"] = np.random.randint(0, 100000000)

                        print_run(params, i, rep)
                        run = start_run(params)
                        i += 1
        '''
        #param_list = read_batch_file(args['BATCH'][0])

        #for i,params in enumerate(param_list):
            #num_rep = int(params['NUM_REPLICATES'])

            for rep in range(num_rep):
                this_rep_params = copy.deepcopy(params)
                this_rep_params["DATA_DIRECTORY"] = params["DATA_DIRECTORY"] + str(rep)
                this_rep_params["RANDOM_SEED"] = np.random.randint(0, 100000000)
                this_rep_params["EF_RANDOM_SEED"] = np.random.randint(0, 100000000)
                this_rep_params["PATCH_RANDOM_SEED"] = np.random.randint(0, 100000000)
                this_rep_params["GENOME_RANDOM_SEED"] = np.random.randint(0, 100000000)

                os.chdir(this_dir)
                create_batch_run_file(this_dir, this_rep_params)

                #print_run(this_rep_params, i, rep)
                #p = multiprocessing.Process(target=start_run, args=(this_rep_params,))
                #p.start()
        '''
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
