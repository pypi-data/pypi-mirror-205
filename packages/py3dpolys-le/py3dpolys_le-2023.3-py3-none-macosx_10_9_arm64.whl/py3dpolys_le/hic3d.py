#! /usr/bin/env python

import argparse
import logging
import os
import sys
from itertools import permutations, combinations

import cooler
import h5py
import numba
import numpy as np
import pandas as pd
import seaborn as sns
# from PIL import Image
from matplotlib import pyplot as plt
# from matplotlib.colors import LinearSegmentedColormap
# from mpl_toolkits.mplot3d import Axes3D
from scipy import sparse
from scipy.stats import chisquare, pearsonr

import __init__

# import pyBigWig
# from scipy import stats
# import umap
# import umap.plot
# from sklearn.manifold import TSNE

# from numpy.core._multiarray_umath import ndarray

# Constants
PLOT_UMAP = 'umap'
PLOT_TSNE = 'tsne'
PLOT_3D = '3d'
AXES = [0, 1, 2]
AXIS_MANES = ['x', 'y', 'z']

CHR_SIZES_FILE_DEFAULT = "./chromosome_sizes.tsv"
RESOLUTION = 5000
COOLER_RESOLUTION_FACTORS = [1, 2, 5, 10, 20, 50]

HDF5_DATASET = "hic3d_cool"
HDF5_BINS = "bins"

CHROMS = np.array(['chrI', 'chrII', 'chrIII', 'chrIV', 'chrV', 'chrX'])
CHROMOSOME_DEFAULT = 'chrX'

HIC3D_CONTACT_CATEGORIES = ['AAA', 'AAB', 'ABB', 'BsBsBs', 'BlBrB', 'AA0', 'AB0', 'BB0', 'A00', 'B00', '000']
CMAP_3WAY_AB = 'tab20b'

# Initialization
logger = logging.getLogger(__init__.__name__)


# https://matplotlib.org/3.1.3/tutorials/colors/colormaps.html

def get_parser():
    p = argparse.ArgumentParser()
    p.add_argument("command", help="Command name.",
                   choices=['plot', 'ins_score', 'merge'])
    p.add_argument("-i", "--input_file",
                   help="Input Hi-C3D cool HDF5 file.")
    p.add_argument("-j", "--input_file2", default=None,
                   help="Input Hi-C3D cool HDF5 file 2.")
    p.add_argument("-r", "--resolution", default=10000, type=int,
                   help="Resolution of the Hi-C3D cool HDF5 file.")
    p.add_argument("-chr", "--chromosome", default=CHROMOSOME_DEFAULT,
                   help="Chromosome to be used for hic3d export and A/B compartments.")
    p.add_argument("-cs", "--chromosome_sizes", default="./chromosome_sizes.tsv",
                   help="Input Hi-C3D cool HDF5 file.")
    p.add_argument("-o", "--output", default=".", help="Output folder or file where to save plots, "
                                                       "merged hic3ds, ins_score.")
    p.add_argument("-p", "--plot_method", choices=[PLOT_UMAP, PLOT_TSNE, PLOT_3D], default=PLOT_3D,
                   help="Plot method.")
    #    p.add_argument("-a", "--axis", choices=[0, 1, 2], type=int, default=0, help="Axis to slice.")
    p.add_argument("-pr", "--points_range", nargs='+', default=[0, 391170], type=int,
                   help="Range of points to be plotted: [start, end].")
    p.add_argument("-nn", "--n_neighbors", default=20, help="UMAP parameter n_neighbors. Default: 20.", type=int)
    p.add_argument("-md", "--min_dist", default=0.01, help="UMAP parameter min_dist. Default: 0.01.", type=float)
    p.add_argument("-c", "--cmap", default="Greys",
                   help="Color map used for the 3D visualization method: "
                        "cool, hot_r, gist_heat_r, afmhot_r, YlOrRd, Greys, gist_yarg. Default: hot_r.")
    p.add_argument("-m", "--metric", default="canberra", help="UMAP metric: euclidean, manhattan, minkowski, canberra. "
                                                              "Default: canberra.")
    # https://umap-learn.readthedocs.io/en/latest/parameters.html#metric
    p.add_argument("-f", "--file_format", default="tif", help="File format extension: png, tif, svg. Default: png.")

    return p


@numba.njit
def hic3d_idx(x, y, z, N):
    sum_xNN = (x - 1) * (N - 1) * N - N * (x - 1) * x / 2 - (x - 1) * (N - 1) * N / 2 + x * (x - 1) * (x + 1) / 6
    sum_yN = (y - x - 1) * N - ((y - 1) * y - (x + 1) * x) / 2
    sum_z = (z - y)
    return int(sum_xNN + sum_yN + sum_z)


# @numba.njit
def init_hic3d_cool(N):
    hic3d_len = hic3d_idx(N - 2, N - 1, N, N)
    # logger.info(f'init_hic3d_cool for N:{N} hic3d_len:{hic3d_len} ...')
    hic3d_cool = np.full((hic3d_len, 4), 0)  # np.zeros([hic3d_len, 4], dtype=np.int32)
    # idx = 0
    # for x in range(1, N-1):
    #     for y in range(x+1, N):
    #         for z in range(y+1, N+1):
    #             hic3d_cool[idx, 0] = x-1
    #             hic3d_cool[idx, 1] = y-1
    #             hic3d_cool[idx, 2] = z-1
    #             hic3d_cool[idx, 3] = 0
    #             idx = idx + 1
    return hic3d_cool


def hic3d_ins_score(hic3d_file: str, resolution: int, chrom: str, chromosome_sizes: str,
                    hic3d_file2: str = None):
    bed_graph_file = f'{os.path.splitext(hic3d_file)[0]}_ins_score.bedGraph'

    # chr_sizes_pd = pd.read_table(chromosome_sizes, names=['chr', 'size'])
    # chr_sizes = list(chr_sizes_pd['size'])

    with h5py.File(hic3d_file, 'r') as f:
        logger.info(f"plotting HiC: {hic3d_file} , Keys: {f.keys()}")
        # a_group_key = list(f.keys())[0]

        # Get the data
        bins = list(f[HDF5_BINS])
        data = list(f[HDF5_DATASET])

        bins_cool = np.array(bins)
        hic3_cool = np.array(data)

        if hic3d_file2:
            with h5py.File(hic3d_file2, 'r') as f2:
                data2 = list(f2[HDF5_DATASET])
                hic3_cool2 = np.array(data2)
        else:
            hic3_cool2 = None
        logger.info(f"hic3_cool.shape: ${hic3_cool.shape} ...")

        hic3_N = max(max(hic3_cool[:, 0]), max(hic3_cool[:, 1]), max(hic3_cool[:, 2]))  # ?== n_bin
        n_bin = len(bins)   #hic3_N
        win = 10  # 5000kb = 5Mb
        ins_score_vals = np.zeros(win)  # add start zeros: not calculated
        for s in range(win, n_bin - win):
            full_cube = hic3_cool[(hic3_cool[:, 0] >= s-win) & (hic3_cool[:, 0] <= s+win)
                                  & (hic3_cool[:, 1] >= s-win) & (hic3_cool[:, 1] <= s+win)
                                  & (hic3_cool[:, 2] >= s-win) & (hic3_cool[:, 2] <= s+win)]
            full_cube_sum = np.sum(full_cube[:, 3])
            if hic3_cool2:
                full_cube2 = hic3_cool2[(hic3_cool2[:, 0] >= s-win) & (hic3_cool2[:, 0] <= s+win)
                                        & (hic3_cool2[:, 1] >= s-win) & (hic3_cool2[:, 1] <= s+win)
                                        & (hic3_cool2[:, 2] >= s-win) & (hic3_cool2[:, 2] <= s+win)]
                full_cube_sum += np.sum(full_cube2[:, 3])

            lower_cube = full_cube[(full_cube[:, 0] < s) & (full_cube[:, 1] < s) & (full_cube[:, 2] < s)]
            lower_cube_sum = np.sum(lower_cube[:, 3])
            if hic3_cool2:
                lower_cube2 = full_cube2[(full_cube2[:, 0] < s) & (full_cube2[:, 1] < s) & (full_cube2[:, 2] < s)]
                lower_cube_sum += np.sum(lower_cube2[:, 3])

            upper_cube = full_cube[(full_cube[:, 0] > s) & (full_cube[:, 1] > s) & (full_cube[:, 2] > s)]
            upper_cube_sum = np.sum(upper_cube[:, 3])
            if hic3_cool2:
                upper_cube2 = full_cube2[(full_cube2[:, 0] > s) & (full_cube2[:, 1] > s) & (full_cube2[:, 2] > s)]
                upper_cube_sum += np.sum(upper_cube2[:, 3])

            cube_center = np.sum(full_cube[(full_cube[:, 0] == s) & (full_cube[:, 1] == s) & (full_cube[:, 2] == s), 3])  # sum to avoid problems with empty list
            if hic3_cool2:
                cube_center += np.sum(full_cube2[(full_cube2[:, 0] == s) & (full_cube2[:, 1] == s) & (full_cube2[:, 2] == s), 3])  # sum to avoid problems with empty list
            s_val = (full_cube_sum - lower_cube_sum - upper_cube_sum - cube_center) / (win ** 3)
            ins_score_vals = np.append(ins_score_vals, s_val)
        ins_score_vals = np.append(ins_score_vals, np.zeros(win))  # add end zeros: not calculated

        # n_bin = hic3_N  # hic3_cool.shape[1] if hic3_cool.ndim > 1 else len(hic3_cool)
        ins_score_df = pd.DataFrame(columns=['chrom', 'start', 'end', 'value'], index=None)
        ins_score_df['start'] = np.arange(0, n_bin*resolution, resolution)
        ins_score_df['end'] = np.arange(resolution, (n_bin+1)*resolution, resolution)
        ins_score_df['value'] = ins_score_vals
        ins_score_df['chrom'] = chrom
        ins_score_df.to_csv(bed_graph_file, sep='\t', header=False, index=False)


def assure_folder(folder_name):
    if not os.path.exists(folder_name):  # or not os.path.isdir(folder_name):
        try:
            os.makedirs(folder_name)
        except:
            logging.debug(f'Folder {folder_name} was created by other thread.')


class PlotParams:
    # UMAP params
    n_neighbors: int
    min_dist: float
    points_range: list
    # 3D params
    cmap: str

    def __init__(self, n_neighbors=None, min_dist=None, metric=None, points_range=[0], cmap='hot_r') -> None:
        super().__init__()
        self.n_neighbors = n_neighbors
        self.min_dist = min_dist
        self.metric = metric
        self.points_range = points_range
        self.cmap = cmap


def merge_hic3d(hic3d_file, hic3d_file2, output_file):
    with h5py.File(hic3d_file, 'r') as f, h5py.File(hic3d_file2, 'r') as f2, h5py.File(output_file, 'w') as fout:
        logger.info(f"Merging HiC3D {hic3d_file} and {hic3d_file2} ...")

        # Get the data
        bins = np.array(list(f[HDF5_BINS]))
        hic3_cool = np.array(list(f[HDF5_DATASET]))

        bins2 = np.array(list(f[HDF5_BINS]))
        hic3_cool2 = np.array(list(f2[HDF5_DATASET]))

        if not len(bins) == len(bins2):
            logger.info(f"plotting HiC: {hic3d_file} , Keys: {f.keys()}")
        # concat & sort
        hic3d_cool = np.vstack([hic3_cool, hic3_cool2])
        sorted_ind = np.lexsort((hic3d_cool[:, 2], hic3d_cool[:, 1], hic3d_cool[:, 0]))
        hic3d_cool = hic3d_cool[sorted_ind]

        sxy = [-1, -1, -1]
        si = 0
        logger.info(f"start merging...")
        for i, pix in enumerate(hic3d_cool):
            if np.array_equal(sxy, pix[0:3]):  # still same coordinates: accumulate
                hic3d_cool[si, 3] += pix[3]    # == hic3d_cool[i, 3]
                hic3d_cool[i, 3] = 0           # same: pix[3] = 0
            else:  # new coordinates
                si = i
                sxy = pix[0:3]
        zero_idx = np.where(hic3d_cool[:, 3] == 0)
        hic3d_cool = np.delete(hic3d_cool, zero_idx, 0)

        fout.create_dataset(HDF5_BINS, data=bins)
        fout.create_dataset(HDF5_DATASET, data=hic3d_cool)
    #  save_cooler(zplot_hic, bins, file_prefix=output_file, balanced=True)


def plot(hic3d_file, output_folder='.', chromosome_sizes=CHR_SIZES_FILE_DEFAULT,
         plot_method=PLOT_3D, plot_params: PlotParams = PlotParams(), format='png'):
    logger.info(f'Plotting {plot_method.upper()} HiC3D for {hic3d_file} in file format: {format} ...')
    assure_folder(output_folder)

    # chr_sizes_pd = pd.read_table(chromosome_sizes, names=['chr', 'size'])
    # chr_sizes = list(chr_sizes_pd['size'])

    with h5py.File(hic3d_file, 'r') as f:
        logger.info(f"plotting HiC: {hic3d_file} , Keys: {f.keys()}")
        # a_group_key = list(f.keys())[0]

        # Get the data
        data = list(f[HDF5_DATASET])
        # bins = list(f[HDF5_BINS])

        # bins_cool = np.array(bins)
        hic3_cool = np.array(data)
        logger.info(f"hic3_cool.shape: ${hic3_cool.shape} ...")
        start_point = plot_params.points_range[0]
        if len(plot_params.points_range) > 1:
            end_point = plot_params.points_range[1]
        else:
            end_point = ''
        hic3_N = max(hic3_cool[2, :])  # , max(hic3_cool[1, :]), max(hic3_cool[0, :]))  # len(bins_cool)  #

        basename = os.path.basename(hic3d_file)
        file_pref = f'{basename}_{plot_method}-pr{start_point}-{end_point if end_point else ""}'

        hic3_cool_3log = np.log10(hic3_cool[:, 3])

        title = f'Hi-C3D {plot_method} view for {basename}'
        # f'points range:{start_point}-{end_point if end_point else ""}'

        logger.info(f'{title} ...')

        # Check how R did it: sneaked matrix zhic_merged_mat exported with R
        # zhic_file_pref = "./hic3d_366/HiC3D_366_50kb_chrX_zhic"
        # logger.info(f'Conver {zhic_file_pref}.tsv to cool ...')
        # zplot_hic = np.genfromtxt(open(zhic_file_pref+".tsv"), delimiter="\t", dtype=int)
        # save_cooler(zplot_hic, bins, file_prefix=zhic_file_pref, balanced=True)
        # exit(1)  # done and out

        if False:  # plot_method.upper() == PLOT_UMAP.upper() or plot_method.upper() == PLOT_TSNE.upper():
            # enabled it later when everything else looks good
            hic3_cool[:, 3] = hic3_cool_3log

            if end_point:
                data_points = hic3_cool[:, start_point:end_point].transpose()
                data_points = data_points.astype(float)
                # data_points[:, 3] = hic3_cool_3log[start_point:end_point]
            else:
                data_points = hic3_cool[:, start_point:].transpose()
                data_points = data_points.astype(float)
                # data_points[:, 3] = hic3_cool_3log[start_point:]

            if plot_method.upper() == PLOT_UMAP.upper():
                logger.info(f'UMAP(n_neighbors={plot_params.n_neighbors}, min_dist={plot_params.min_dist})'
                            f' fit[{start_point}:{end_point}] hic3_cool ...')

                umap_conf = umap.UMAP(n_neighbors=plot_params.n_neighbors, min_dist=plot_params.min_dist,
                                      metric=plot_params.metric)
                hic3d_mapper = umap_conf.fit(data_points)
                logger.info(f'UMAP points hic3_cool ...')
                umap.plot.points(hic3d_mapper)
                # hic3d_2d = umap_conf.fit_transform(data_points)
                # plt.scatter(hic3d_2d[:, 0], hic3d_2d[:, 1], c=data_points[:, 3])
                plt.title(title)
                metric = f'_{plot_params.metric}'
                ##umap.plot.show(p)
            elif plot_method.upper() == PLOT_TSNE.upper():
                # tSNE
                tsne = TSNE(n_components=2, random_state=0)
                hic3d_2d = tsne.fit_transform(data_points)
                plt.figure()  # figsize=(6, 5))
                plt.scatter(hic3d_2d[:, 0], hic3d_2d[:, 1], c=data_points[:, 3])
                plt.title(title)
                metric = ''

            file_name = os.path.join(output_folder, f'{file_pref}'
                                                    f'-nn{plot_params.n_neighbors}-md{plot_params.min_dist}'
                                                    f'_fit{metric}.{format}')

            logger.info(f'Plot savefig to {file_name} ...')
            plt.savefig(file_name, dpi=200)
        else:  # plot_method == PLOT_3D
            # c_palette = plt.get_cmap(plot_params.cmap)
            hic3_cool[:, 3] = hic3_cool_3log
            # the sub-CUBE plot
            # if end_point:
            #     x = hic3_cool[start_point:end_point, 0]
            #     y = hic3_cool[start_point:end_point, 1]
            #     z = hic3_cool[start_point:end_point, 2]
            #     c = hic3_cool_3log[start_point:end_point]
            # else:
            #     x = hic3_cool[start_point:, 0]
            #     y = hic3_cool[start_point:, 1]
            #     z = hic3_cool[start_point:, 2]
            #     c = hic3_cool_3log[start_point:]
            #
            #
            # fig = plt.figure()
            # ax = fig.add_subplot(111, projection='3d')
            # ax.scatter(x, y, z, c=c, cmap=c_palette, marker='.')
            #
            # # plt.imshow(hic_log, interpolation='nearest', cmap=cmap)  # color scale
            # # ax.scatter(hic_log, cmap=cmap, marker='o')
            # # mlab.points3d(x[-2:], y[-2:], z[-2:], cmap=cmap, scale_factor=.25)
            #
            # logger.info(plt.rcParams['axes.prop_cycle'].by_key()['color'])
            #
            # # plt.clim(-2.75, 0)
            # plt.title(f'{title}')
            #
            # # plt.show()
            # file_name = os.path.join(output_folder, f'{file_pref}-{plot_params.cmap}.{format}')
            # logger.info(f'Plot savefig to {file_name} ...')
            #
            # fig.savefig(file_name, dpi=200)
            # plt.close()

            zplot_pd = pd.DataFrame(columns=['s', 'x', 'y', 'c'], index=None)
            zplot_hic = np.zeros((hic3_N, hic3_N)).astype(np.uint8)
            for s in range(1, hic3_N+1):
                # x = []
                # y = []
                # c = []
                zplot = np.zeros((hic3_N, hic3_N)).astype(np.uint8)
                for xi, yi, zi in list(permutations(AXES, 3)):
                    s_ids = np.where(hic3_cool[:, xi] == s)[0]
                    new_x = hic3_cool[s_ids, yi]
                    new_y = hic3_cool[s_ids, zi]
                    new_c = hic3_cool[s_ids, 3]  # hic3_cool_3log[s_ids]
                    zplot[new_x, new_y] = new_c
                    zslice_pd = pd.DataFrame(columns=['s', 'x', 'y', 'c'], index=None)
                    zslice_pd['x'] = new_x
                    zslice_pd['y'] = new_y
                    zslice_pd['c'] = new_c
                    zslice_pd['s'] = s
                    # z_row = {'s': s_ids, 'x': new_x, 'y': new_y, 'c': new_c}
                    zplot_pd = zplot_pd.append(zslice_pd, ignore_index=True)
                    ## logger.info(f'permutation xi:{xi}={s}#{len(s_ids)}, yi:{yi}#{len(new_x)}, zi:{zi}#{len(new_y)}, c#{len(new_c)}')
                    # x.extend(new_x)
                    # y.extend(new_y)
                    # c.extend(new_c)
                zplot_hic = zplot_hic + zplot
                # fig = plt.figure(figsize=(hic3_N, hic3_N))  # , dpi=80)
                fig, ax = plt.subplots()
                logger.info(f'plotting slice {s} ...')
                # plt.scatter(x, y, c=c, cmap=c_palette, marker=',', lw=1, s=1)

                # ax = fig.add_axes([0, 0, 1, 1])
                # ax.axis('off')
                ax.imshow(zplot, interpolation='none')  # cmap=c_palette, interpolation='nearest')  #

                ax.set_xlim((0, hic3_N))
                ax.set_ylim((0, hic3_N))
                # x0, x1 = ax.get_xlim()
                # y0, y1 = ax.get_ylim()
                # ax.set_aspect(abs(x1 - x0) / abs(y1 - y0))
                # for chr in chr_sizes:
                #     ax.hlines(chr // RESOLUTION, xmin=0, xmax=hic3_N, linewidth=1, color='black')
                #     ax.vlines(chr // RESOLUTION, ymin=0, ymax=hic3_N, linewidth=1, color='black')
                hide_axis(ax)
                # plt.title(f'{title}\n slice:{s}')
                # plt.show()

                a_file_name = os.path.join(output_folder,
                                           f'{basename}_{plot_method}-{plot_params.cmap}_s{s:03d}.{format}')
                # a_file_tiff = os.path.join(output_folder, f'{basename}_{plot_method}-{plot_params.cmap}_s{s}.tiff')
                # logger.info(f'Plot savefig to {a_file_name}, {a_file_tiff} ...')
                fig.savefig(a_file_name, format=format)  # , bbox_inches='tight'
                # im = Image.fromarray(zplot)  # .astype(np.uint8))
                # im.save(a_file_name)

                # fig.savefig(a_file_tiff, bbox_inches='tight')
                plt.close()

        save_cooler(zplot_hic, bins, file_prefix=os.path.join(output_folder, f'{basename}_zhic'), balanced=True)
        # plot zplot_hic
        fig, ax = plt.subplots()
        logger.info(f'Plotting Z plane projection ...')
        ax.imshow(zplot_hic, interpolation='none')  # cmap=c_palette, interpolation='nearest')  #
        ax.set_xlim((0, hic3_N))
        ax.set_ylim((0, hic3_N))
        hide_axis(ax)
        a_file_name = os.path.join(output_folder, f'{basename}_zhic.{format}')
        fig.savefig(a_file_name, format=format)  # , bbox_inches='tight'
        plt.close()

        zplot_file_name = os.path.join(output_folder, f'{basename}_zplot.tsv.gz')
        zplot_pd.sort_values(by=['s', 'x', 'y'])
        zplot_pd.to_csv(zplot_file_name, sep='\t', na_rep='.', header=True, index=False, compression='gzip')
        plt.close()


def save_cooler(hic_mat, bins_index, file_prefix, balanced=True):
    resolution = int(bins_index[0][2])
    bins = pd.DataFrame(data=bins_index, columns=['chrom', 'start', 'end'])  # , dtype=np.dtype([('','','')]))
    # bins['chrom'] = chrom
    # pandas data frame way doesn't work for now with cooler 0.8.10!?!
    # pixels_pd = pd.DataFrame(columns=['bin1_id', 'bin2_id', 'count'])   # , dtype=np.dtype([('int64', 'int64', 'int32')]))
    pixels_bin1_id = []
    pixels_bin2_id = []
    pixels_count = []
    for bin1_id in range(hic_mat.shape[0] - 1):
        for bin2_id in range(bin1_id + 1, hic_mat.shape[1]):
            count: np.int32 = hic_mat[bin1_id, bin2_id]
            if count != 0:
                # pixels_pd = pixels_pd.append({'bin1_id': np.int64(bin1_id), 'bin2_id': np.int64(bin2_id), 'count': count}, ignore_index=True)
                pixels_bin1_id.append(np.int64(bin1_id))
                pixels_bin2_id.append(np.int64(bin2_id))
                pixels_count.append(count)
            # else:
            #    print(f'0 pixel ({bin1_id}, {bin2_id})wil be removed')
    pixels_dic = {'bin1_id': pixels_bin1_id, 'bin2_id': pixels_bin2_id, 'count': pixels_count}
    metadata = {'format': 'HDF5::Cooler',
                'format-version': cooler.__version__,
                'bin-type': 'fixed',
                'bin-size': resolution,
                'storage-mode': 'symmetric-upper',
                # 'assembly': 'ce11',
                'generated-by': __init__.__name__ + '-' + __init__.__version__
                # , 'creation-date': datetime.date.today()
                }
    cool_file = file_prefix + '.cool'
    cooler.create_cooler(cool_file, bins=bins, pixels=pixels_dic, ordered=True, metadata=metadata)
    # problem with showing .cool file in higlass but with .mcool it works
    resolutions = [int(i*resolution) for i in COOLER_RESOLUTION_FACTORS]
    if balanced:
        os.system(f'cooler zoomify --balance {cool_file}')
        mcool_file = file_prefix + '.mcool'
        res_str = str(resolutions).strip('[]')
        cmd = f'cooler zoomify --balance -o {mcool_file} -r \'{res_str}\' {cool_file}'
        os.system(cmd)
    else:
        mcool_file = file_prefix + f'.{resolution}.mcool'
        cooler.zoomify_cooler(cool_file, mcool_file, resolutions=resolutions, chunksize=int(10e6))

    return mcool_file


def hide_axis(ax):
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    for position in ["left", "right", "top", "bottom"]:
        ax.spines[position].set_visible(False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("").setLevel(logging.INFO)

    p = get_parser()
    args = p.parse_args(sys.argv[1:])

    if args.command == 'plot':
        plt_params = PlotParams(n_neighbors=args.n_neighbors, min_dist=args.min_dist, metric=args.metric,
                                points_range=args.points_range, cmap=args.cmap)
        plot(args.input_file, output_folder=args.output, chromosome_sizes=args.chromosome_sizes,
             plot_method=args.plot_method, plot_params=plt_params, format=args.file_format)

    elif args.command == 'ins_score':
        hic3d_ins_score(args.input_file, hic3d_file2=args.input_file2, resolution=args.resolution,
                        chrom=args.chromosome, chromosome_sizes=args.chromosome_sizes)
    elif args.command == 'merge':
        merge_hic3d(args.input_file, args.input_file2, output_file=args.output)
    else:
        logger.error(f'Unsupported command {args.run_command}!')
        p.print_help(sys.stderr)
