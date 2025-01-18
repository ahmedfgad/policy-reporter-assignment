from threshold_analyzer import ThresholdAnalyzer
import numpy

# Simply create an instance of the ThresholdAnalyzer class and override the 2 attributes: 1) prediction_scores 2) ground_truth
inst2 = ThresholdAnalyzer()
inst2.prediction_scores = numpy.array([0.34, 0.24, 0.34, 0.73, 0.42, 0.55, 0.66, 0.53, 0.34, 0.97])
inst2.ground_truth = numpy.array([0, 1, 1, 0, 1, 1, 0, 0, 1, 1])
inst2.find_threshold()
