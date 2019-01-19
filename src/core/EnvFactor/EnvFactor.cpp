#include "EnvFactor.h"

EnvFactor::EnvFactor(double diff){
    int size = params["NUM_PATCHES"];
    this->map = new double[size];
    map[0] = 0.5 + float(diff*0.5);
    map[1] = 0.5 - float(diff*0.5);
}

double EnvFactor::get_env_factor_value(int patch_id){
    return this->map[patch_id];
}
