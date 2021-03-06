# Edge weight distribution

import json
import os

import matplotlib
import matplotlib.pyplot as plt

from sketches import Sketches


def ewd_visualize():
    print(os.path.basename(__file__).split('.')[0])

    sketches = (
        (Sketches.fullgraph.name, 'FullGraph'),
        (Sketches.countmin.name, 'CountMin'),
        (Sketches.gsketch.name, 'gSketch'),
        (Sketches.tcm.name, 'TCM'),
        (Sketches.gmatrix.name, 'GMatrix'),
        (Sketches.alpha.name, 'Alpha'),
    )

    sketch_sizes = (
        # (100, '100 KB'),
        # (200, '200 KB'),
        # (300, '300 KB'),
        # (400, '400 KB'),
        # (512, '512 KB'),
        (1024, '1 MB'),
        # (2048, '2 MB'),
        # (4096, '4 MB'),
        # (8192, '8 MB'),
        # (16384, '16 MB'),
        # (32768, '32 MB'),
        # (65536, '64 MB')
    )

    matplotlib.rcParams['figure.dpi'] = 500

    test_output_dir = '../output/{}_test'.format(os.path.basename(__file__).split('.')[0].split('_')[0])

    for sketch_name, pretty_name in sketches:
        for sketch_size, pretty_size in sketch_sizes:
            if sketch_name == Sketches.fullgraph.name:
                if sketch_size == 1024:
                    file = open('{}/{}.json'.format(test_output_dir, Sketches.fullgraph.name))
                    sketch_size = ''
                else:
                    break
            else:
                file = open('{}/{}_{}.json'.format(test_output_dir, sketch_name, sketch_size))

            output = json.load(file)
            edge_weight_distribution = output['edge_weight_distribution']

            fig = plt.figure()
            ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
            ax.set_xscale("log")

            X = [int(float(i)) for i in edge_weight_distribution.keys()]
            Y = [i / 1000000 for i in edge_weight_distribution.values()]
            plt.scatter(X, Y, marker='.', s=10)

            plt.title('Edge weight distribution of {}'.format(pretty_name))
            plt.ylabel('Distribution (10^6)')
            plt.xlabel('Edge weight')

            fig.text(0.5, 0.03, '# edges : {:,}'.format(output['number_of_edges']))
            fig.text(0.1, 0.03, '# vertices : {:,}'.format(output['number_of_vertices']))

            test_name = os.path.basename(__file__).split('.')[0].split('_')[0]
            os.makedirs('../reports/{}'.format(test_name), exist_ok=True)
            plt.savefig('../reports/{}/{}_{}.png'.format(test_name, sketch_name, sketch_size))

            # plt.show()
            plt.close()

            print('Completed visualization: {}_{}'.format(sketch_name, sketch_size))
