import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd

sns.set_style("ticks")


def check_contact(mask_array, value):
    kernel = np.array([
        [-1, -1], [-1, 0], [-1, 1],
        [0, -1], [0, 1],
        [1, -1], [1, 0], [1, 1]
    ])

    y_indices, x_indices = np.where(mask_array == value)
    for y, x in zip(y_indices, x_indices):
        for dy, dx in kernel:
            ny, nx = y + dy, x + dx
            if 0 <= ny < mask_array.shape[0] and 0 <= nx < mask_array.shape[1]:
                if mask_array[ny, nx] != 0 and mask_array[ny, nx] != value:
                    return True
    return False


def process_mask_updated(mask_array):
    unique_non_zero_values = np.unique(mask_array[mask_array > 0])
    total_instances = len(unique_non_zero_values)
    contacted_instances = sum([1 for value in unique_non_zero_values if check_contact(mask_array, value)])
    contacted_percentage = max(0, (100.0 * contacted_instances / total_instances)) if total_instances != 0 else 0
    return total_instances, contacted_instances, contacted_percentage


data_stats = {'dataset': [], 'contacted_percentage': []}


def process_datasets_statistics():
    dataset_stats = {
        '2018_DSB': {'total_images': 0, 'total_instances': 0, 'contacted_instances': 0, 'all_percentages': []},
        'TissueNet': {'total_images': 0, 'total_instances': 0, 'contacted_instances': 0, 'all_percentages': []},
        'MoNuSeg': {'total_images': 0, 'total_instances': 0, 'contacted_instances': 0, 'all_percentages': []}
    }

    # Process 2018_DSB dataset
    masks_directory = "/home/yiming/WorkSpace/datasets/2018_DSB/original_masks"
    all_files = [f for f in os.listdir(masks_directory) if f.endswith(".png")]
    for idx, mask_file in enumerate(all_files):
        mask_path = os.path.join(masks_directory, mask_file)
        mask_image = Image.open(mask_path)
        mask_array = np.array(mask_image)
        total, contacted, perc = process_mask_updated(mask_array)
        dataset_stats['2018_DSB']['total_images'] += 1
        dataset_stats['2018_DSB']['total_instances'] += total
        dataset_stats['2018_DSB']['contacted_instances'] += contacted
        dataset_stats['2018_DSB']['all_percentages'].append(perc)
        data_stats['dataset'].append('2018_DSB')
        data_stats['contacted_percentage'].append(perc)
        print(f"2018_DSB: Processed {idx + 1}/{len(all_files)} images...")

    # Process TissueNet dataset
    TisssueNet_Dataset_Root = '/home/yiming/WorkSpace/datasets/tissuenet_1.0'
    for dataset_name in ['test', 'train', 'val']:
        dataset_dict = np.load(os.path.join(TisssueNet_Dataset_Root, 'tissuenet_v1.0_' + dataset_name + '.npz'))
        y = dataset_dict['y']
        nuclear_masks = y[..., 1]
        for idx, mask_array in enumerate(nuclear_masks):
            total, contacted, perc = process_mask_updated(mask_array)
            dataset_stats['TissueNet']['total_images'] += 1
            dataset_stats['TissueNet']['total_instances'] += total
            dataset_stats['TissueNet']['contacted_instances'] += contacted
            dataset_stats['TissueNet']['all_percentages'].append(perc)
            data_stats['dataset'].append('TissueNet')
            data_stats['contacted_percentage'].append(perc)
            print(f"TissueNet ({dataset_name}): Processed {idx + 1}/{len(nuclear_masks)} images...")

    # Process MoNuSeg dataset with the split
    masks_directory = "/home/yiming/WorkSpace/datasets/MoNuSeg/all_masks"
    all_files = [f for f in os.listdir(masks_directory) if f.endswith(".png")]
    for idx, mask_file in enumerate(all_files):
        mask_path = os.path.join(masks_directory, mask_file)
        mask_image = Image.open(mask_path)
        mask_array = np.array(mask_image)
        sub_masks = [
            mask_array[0:512, 0:512],
            mask_array[0:512, 512:1024],
            mask_array[512:1024, 0:512],
            mask_array[512:1024, 512:1024]
        ]
        for sub_mask in sub_masks:
            total, contacted, perc = process_mask_updated(sub_mask)
            dataset_stats['MoNuSeg']['total_images'] += 1
            dataset_stats['MoNuSeg']['total_instances'] += total
            dataset_stats['MoNuSeg']['contacted_instances'] += contacted
            dataset_stats['MoNuSeg']['all_percentages'].append(perc)
            data_stats['dataset'].append('MoNuSeg')
            data_stats['contacted_percentage'].append(perc)
        print(f"MoNuSeg: Processed {idx + 1}/{len(all_files)} images (with 4 splits each)...")

    return dataset_stats


def save_to_csv():
    df = pd.DataFrame(data_stats)
    bins = np.arange(0, 101, 1)
    df['binned'] = pd.cut(df['contacted_percentage'], bins, right=False, labels=bins[:-1])
    final_data = {}
    for dataset in df['dataset'].unique():
        subset = df[df['dataset'] == dataset]
        count_series = subset.groupby('binned').size()
        final_data[dataset] = count_series.reindex(bins[:-1], fill_value=0).values
    final_df = pd.DataFrame(final_data)
    final_df['percentage'] = bins[:-1]
    final_df.to_csv("dataset_percentages.csv", index=False)


# Gather statistics
dataset_stats = process_datasets_statistics()

# Print the statistics
for dataset, stats in dataset_stats.items():
    print(f"Dataset: {dataset}")
    print(f"Total images: {stats['total_images']}")
    print(f"Total instances: {stats['total_instances']}")
    print(f"Total contacted instances: {stats['contacted_instances']}")
    print(f"Contacted instance ratio: {100 * stats['contacted_instances'] / stats['total_instances']:.2f}%")
    print(f"Average contacted instance percentage across images: {np.mean(stats['all_percentages']):.2f}%")
    print('-' * 50)

# Save the data
save_to_csv()
