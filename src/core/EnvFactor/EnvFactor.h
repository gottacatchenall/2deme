
#ifndef ENV_FACTOR_H
#define ENV_FACTOR_H

#include "include.h"

class EnvFactor{
    private:
        double* map;
    public:
        EnvFactor(double diff);
        double get_env_factor_value(int patch_id);
};

#endif
