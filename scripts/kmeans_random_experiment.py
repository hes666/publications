"""
Run the experimental procedure of the 
K-Means Oversampling paper.
"""

# Author: Georgios Douzas <gdouzas@icloud.com>
# License: MIT

# Imports
from os.path import join, dirname

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors.classification import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearnext.cluster import KMeans
from sklearnext.tools import evaluate_binary_imbalanced_experiments, read_csv_dir, summarize_binary_datasets
from sklearnext.over_sampling import RandomOverSampler, SMOTE, GeometricSMOTE
from sklearnext.over_sampling import DensityDistributor

# Paths
datasets_path = join(dirname(__file__), '..', 'data', 'binary-numerical-imbalanced')
results_path = join(dirname(__file__), '..', 'data', 'results', 'kmeans-oversampling', 'random-oversampler')

# Oversamplers and classifiers
oversamplers = [
    ('NO OVERSAMPLING', None),
    ('RANDOM OVERSAMPLING', RandomOverSampler(random_state=0)),
    ('K-MEANS RANDOM OVERSAMPLING', RandomOverSampler(clusterer=KMeans(random_state=2), distributor=DensityDistributor(), random_state=1) , {
        'clusterer__n_clusters': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        'distributor__distances_exponent': [0, 1, 2, 5],
        'distributor__filtering_threshold': [0.0, 0.5, 1.0, 2.0],
        }
    ), 
]
classifiers = [
    ('LR', LogisticRegression()),
    ('KNN', KNeighborsClassifier(), {'n_neighbors':[3, 5]}),
    ('DT', DecisionTreeClassifier(random_state=3), {'max_depth': [3, 6]}),
    ('GBC', GradientBoostingClassifier(random_state=4), {'max_depth':[3, 6], 'n_estimators':[50, 100]})
]

# Load datasets
imbalanced_datasets = read_csv_dir(datasets_path)

# Summarize datasets
imbalanced_datasets_summary = summarize_binary_datasets(imbalanced_datasets)

# Run main experiment
results = evaluate_binary_imbalanced_experiments(datasets=imbalanced_datasets,
                                                 oversamplers=oversamplers,
                                                 classifiers=classifiers,
                                                 scoring=['roc_auc', 'f1', 'geometric_mean_score'],
                                                 n_splits=5,
                                                 n_runs=3,
                                                 random_state=5)

# Save various datasets 
imbalanced_datasets_summary.to_csv(join(results_path, 'imbalanced_datasets_summary.csv'), index=False)
for name, result in results.items():
    result.to_csv(join(results_path, '%s.csv' % name), index=(name == 'aggregated'))
