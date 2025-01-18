from threshold_analyzer import ThresholdAnalyzer

# Simply create an instance of the ThresholdAnalyzer class.
inst3 = ThresholdAnalyzer()
# This is an example of the data structure used in the code.
# It maps each threshold to its confusion matrix parameters.
metrics_list = [{'threshold': 0.1, 'TP': 2, 'TN': 0, 'FP': 8, 'FN': 0},
                {'threshold': 0.2, 'TP': 2, 'TN': 3, 'FP': 5, 'FN': 0},
                {'threshold': 0.3, 'TP': 2, 'TN': 4, 'FP': 4, 'FN': 0},
                {'threshold': 0.4, 'TP': 1, 'TN': 4, 'FP': 4, 'FN': 1},
                {'threshold': 0.5, 'TP': 0, 'TN': 5, 'FP': 3, 'FN': 2},
                {'threshold': 0.6, 'TP': 0, 'TN': 7, 'FP': 1, 'FN': 2},
                {'threshold': 0.7, 'TP': 0, 'TN': 8, 'FP': 0, 'FN': 2},
                {'threshold': 0.8, 'TP': 0, 'TN': 8, 'FP': 0, 'FN': 2},
                {'threshold': 0.9, 'TP': 0, 'TN': 8, 'FP': 0, 'FN': 2}]
# Pass metrics_list to the find_threshold() method.
inst3.process_metrics(metrics_list)

