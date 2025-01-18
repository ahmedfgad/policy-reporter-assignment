import numpy
from sklearn.metrics import confusion_matrix

class ThresholdAnalyzer:
    """
    A class for performing classification threshold analysis based on prediction scores and ground truth data.

    Attributes:
        found_thresholds (list): A list of thresholds where recall >= 0.9.
        metrics_list (list): A list to store performance metrics (TP, TN, FP, FN) for each threshold.
        threshold (float): The best threshold where recall is maximized.
        ground_truth (numpy.ndarray): Ground truth labels (0 or 1).
        prediction_scores (numpy.ndarray): Prediction scores for classification.
    """
    
    found_thresholds = [] # Stores thresholds with recall >= 0.9
    metrics_list = [] # Stores performance metrics for each threshold
    threshold = None # Best threshold for classification
    ground_truth = [] # Ground truth labels
    prediction_scores = [] # Prediction scores

    def __init__(self, num_samples=None):
        """
        Initialize the classification data with random prediction scores and ground truth labels.

        Args:
            num_samples (int, optional): The number of samples to generate for testing.
                If None, no data will be created. Defaults to None.
        """
        if num_samples is None:
            print("No data is created!")
        elif isinstance(num_samples, int):
            prediction_scores = numpy.random.rand(num_samples)
            # Generate an array of zeros as the ground truth data.
            ground_truth = numpy.random.randint(low=0, high=1, size=num_samples)
            num_positives = numpy.random.randint(low=int(num_samples/4), high=int(num_samples/1.5), size=1)[0]
            positives_indices = numpy.random.choice(range(0, num_samples), size=num_positives, replace=False)
            ground_truth[positives_indices] = 1

            self.ground_truth = numpy.array(ground_truth)
            self.prediction_scores = numpy.array(prediction_scores)
            print(f"GT number of TPs: {sum(self.ground_truth)}")
            print(f"GT number of TNs: {num_samples-sum(self.ground_truth)}")
        else:
            print("Expected an integer for the number of samples!")

    def filter_thresholds(self, recall_target=0.9):
        """
        Filter and identify the best threshold from the found thresholds.

        This method checks the `found_thresholds` attribute, which should be a list of threshold-recall pairs.
        It sorts the thresholds based on the recall values in descending order and returns the threshold with the 
        highest recall. If no valid thresholds are found, it will print a message and return None.

        Args:
            recall_target: The target recall.

        Returns:
            float or None: The best threshold if found, else None.
        """
        if not type(self.found_thresholds) is list or not len(self.found_thresholds) > 0:
            print("The found_thresholds attribute must be a non-empty list!")
            return None
        if len(self.found_thresholds) > 0:
            print(f"Found {len(self.found_thresholds)} threshold(s): {[el[0] for el in self.found_thresholds]}")
            sorted_data = sorted(self.found_thresholds, key=lambda x: x[1], reverse=True)
            self.threshold = sorted_data[0][0]
            print(f"The best threshold is {self.threshold}")
            return self.threshold
        else:
            print(f"No threshold found satisfying the condition recall >= {recall_target}")
            return None

    def find_threshold(self, recall_target=0.9):
        """
        Find the optimal threshold where recall is greater than or equal to recall_target.

        This method loops through potential thresholds (from 0.1 to 0.9) and computes the confusion matrix
        for each threshold. It stores the thresholds that yield a recall of recall_target or more and returns the best
        threshold with the highest recall.

        Args:
            recall_target: The target recall.

        Returns:
            float or None: The best threshold if found, else None.
        """
        if not isinstance(self.ground_truth, numpy.ndarray) or not isinstance(self.prediction_scores, numpy.ndarray):
            print("The 2 attributes ground_truth and prediction_scores must be NumPy arrays!")
            return None
        elif not len(self.ground_truth.shape) == len(self.prediction_scores.shape) == 1 or not self.ground_truth.shape[0] == self.prediction_scores.shape[0]:
            print("The 2 attributes ground_truth and prediction_scores must be 1D NumPy arrays!")
            return None
        elif len(self.ground_truth) == 0 or len(self.prediction_scores) == 0:
            print("Cannot proceed without having data!")
            return None

        # Initialize an empty list to store metrics for each threshold
        self.metrics_list = []
        self.found_thresholds = []

        # Loop through thresholds from 0.1 to 0.9
        for threshold in numpy.arange(0.1, 1.0, 0.1):
            # Get the predicted labels based on the threshold
            data_predicted = self.prediction_scores >= threshold

            # Calculate the confusion matrix
            tn, fp, fn, tp = confusion_matrix(self.ground_truth, data_predicted).ravel()

            # Append the metrics as a dictionary for the current threshold
            self.metrics_list.append({'threshold': round(threshold, 1),
                                      'TP': tp,
                                      'TN': tn,
                                      'FP': fp,
                                      'FN': fn})

            # Calculate the recall for the current threshold
            recall = tp / (tp + fn) if (tp + fn) != 0 else 0
            if recall >= recall_target:
                self.found_thresholds.append([threshold, recall])

        return self.filter_thresholds()

    def process_metrics(self, metrics_list, recall_target=0.9):
        """
        Process and find the best threshold from a given list of metrics.

        This method is similar to `find_threshold()` but allows passing a pre-calculated list of metrics
        instead of using the internal `ground_truth` and `prediction_scores`.

        Args:
            metrics_list (list): A list of dictionaries containing 'threshold', 'TP', 'TN', 'FP', and 'FN' values.
            recall_target: The target recall.

        Returns:
            float or None: The best threshold if found, else None.
        """
        self.found_thresholds = []
        if type(metrics_list) is list:
            pass
        else:
            raise TypeError(f'The type of the metrics data structure must be a list but {type(metrics_list)} found.')

        for record in metrics_list:
            if type(record) is dict and 'threshold' in record and 'TP' in record and 'TN' in record and 'FP' in record and 'FN' in record:
                pass
            else:
                raise ValueError('Each record in the dictionary must have the 5 keys: threshold, TP, TN, FP, and FN.')

            tp = record['TP']
            tn = record['TN']
            fp = record['FP']
            fn = record['FN']

            # Avoid division by zero
            recall = tp / (tp + fn) if (tp + fn) != 0 else 0
            if recall >= recall_target:
                self.found_thresholds.append([record['threshold'], recall])

        return self.filter_thresholds()
