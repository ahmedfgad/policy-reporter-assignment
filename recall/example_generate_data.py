from threshold_analyzer import ThresholdAnalyzer

# This is an example where the data is generated randomly by the code.
# Number of samples to generate randomly.
num_samples = 10
# Create an instance of the ThresholdAnalyzer class that initializes the data its ground truth.
inst = ThresholdAnalyzer(num_samples)
# Call the find_threshold() method to find the best threshold that satisfies the condition recall >= recall_target
inst.find_threshold()

