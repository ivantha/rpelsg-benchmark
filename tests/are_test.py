# Average Relative Error
import sys, os
import gc
import json

# Path hack.
sys.path.insert(0, os.path.abspath('..'))

from common import utils, sampling
from sketches import Sketches
from sketches.alpha import Alpha
from sketches.countmin import CountMin
from sketches.full_graph import FullGraph
from sketches.gsketch import GSketch
from sketches.tcm import TCM

if __name__ == '__main__':
    base_edges = utils.get_edges_in_path('../datasets/unicorn_wget_small/benign_base/')  # base_path: Path to edges in the base graph
    streaming_edges = utils.get_edges_in_path('../datasets/unicorn_wget_small/benign_streaming/')  # streaming_path: Path to streaming edges

    base_edge_count = len(base_edges)
    streaming_edge_count = len(streaming_edges)

    memory_profiles = (
        (
            Sketches.countmin.name,
            (
                (512, CountMin(m=1024 * 32, d=8)),  # 512 KB
                (1024, CountMin(m=1024 * 32 * 2, d=8),),  # 1 MB
                (2048, CountMin(m=1024 * 32 * 4, d=8),),  # 2 MB
                (4096, CountMin(m=1024 * 32 * 8, d=8),),  # 4 MB
                (8192, CountMin(m=1024 * 32 * 16, d=8)),  # 8 MB
                (16384, CountMin(m=1024 * 32 * 32, d=8)),  # 16 MB
                (32768, CountMin(m=1024 * 32 * 64, d=8)),  # 32 MB
                (65536, CountMin(m=1024 * 32 * 128, d=8)),  # 64 MB
            )
        ),
        (
            Sketches.gsketch.name,
            (
                (512, GSketch(base_edges, streaming_edges,
                              total_sketch_width=1024 * 24, outlier_sketch_width=1024 * 8,
                              sketch_depth=8)),  # 512 KB
                (1024, GSketch(base_edges, streaming_edges,
                               total_sketch_width=1024 * 24 * 2, outlier_sketch_width=1024 * 8 * 2,
                               sketch_depth=8)),  # 1 MB
                (2048, GSketch(base_edges, streaming_edges,
                               total_sketch_width=1024 * 24 * 4, outlier_sketch_width=1024 * 8 * 4,
                               sketch_depth=8)),  # 2 MB
                (4096, GSketch(base_edges, streaming_edges,
                               total_sketch_width=1024 * 24 * 8, outlier_sketch_width=1024 * 8 * 8,
                               sketch_depth=8)),  # 4 MB
                (8192, GSketch(base_edges, streaming_edges,
                               total_sketch_width=1024 * 24 * 16, outlier_sketch_width=1024 * 8 * 16,
                               sketch_depth=8)),  # 8 MB
                (16384, GSketch(base_edges, streaming_edges,
                                total_sketch_width=1024 * 24 * 32, outlier_sketch_width=1024 * 8 * 32,
                                sketch_depth=8)),  # 16 MB
                (32768, GSketch(base_edges, streaming_edges,
                                total_sketch_width=1024 * 24 * 64, outlier_sketch_width=1024 * 8 * 64,
                                sketch_depth=8)),  # 32 MB
                (65536, GSketch(base_edges, streaming_edges,
                                total_sketch_width=1024 * 24 * 128, outlier_sketch_width=1024 * 8 * 128,
                                sketch_depth=8)),  # 64 MB
            )
        ),
        (
            Sketches.tcm.name,
            (
                (512, TCM(w=181, d=8)),  # 511.8 KB
                (1024, TCM(w=256, d=8)),  # 1 MB
                (2048, TCM(w=362, d=8)),  # 1.9996 MB
                (4096, TCM(w=512, d=8)),  # 4 MB
                (8192, TCM(w=724, d=8)),  # 7.9983 MB
                (16384, TCM(w=1024, d=8)),  # 16 MB
                (32768, TCM(w=1448, d=8)),  # 31.9932 MB
                (65536, TCM(w=2048, d=8)),  # 64 MB
            )
        ),
        (
            Sketches.alpha.name,
            (
                (512, Alpha(base_edges, streaming_edges,
                            total_sketch_width=157,  # 385.1 KB
                            outlier_sketch_width=91,  # 129.4 KB
                            sketch_depth=8)),  # 512 KB
                (1024, Alpha(base_edges, streaming_edges,
                             total_sketch_width=222,  # 770 KB
                             outlier_sketch_width=128,  # 256 KB
                             sketch_depth=8)),  # 1 MB
                (2048, Alpha(base_edges, streaming_edges,
                             total_sketch_width=314,  # 1.5045 MB
                             outlier_sketch_width=181,  # 0.4999 MB
                             sketch_depth=8)),  # 2 MB
                (4096, Alpha(base_edges, streaming_edges,
                             total_sketch_width=443,  # 2.9945 MB
                             outlier_sketch_width=256,  # 1 MB
                             sketch_depth=8)),  # 4 MB
                (8192, Alpha(base_edges, streaming_edges,
                             total_sketch_width=627,  # 5.9987 MB
                             outlier_sketch_width=362,  # 1.9996 MB
                             sketch_depth=8)),  # 8 MB
                (16384, Alpha(base_edges, streaming_edges,
                              total_sketch_width=887,  # 12.0051 MB
                              outlier_sketch_width=512,  # 4 MB
                              sketch_depth=8)),  # 16 MB
                (32768, Alpha(base_edges, streaming_edges,
                              total_sketch_width=1254,  # 23.9947 MB
                              outlier_sketch_width=724,  # 7.9983 MB
                              sketch_depth=8)),  # 32 MB
                (65536, Alpha(base_edges, streaming_edges,
                              total_sketch_width=1774,  # 48.0206 MB
                              outlier_sketch_width=1024,  # 16 MB
                              sketch_depth=8)),  # 64 MB
            )
        ),
    )

    # construct a FullGraph
    full_graph = FullGraph()
    full_graph.initialize()

    full_graph.stream(base_edges)  # FullGraph - construct base graph
    full_graph.stream(streaming_edges)  # FullGraph - streaming edges

    print('Completed: full_graph')

    # reservoir sampling for 1000 items as (i, j) => 1000 queries
    sample_size = 1000
    sample_stream = sampling.select_k_items(base_edges, sample_size)

    for sketch_name, profiles in memory_profiles:  # sketches are recreated with increasing memories
        output = {
            'sketch_name': sketch_name,
            'base_edge_count': base_edge_count,
            'streaming_edge_count': streaming_edge_count,
            'results': []
        }

        for memory_allocation, sketch in profiles:
            sketch.initialize()  # initialize the sketch
            sketch.stream(base_edges)  # construct base graph
            sketch.stream(streaming_edges)  # streaming edges

            # query
            relative_error_sum = 0
            for source_id, target_id in sample_stream:
                true_frequency = full_graph.get_edge_frequency(source_id, target_id)
                estimated_frequency = sketch.get_edge_frequency(source_id, target_id)
                relative_error = (estimated_frequency - true_frequency) / true_frequency * 1.0
                relative_error_sum += relative_error

            result = {
                'memory_allocation': memory_allocation,
                'average_relative_error': relative_error_sum / sample_size
            }

            output['results'].append(result)

            print('Completed: {}_{}'.format(sketch_name, memory_allocation))

            # free memory - remove reference to the sketch
            del sketch

        # free memory - call garbage collector
        gc.collect()

        os.makedirs(os.path.dirname('../output/are/{}.json'.format(sketch_name)), exist_ok=True)
        with open('../output/are/{}.json'.format(sketch_name), 'w') as file:
            json.dump(output, file, indent=4)
