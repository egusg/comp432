# %% [code]
import pathlib as pl
import pickle as pkl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
data = []
for path in pl.Path('/content/drive/My Drive/hyper-results/full-experimentEEGNetE2-100').glob('**/*_metrics.pkl'):
    with open(path, 'rb') as f:
        metrics = pkl.load(f)
    parts = path.parts
    set_ = parts[-1].split('_')[0]
    session = parts[-2]
    subject = parts[-3]
    trial = parts[-7]
    seed = parts[-5]
    run = parts[-6]
    metrics.update(session=session, subject=subject, trial=trial, seed=seed, run=run, set=set_)
    data.append(metrics)

# Create DataFrame
data = pd.DataFrame(data)
data = data.set_index(['trial', 'session', 'subject', 'set'])
valid = data.xs('valid', level='set')
test = data.xs('test', level='set')
data = valid.join(test, lsuffix='_valid', rsuffix='_test')

# Plot
sns.scatterplot(data=data, x='acc_valid', y='acc_test', hue='subject')
plt.xlim(0, 1.0)
plt.ylim(0, 1.0)
plt.title("Plot of EEGNetE2.yaml")  # Add your plot title here
plt.show()
