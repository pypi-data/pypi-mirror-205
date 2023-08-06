
import numpy as np


class Metrics:

    @staticmethod
    def mean_squared_error(y, y_pred):
        return np.mean((y - y_pred) ** 2)

    @staticmethod
    def SSR(y, y_pred):
        return sum((y_pred - np.mean(y)) ** 2)

    @staticmethod
    def SSE(y, y_pred):
        return sum((y_pred - y) ** 2)

    @staticmethod
    def SST(y, y_pred):
        return Metrics.SSR(y, y_pred) + Metrics.SSE(y, y_pred)

    @staticmethod
    def mean_absolute_error(y, y_pred):
        return np.mean(abs(y - y_pred))

    @staticmethod
    def root_mean_squared_error(y, y_pred):
        return np.sqrt(Metrics.mean_squared_error(y, y_pred))

    @staticmethod
    def residual_standart_error(y, y_pred, p):
        return np.sqrt((Metrics.SSE(y, y_pred) / (len(y) + p + 1)))

    @staticmethod
    def r_squared(y, y_pred):
        return Metrics.SSR(y, y_pred) / Metrics.SST(y, y_pred)

    @staticmethod
    def accuracy_score(y_true, y_pred):
        return np.sum(y_true == y_pred) / len(y_true)

    @staticmethod
    def confusion_matrix(y_true, y_pred):

        classes = np.unique(np.concatenate((y_true, y_pred)))
        n = len(classes)
        cjnfusion_matrics = np.zeros(shape=(n, n), dtype=np.int32)
        for i, j in zip(y_true, y_pred):
            cjnfusion_matrics[np.where(classes == i)[0], np.where(classes == j)[0]] += 1  # noqa

        return cjnfusion_matrics

    @staticmethod
    def precision_score(y_true, y_pred, average='auto'):

        classes = np.unique(np.concatenate((y_true, y_pred)))
        if average == 'auto':
            if len(classes) == 2:
                average = 'binary'
            else:
                average = 'micro'

        cm = Metrics.confusion_matrix(y_true, y_pred)
        if average == 'binary':
            tp, fp = cm.ravel()[:2]
            return tp/(tp + fp)

        if average == 'micro':
            tp, fp = list(), list()
            for i in range(len(cm)):
                tp.append(cm[i, i])
                fp.append(sum(np.delete(cm[i], i)))

            tp_all = sum(tp)
            fp_all = sum(fp)
            return tp_all/(tp_all + fp_all)

    @staticmethod
    def f1_score(y_true, y_pred, average='auto'):
        precision = Metrics.__bases__precision_score(
            y_true, y_pred, average)
        recall = Metrics.recall_score(y_true, y_pred, average)
        return 2 * (precision * recall)/(precision + recall)

    @staticmethod
    def recall_score(y_true, y_pred, average='auto'):

        classes = np.unique(np.concatenate((y_true, y_pred)))
        if average == 'auto':
            if len(classes) == 2:
                average = 'binary'
            else:
                average = 'micro'

        cm = Metrics.confusion_matrix(y_true, y_pred)
        if average == 'binary':
            tp, fn = cm.ravel()[[0, 2]]
            return tp/(tp + fn)

        if average == 'micro':
            tp, fn = list(), list()
            for i in range(len(cm)):
                tp.append(cm[i, i])
                fn.append(sum(np.delete(cm[:, i], i)))

            tp_all = sum(tp)
            fn_all = sum(fn)
            return tp_all/(tp_all + fn_all)
