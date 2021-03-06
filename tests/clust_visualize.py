# clustering

import json
import os

import matplotlib.pyplot as plt

from sketches import Sketches


def clust_visualize():
    print(os.path.basename(__file__).split('.')[0])

    sketches = (
        (Sketches.countmin.name, 'CountMin'),
        (Sketches.gsketch.name, 'gSketch'),
        (Sketches.tcm.name, 'TCM'),
        (Sketches.gmatrix.name, 'GMatrix'),
        (Sketches.alpha.name, 'Alpha'),
    )

    sketch_sizes = (
        (1024, '1 MB'),
        (2048, '2 MB'),
        (4096, '4 MB'),
        (8192, '8 MB'),
        (16384, '16 MB'),
        (32768, '32 MB'),
        (65536, '64 MB'),
        (131072, '128 MB'),
        (262144, '256 MB'),
        (524288, '512 MB'),
        (1048576, '1024 MB')
    )

    plt.rcParams['figure.dpi'] = 500
    # plt.rcParams["figure.figsize"] = (20, 15)

    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    ax.set_xscale("log")
    ax.minorticks_off()

    edge_count = 0
    test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])
    for sketch_name, pretty_name in sketches:
        memory_allocation = []
        clustering_coefficient = []

        for sketch_size, pretty_size in sketch_sizes:
            with open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size)) as file:
                output = json.load(file)
                memory_allocation.append(output['memory_allocation'])
                clustering_coefficient.append(output['clustering_coefficient'])
                edge_count = output['edge_count']

        plt.plot(memory_allocation, clustering_coefficient, label=pretty_name)

    # plot the fullgraph
    with open('{}/{}.json'.format(test_output_dir, Sketches.fullgraph.name)) as file:
        output = json.load(file)
        fullgraph_cc = output['clustering_coefficient']
        plt.plot([x[0] for x in sketch_sizes], [fullgraph_cc for x in sketch_sizes], label='FullGraph')


    plt.title('Memory vs Clustering Coefficient')
    plt.ylabel('Clustering Coefficient')
    plt.xlabel('Memory')
    plt.xticks(ticks=[x[0] for x in sketch_sizes], labels=[x[1] for x in sketch_sizes], rotation='vertical')
    plt.legend()

    fig.text(0.1, 0.045, '# edges : {:,}'.format(edge_count))

    test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
    os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
    plt.savefig('../reports/{}/{}.png'.format(os.path.basename(__file__).split('.')[0].split('_')[0], test_name))

    # plt.show()
    plt.close()
