import enum


class MemoryProfile(enum.Enum):
    fullgraph = 'fullgraph'

    countmin_512 = 'countmin_512'
    countmin_1024 = 'countmin_1024'
    countmin_2048 = 'countmin_2048'
    countmin_4096 = 'countmin_4096'
    countmin_8192 = 'countmin_8192'
    countmin_16384 = 'countmin_16384'
    countmin_32768 = 'countmin_32768'
    countmin_65536 = 'countmin_65536'

    gsketch_512 = 'gsketch_512'
    gsketch_1024 = 'gsketch_1024'
    gsketch_2048 = 'gsketch_2048'
    gsketch_4096 = 'gsketch_4096'
    gsketch_8192 = 'gsketch_8192'
    gsketch_16384 = 'gsketch_16384'
    gsketch_32768 = 'gsketch_32768'
    gsketch_65536 = 'gsketch_65536'

    tcm_512 = 'tcm_512'
    tcm_1024 = 'tcm_1024'
    tcm_2048 = 'tcm_2048'
    tcm_4096 = 'tcm_4096'
    tcm_8192 = 'tcm_8192'
    tcm_16384 = 'tcm_16384'
    tcm_32768 = 'tcm_32768'
    tcm_65536 = 'tcm_65536'

    alpha_512 = 'alpha_512'
    alpha_1024 = 'alpha_1024'
    alpha_2048 = 'alpha_2048'
    alpha_4096 = 'alpha_4096'
    alpha_8192 = 'alpha_8192'
    alpha_16384 = 'alpha_16384'
    alpha_32768 = 'alpha_32768'
    alpha_65536 = 'alpha_65536'
