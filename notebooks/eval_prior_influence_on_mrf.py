import numpy as np
np.random.seed(7)

import skimage.io as skio
import matplotlib.pyplot as plt

from stereovis.framed.algorithms.mrf import StereoMRF


if __name__ == '__main__':
    # Read left and right images as well as ground truth
    img_left = skio.imread("/Users/admin/Documents/University/TUM/Master_Info/SS17/IDP/SemiframelessStereoVision/"
                           "hybrid-stereo-matching/data/input/frames/head/left/32.png", as_grey=True)
    img_right = skio.imread("/Users/admin/Documents/University/TUM/Master_Info/SS17/IDP/SemiframelessStereoVision/"
                           "hybrid-stereo-matching/data/input/frames/head/right/32.png", as_grey=True)
    # img_left = skio.imread("/Users/admin/Documents/University/TUM/Master_Info/SS17/IDP/SemiframelessStereoVision/"
    #                        "hybrid-stereo-matching/data/demo_samples/motorcycle_l.png", as_grey=True)
    # img_right = skio.imread("/Users/admin/Documents/University/TUM/Master_Info/SS17/IDP/SemiframelessStereoVision/"
    #                         "hybrid-stereo-matching/data/demo_samples/motorcycle_r.png", as_grey=True)
    # ground_truth = load_ground_truth("/Users/admin/Documents/University/TUM/Master_Info/SS17/IDP/SemiframelessStereoVision/"
    #                                  "hybrid-stereo-matching/data/demo_samples/motorcycle_gt.pfm")
    # print(ground_truth.shape)

    # since the images are too large, e.g. 1980 x 2880, scale them down
    # NOTE: rescale the disparity too!
    scale_down_factor = 1.0
    if scale_down_factor != 1.0:
        from skimage.transform import rescale

        img_left = rescale(img_left, 1.0 / scale_down_factor, preserve_range=True)
        img_right = rescale(img_right, 1.0 / scale_down_factor, preserve_range=True)
        # ground_truth = rescale(ground_truth, 1.0 / scale_down_factor, preserve_range=True) / scale_down_factor

    # ground_truth = ground_truth.astype('int16')

    # skio.imshow_collection([img_left, img_right, ground_truth])
    # plt.show()
    # print("Image resolution: {}".format(img_left.shape[::-1]))
    # max_disp = np.max(ground_truth)
    # print("Max disparity: {}".format(max_disp))

    # Initialise a MRF and calculate the some (possible sub-optimal) disparity assignment
    img_res = img_left.shape
    # img_left = np.concatenate([img_left[0, 100] * np.ones((1, img_left.shape[1])), img_left[:-1, :]], axis=0)
    mrf = StereoMRF(img_res, n_levels=55 + 1)
    disp_map = mrf.lbp(img_left/255., img_right/255., n_iter=15)
    # disp_map[disp_map <= 5] = 0
    # plt.imshow(disp_map, cmap=cm.jet)
    # plt.colorbar()
    skio.imshow_collection([disp_map, img_right, img_left])
    plt.show()

    # Run the LBP algorithm again with the same image pair but provide a retina-like prior,
    # sampled from the ground truth + noise
    # prior_density = 0.01
    # edges_mask = skft.canny(ground_truth.astype('float'), sigma=2)
    # prior = ground_truth * (np.random.uniform(size=img_left.shape) <= prior_density)
    # prior = prior * edges_mask
    # prior[prior == 0] = max_disp + 2
    # skio.imshow(prior)
    # plt.show()

    # disp_map_with_prior = mrf.lbp(img_left, img_right, prior=None, prior_trust_factor=0, n_iter=10)
    # skio.imshow_collection([disp_map, disp_map_with_prior, prior])
    # plt.show()

    # clipped_ground_truth = ground_truth[18:-18, 18:-18]
    # clipped_without_prior = disp_map[18:-18, 18:-18]
    # clipped_with_prior = disp_map_with_prior[18:-18, 18:-18]

    # print("RMSE w/o prior: {}".format(np.sqrt(np.mean((clipped_without_prior - clipped_ground_truth) ** 2))))
    # print("RMSE w. prior: {}".format(np.sqrt(np.mean((clipped_with_prior - clipped_ground_truth) ** 2))))
