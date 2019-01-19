
#ifndef GENOME_DICT_H
#define GENOME_DICT_H

#include "include.h"

class GenomeDict{
    public:
        GenomeDict();
        int* generate_perm_with_uniq_ints(int size, int n);

        std::vector<int> chromo_map;
        std::vector<std::vector<int>> fitness_loci;
        double* selection_strengths;
        std::vector<int> neutral_loci;
};

#endif
