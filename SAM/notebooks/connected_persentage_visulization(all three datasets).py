import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 1. Load the data
data = pd.read_csv('/home/yiming/WorkSpace/scripts/dataset_percentages.csv')

# 2. Calculate the percentage representation for each dataset
data['2018_DSB_percentage'] = (data['2018_DSB'] / data['2018_DSB'].sum()) * 100
data['MoNuSeg_percentage'] = (data['MoNuSeg'] / data['MoNuSeg'].sum()) * 100
data['TissueNet_percentage'] = (data['TissueNet'] / data['TissueNet'].sum()) * 100

# 3. Define the x-axis limits for each dataset
xlims = {
    '2018_DSB_percentage': max(data['2018_DSB_percentage']) * 1.1,
    'MoNuSeg_percentage': max(data['MoNuSeg_percentage']) * 1.1,
    'TissueNet_percentage': max(data['TissueNet_percentage']) * 1.1
}

# 4. Define a custom formatter for x-axis labels to display absolute values
def format_abs(x, _):
    return "{:.0f}".format(abs(x))

# 5. Adjust the global font settings for better visibility
plt.rcParams.update({
    'font.size': 14,
    'font.weight': 'bold',
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold'
})

# 6. Plot the data
fig, axs = plt.subplots(1, 3, figsize=(16, 8), sharey=True)
datasets = ['2018 DSB', 'MoNuSeg', 'TissueNet']
percentage_columns = ['2018_DSB_percentage', 'MoNuSeg_percentage','TissueNet_percentage']

for idx, (dataset, percentage_column) in enumerate(zip(datasets, percentage_columns)):
    axs[idx].barh(data['percentage'], data[percentage_column], align='center', height=1,
                  color=['b', 'g', 'r'][idx], alpha=0.7, left=-data[percentage_column]/2)
    axs[idx].set_title(dataset)
    axs[idx].grid(axis='x', linestyle='--')
    axs[idx].set_xlim(-xlims[percentage_column], xlims[percentage_column])
    axs[idx].xaxis.set_major_formatter(FuncFormatter(format_abs))

axs[0].set_xlabel('Percentage of Total Images',fontsize=16)
axs[1].set_xlabel('Percentage of Total Images',fontsize=16)
axs[2].set_xlabel('Percentage of Total Images',fontsize=16)
axs[0].set_ylabel('Percentage of connected nucleus',fontsize=25)

plt.tight_layout()
plt.show()

# 7. Reset the global font settings to default
plt.rcParams.update(plt.rcParamsDefault)
