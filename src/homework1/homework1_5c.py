import numpy as np
import homework1_5b as hm1b



def join_intercept(mat):
    ones = np.ones(((len(mat), 1)))

    return np.concatenate((ones, mat), axis=1)


class SpectrumModel():
    """
    The SpectrumModel type packs the smooths of each training example in a data set
    of light spectra together so the entire model can be evaluated conveniently.
    """
    def __init__(self, data_set, features, weight_matrix):
        self._data_set = data_set
        self._features = join_intercept(features.reshape(len(features), 1))

        spectrums = {}
        for i in range(0, len(data_set)):
            W_i = weight_matrix(self._features)
            y_i = data_set[i]
            spectrums[i] = hm1b.LWLRModel(W_i, self._features, y_i)

        self._spectrums = spectrums

    def __call__(self, x):
        return self.evaluate(x)

    def evaluate(self, x):
        """
        Evaluate takes an input vector of wavelengths X, and returns a matrix of 
        estimates such that each row i is a function generated by the smooth of the spectrum from 
        the ith training example. Each column j is the estimate of relative flux by estimator
        i for input value j.
        """
        # First try treating x as a vector. If this succeeds we are evaluating pointwise.
        rows = len(self._spectrums)
        try:
            cols = len(x)
            results = np.zeros((rows, cols))
            for i in range(0, rows):
                results[i] = self._spectrums[i](x)

            return results
        except:
            # Otherwise, try treating it as a scalar.
            results = np.zeros((rows, 1))
            for i in range(0, rows):
                results[i] = self._spectrums[i](x)

            return results

    @property 
    def spectrums(self):
        return self._spectrums


