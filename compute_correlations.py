import os
from collections import Counter
import numpy as np
import pandas as pd
from scipy.stats import pointbiserialr
import seaborn as sns
import matplotlib.pyplot as plt


def load_data():
    """Load and process data files to create a dictionary of book data."""

    data = {}

    canonical = ['sche034janc01_01', 'du_p001land01_01', 'braa002drdu01_01', 'buys009tbol01_01', 'deys001lief01_01',
                 'timm010pall01_01', 'eman001nage01_01', 'eede003vand04_01', 'stre009vlas01_01', 'bord001kara01_01',
                 'vest002mene02_01', 'ouds001will01_01', 'busk001lide01_01', 'lenn006klaa01_01', 'wals004adel01_01',
                 'mees009geer01_01', 'roel004kome01_01', 'szek002rubb01_01', 'helm003stil02_01', 'slau001verb01_01']

    non_canonical = ['drie015moed02_01', 'huiz004adri01_01', 'wijn150timt01_01', 'hoev006were01_01', 'stra018verb01_01',
                     'bosm004witt01_01', 'revi002krin01_01', 'thij006taai01_01', 'lapi001vrij01_01', 'schr014kron02_01',
                     'avan003doll01_01', 'veer004fran01_01', 'koen006hofk01_01', 'reyn008roma02_01', 'pott003robe01_01',
                     'cool004drie02_01', 'maur005oude01_01', 'crof001wiei01_01', 'buys010spok01_01', 'zegg001kolo01_01']

    for file in os.listdir('./tag'):
        book_identifier, ext = os.path.splitext(file)
        if ext == '.icarus':
            # Get labels per file
            with open(os.path.join('./tag', file), encoding='utf-8') as f:
                labels = [line.strip().split(';')[-1].split(':')[1] for line in f
                          if not line.startswith('#end') and 'category' in line]

            # Get number of tokens in file
            with open(os.path.join('./tag', book_identifier + '.conll'), encoding='utf-8') as f:
                count = sum(1 for line in f if line.startswith(book_identifier))

            # Get prestige
            if book_identifier in canonical:
                prestige = 'prestigious'
            elif book_identifier in non_canonical:
                prestige = 'not_prestigious'

            data[book_identifier] = {'n_tokens': count,
                                     'frequencies': Counter(labels),
                                     'prestige': prestige}

    return data


def report_correlations(data):
    """Generate correlation analysis and violin plots for relative frequencies of different categories
    with respect to a binary prestige variable."""

    labels = ['PER', 'PKM', 'MISC', 'OBJ', 'LOC', 'ORG']
    relative_frequencies = np.array(
        [[entry['frequencies'][label] / entry['n_tokens'] for label in labels] for entry in data.values()])
    prestige_values = np.array([1 if entry['prestige'] == 'prestigious' else 0 for entry in data.values()])

    for i, label in enumerate(labels):
        correlation, p_value = pointbiserialr(relative_frequencies[:, i], prestige_values)

        print("For class", label)
        print("Correlation:", correlation)
        print("p-value:", p_value)
        print()

        plot_data = {'Prestigious': relative_frequencies[prestige_values == 1, i],
                     'Not Prestigious': relative_frequencies[prestige_values == 0, i]}
        df = pd.DataFrame(plot_data)

        sns.violinplot(data=df, palette='Greens')

        # Set labels and title
        plt.xlabel('Class')
        plt.ylabel('Relative Frequency')
        plt.title(f'Distribution of category {label}')

        # Save plot
        plt.savefig('./figures/violin_' + label)

        # Display the plot
        plt.show()


def main():
    data = load_data()
    report_correlations(data)


if __name__ == '__main__':
    main()
