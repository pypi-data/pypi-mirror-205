
import numpy as np
from IPython.display import display, Latex
# ==========================================================================================================================================|
# ===================================================================Linear_Regressor================================================|
# ==========================================================================================================================================|

# OLS
# https://www.youtube.com/watch?v=sl3MM_i3az8&list=PL4_hYwCyhAvasRqzz4w562ce0esEwS0Mt&index=3
# https://www.youtube.com/watch?v=bOIPwdWso_0&list=RDCMUC5_6ZD6s8klmMu9TXEB_1IA&index=8
# https://www.youtube.com/watch?v=z2hpinQggNM&list=RDCMUC_lePY0Lm0E2-_IkYUWpI5A&index=2 - digg into

# Lasso
# https://www.youtube.com/watch?v=eGXw9n7AnV4

# while Linear Algebra Mastering
# https://www.youtube.com/watch?v=--aZGoTBibA&list=PL4_hYwCyhAvYAPsfeaIWH6cBb8Js9lLNt&index=2 Regulariasation MFTI
# https://www.youtube.com/watch?v=sl3MM_i3az8&list=PL4_hYwCyhAvasRqzz4w562ce0esEwS0Mt&index=2  Regulariasation MFTI

# https://towardsdatascience.com/intuitions-on-l1-and-l2-regularisation-235f2db4c261


class Linear_Regressor:

    def __init__(self, _fit_method="OLS", _learning_rate=0.01, _tolerance=0.0001, _iterations=1000, _batch_size=None, _momentum=None, _regularisation=None, _alpha=None, _ratio=None):

        self.fit_method = _fit_method
        self.learning_rate = _learning_rate
        self.tolerance = _tolerance
        self.iterations = _iterations
        self.batch_size = _batch_size
        self.momentum = _momentum
        self.regularisation = _regularisation
        self.alpha = _alpha
        self.ratio = _ratio

    def _mse(self, y_true, y_pred):
        return np.mean((y_true - y_pred) ** 2)

    def fit(self, X, y):

        if self.fit_method == 'OLS':

            ones = np.ones(len(X)).reshape(-1, 1)
            X = np.concatenate((ones, X), axis=1)

            model_coeficients = np.matmul(np.linalg.pinv(np.matmul(X.T, X)), np.matmul(X.T, y))  # noqa

            self.weights = model_coeficients[1:]
            self.intercept = model_coeficients[0]

        else:

            n_samples, n_features = X.shape
            self.weights = np.zeros(n_features)
            self.intercept = 0
            mse_prev = np.inf
            prev_d_weights, prev_d_weights = 0.0, 0.0
            w_momentum, i_momentum = 0

            for _ in range(self.iterations):

                if self.batch_size is not None:
                    batch = np.random.sample(range(0, n_samples), self.batch_size)  # noqa
                    X = np.array(X[batch, :])
                    y = np.array(y[batch, :])

                regularisation_term = 0
                if self.regularisation is not None:
                    regularisation_term = (self.alpha * self.ratio + 2 * self.alpha * (1 - self.ratio) * self.weights)  # noqa

                if self.momentum is not None:
                    w_momentum = self.momentum * prev_d_weights
                    i_momentum = self.momentum * prev_d_intercept

                y_pred = self.predict(X)

                d_weights = 2 / n_samples * ((X.T).dot(y_pred - y) + regularisation_term) + w_momentum  # noqa
                d_intercept = 2 / n_samples * np.sum(y_pred - y) + i_momentum  # noqa

                self.weights -= self.learning_rate * d_weights
                self.intercept -= self.learning_rate * d_intercept

                current_mse = self._mse(y, y_pred)

                if abs(current_mse - mse_prev) < self.tolerance:
                    break

                if self.momentum:
                    prev_d_weights = d_weights
                    prev_d_intercept = d_intercept

                mse_prev = current_mse

    def predict(self, X):
        return np.dot(X, self.weights) + self.intercept

    def _pick_best_hyperparameters(self):
        pass

    @staticmethod
    def _explain_ols():
        display(Latex(
            r"""
                $Y_i = \theta_0 + \theta_1X_i + e_i(error)$
                $\hat Y_i = \hat \theta_0 + \hat \theta_1X_i$
                $\hat Y_i - \text{predicted}$
                $e_i = Y_i − \hat Y_i$

                $\text{Goal is to minimise SSE}$

                $\href{https://365datascience.com/tutorials/statistics-tutorials/sum-squares/}
                {SSE } = \sum_{i=1}^N (Y_i - \hat Y_i)^2 = \sum_{i=1}^N(Y_i - (\hat \theta_0 + \hat \theta_1 X_i))^2=
                \text{SSR + SSE} =\sum_{i=1}^N(\hat Y_i-\bar Y)^2 + \sum_{i=1}^n(\hat Y_i -  Y_i)^2$

                $$\hat \theta_1 = \frac{\sum_{i=1}^n(X_i - \bar X)(Y_i - \bar Y)}{\sum_{i=1}^N(X_i - \bar X)^2} =
                \frac {cov(X,Y)}{var(X)}$$
                $$\hat \theta_0 = \bar Y - \hat \theta_1 \bar X$$

                \text{NOTE:}

                $\sum_{i=1}^N(x_i - \bar x) = 0$

                $\text{Because: }$

                $\sum_{i=1}^N(x_i - \bar x) = (x_1 - \bar x) + (x_2 - \bar x) + ... (x_n - \bar x) = (x_1 + x_2 + .... + x_N) - N \bar x$
                $(x_1 + x_2 + .... + x_N) - N \frac {\sum_{i=1}^N x}{N}$
                $(x_1 + x_2 + .... + x_N) - \sum_{i=1}^N x = 0$
                 
                \text{TUTORIALS:}

                $\href{https://www.youtube.com/watch?v=sL3P5wBRkZo&list=PLq4u7PZJwOGuMscNUwxVxKiPvj5My4Saj&index=8}
                {Intro to Linear Regression}$
                $\href{https://www.youtube.com/watch?v=Ts1mvmym97w&list=PLq4u7PZJwOGuMsc}
                {Math behind Linear Regression}$
         """
        ))

    @staticmethod
    def _explain_gd():
        display(Latex(
            r"""
                    $\text{Derivative}$

                    $$\frac{d f}{d x_0} = \lim_{h \to 0}\frac{f(x_0+h) - f(x_0)}{h}$$

                    $\text{Partial Derivative}$

                    $f: R^n -> R$
                    $ f(x_1,x_2, ... ,x_n) = \begin{align}
                        f(\begin{bmatrix}
                            x_1 \\
                            x_2  \\
                            \vdots \\
                            x_n
                            \end{bmatrix} \in R^n)
                    \end{align}$

                    $$ \frac{\delta}{\delta x_1}f(x_1,x_2, ... ,x_n) = \lim_{h \to 0}\frac{f(x_1 + h,x_2, ... , x_n) - f(x_1,x_2, ... ,x_n)}{h}$$
                    $$ \frac{\delta}{\delta x_2}f(x_1,x_2, ... ,x_n) = \lim_{h \to 0}\frac{f(x_1,x_2 + h, ... , x_n) - f(x_1,x_2, ... ,x_n)}{h}$$
                    $$ \frac{\delta}{\delta x_n}f(x_1,x_2, ... ,x_n) = \lim_{h \to 0}\frac{f(x_1,x_2,... ,x_n + h) - f(x_1,x_2, ... , x_n)}{h}$$

                    $\text{Gradient}$

                    $$grad f = \nabla f = \frac{\delta f}{\delta x}\vec i + \frac{\delta f}{\delta y}\vec j + \frac{\delta f}{\delta z}\vec k$$

                    $\text{Directional Derivative}$

                    $\text{Directional derivative of the function f(x,y,z) - is a projection of the gradient vector onto a given direction(some unit vector)}$

                    $\text{Let we have a function $f(x,y,z)$ and a vector $\vec r(x,y,z)$}$

                    $\text{It would be more convenient to convert this vector int unit one by expressing its components like:}$

                    $$cos(\alpha) = \frac{x}{|\vec r|}$$
                    $$cos(\beta) = \frac{y}{|\vec r|}$$
                    $$cos(\gamma) = \frac{z}{|\vec r|}$$

                    $\text{Now we got $\vec r_0$ that has same direction, another module == 1 because after dividing each vector component on the same number it direction stay the same}$

                    $\vec r_0 = (cos(\alpha),cos(\beta),cos(\gamma))$

                    $\text{Proof that $\vec r_0$ is unit vector:}$

                    $$|\vec r| = \sqrt{cos(\alpha) + cos(\beta) + cos(\gamma)} = \sqrt{\frac{x^2}{|\vec r|^2} + \frac{y^2}{|\vec r|^2} + \frac{z^2}{|\vec r|^2}} = \sqrt{\frac{x^2 + y^2 + z^2}{|\vec r|^2}} =  \frac{ \sqrt{x^2 + y^2 + z^2} }{\sqrt{|\vec r|^2}} = 1$$

                    $D_{\vec r_0}f(x,y,z) = \frac{\delta f}{\delta r} = \frac{\delta f}{\delta x}cos(\alpha) + \frac{\delta f}{\delta y}cos(\beta) + \frac{\delta f}{\delta z}cos(\gamma) = grad f(x,y,z) * \vec r_0  = |grad f(x,y,z)| * |\vec r_0| * cos(\theta) = |grad f(x,y,z)| * 1 * cos(\theta)$
                    $\theta = \llcorner	(grad f,\vec r_0)$

                    $\text{Max $\frac{\delta f}{\delta \vec r_0}$ when  $cos(\theta) = 1,\theta = 0$ , so $\frac{\delta f}{\delta \vec{r_0}} = |\nabla f(x,y)|$ when gradient vector is a projection onto vector $\vec r_0$ , so $\vec r_0$ points to the direction of the gradient that points to the direction of the steepest function ascend}$

                    $\text{Directional derivative limit formula:}$
                    $\text{Let we have unit vector $\vec r_0(a,b,c)$}$
                    $$\frac{\delta f(x,y,z)}{\delta{\vec r_0}} = \lim_{h \to 0}\frac{f(x + ha,y + hb, z + hc) - f(a,b,c)}{h}$$
                    $\text{We multiply each nudge h by this components because we need to distinguish that we are moving in the direction of the vector $r_0$}$

                    
                    $\text{TUTORIALS:}$

                    $\href{https://medium.com/swlh/the-math-of-machine-learning-i-gradient-descent-with-univariate-linear-regression-2afbfb556131}
                    {\text{Intro}}$
                    $\href{https://www.youtube.com/watch?v=ZoCxUV893fo}
                    {\text{Directional cosines}}$
                    $\href{https://www.youtube.com/watch?v=gv68-RppB8g&t=322s}
                    {\text{Why the gradient points to the steepest ascent}}$
                    $\href{https://www.youtube.com/watch?v=tDPp5uWSIiU&list=PLDesaqWTN6ESk16YRmzuJ8f6-rnuy0Ry7&index=18}
                    {\text{Lecture about Gradients and Directional Derivatives}}$
          
            """
        ))

    @staticmethod
    def _explain_regularisation():
        display(Latex(
            r"""
            
         """
        ))


# ===================================================================== TO_DO ======================================

# ==========================================================================================================================================|
# ===================================================================Polynomial_Regression================================================|
# ==========================================================================================================================================|


# https://www.youtube.com/watch?v=H8kocPOT5v0
# https://www.youtube.com/watch?v=QptI-vDle8Y
class Polynomial_Regression():

    def __init__(self, _learning_rate=0.01, _iterations=1000):
        pass

    def fit(self, X, y):
        pass

    def predict(self, X):
        pass

# ==========================================================================================================================================|
# ===================================================================Bayesian_Regression================================================|
# ==========================================================================================================================================|


class Bayesian_Regression():

    def __init__(self, _learning_rate=0.01, _iterations=1000):
        pass

    def fit(self, X, y):
        pass

    def predict(self, X):
        pass

# ==========================================================================================================================================|
# ===================================================================Decision_Tree_Regressor================================================|
# ==========================================================================================================================================|


class Node():
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, _variance_reduction=None, *, value=None):

        # for decision node
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.variance_reduction = _variance_reduction

        # for leaf node
        self.value = value

    def _is_leaf_node(self):
        return self.value is not None


class Decision_Tree_Regressor():
    def __init__(self, _min_samples_split=2, _max_depth=100, _n_rand_features=None):

        # tree root
        self.root = None

        # stopping conditions
        self.min_samples_split = _min_samples_split
        self.max_depth = _max_depth
        self.n_rand_features = _n_rand_features

    def _grow_tree(self, dataset, current_depth=0):

        # current node data
        X, y = dataset[:, :-1], dataset[:, -1]
        n_samples, n_features = X.shape
        n_labels = len(np.unique(y))

        # if stopping conditions are met
        if n_samples < self.min_samples_split or current_depth >= self.max_depth or n_labels == 1:
            return Node(value=self._leaf_mean_value(y))

        # rundomly select n_rand_features featurs indexes
        random_features_indexes = np.random.choice(n_features, self.n_rand_features, replace=False)  # noqa

        best_split = self._get_best_split(dataset, random_features_indexes)  # noqa

        if best_split["variance_reduction"] > 0:

            left_subtree = self._grow_tree(best_split["dataset_left"], current_depth+1)  # noqa
            right_subtree = self._grow_tree(best_split["dataset_right"], current_depth+1)  # noqa

            return Node(best_split["feature_index"], best_split["threshold"], left_subtree, right_subtree, best_split["info_gain"])  # noqa

    def _get_best_split(self, dataset, random_features_indexes):

        # dictionary to store the best split

        best_split = {}
        max_variance_reduction = -float("inf")

        # loop over all the features
        for feature_index in random_features_indexes:

            possible_thresholds = np.unique(dataset[:, feature_index])

            for threshold in possible_thresholds:

                dataset_left, dataset_right = self._split(dataset, feature_index, threshold)  # noqa

                if len(dataset_left) > 0 and len(dataset_right) > 0:

                    parent_labels, left_child_labels, right_child_labels = dataset[:, -1], dataset_left[:, -1], dataset_right[:, -1]  # noqa
                    curr_variance_reduction = self._variance_reduction(parent_labels, left_child_labels, right_child_labels, "entropy")  # noqa

                    if curr_variance_reduction > max_variance_reduction:

                        best_split["feature_index"] = feature_index
                        best_split["threshold"] = threshold
                        best_split["dataset_left"] = dataset_left
                        best_split["dataset_right"] = dataset_right
                        best_split["variance_reduction"] = curr_variance_reduction
                        max_variance_reduction = curr_variance_reduction

        return best_split

    def _variance_reduction(self, parent_labels, left_child_labels, right_child_labels):

        weight_l = len(left_child_labels) / len(parent_labels)
        weight_r = len(right_child_labels) / len(parent_labels)
        reduction = np.var(parent_labels) - (weight_l * np.var(left_child_labels) + weight_r * np.var(right_child_labels))  # noqa

        return reduction

    def _split(self, dataset, feature_index, threshold):

        dataset_left = np.array(
            [row for row in dataset if row[feature_index] <= threshold])  # noqa
        dataset_right = np.array(
            [row for row in dataset if row[feature_index] > threshold])  # noqa

        return dataset_left, dataset_right

    def _leaf_mean_value(self, y):
        return np.mean(y)

    def print_tree(self, tree=None, indent=" "):

        if not tree:
            tree = self.root

        if tree.value is not None:
            print(tree.value)

        else:
            print("X_"+str(tree.feature_index), "<=",
                  tree.threshold, "?", tree.info_gain)
            print("%sleft:" % (indent), end="")
            self.print_tree(tree.left, indent + indent)
            print("%sright:" % (indent), end="")
            self.print_tree(tree.right, indent + indent)

    def fit(self, X, Y):
        self.n_rand_features = X.shape[1] if not self.n_rand_features else min(X.shape[1], self.n_rand_features)  # noqa

        dataset = np.concatenate((X, Y), axis=1)
        self.root = self._grow_tree(dataset)

    def predict(self, X):

        return np.array([self._make_prediction(x, self.root) for x in X])

    def _make_prediction(self, x, node):

        if node._is_leaf_node():
            return node.value

        feature_value = x[node.feature_index]
        if feature_value <= node.threshold:
            return self._make_prediction(x, node.left)
        return self._make_prediction(x, node.right)
