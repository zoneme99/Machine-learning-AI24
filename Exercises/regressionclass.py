import numpy as np
import scipy.stats as stats
import pandas as pd

class LinearRegression:
    def __init__(self, matrix, yvariable, confedence_level = 0.05):
        if isinstance(matrix, pd.DataFrame):
            (n, d) = matrix.shape
            self._n = n
            self._d = d
            self._conf_level = confedence_level
            self._matrix = matrix
            self._Y = yvariable
            self._X = matrix
            self._X.insert(0, "bias", np.ones(self._X.shape[0])) if 'bias' not in self._X.columns else None
            self._B = np.linalg.pinv(self._X.T @ self._X) @ self._X.T @ self._Y
        else:
            raise TypeError("Needs to be a Dataframe")

    @property
    def n(self):
        return self._n
    
    @property
    def d(self):
        return self._d
    
    @property
    def conf_level(self):
        return self._conf_level
    
    @property
    def matrix(self):
        return self._matrix
    
    @property
    def Y(self):
        return self._Y
    
    @property
    def X(self):
        return self._X
    
    @property
    def B(self):
        return self._B
    
    @property
    def SSE(self):
        return np.sum(np.square(self.Y.to_numpy() - self.X.to_numpy() @ self.B.to_numpy()))
    
    @property
    def MSE(self):
        return self.SSE/self.n
    
    @property
    def RMSE(self):
        return np.sqrt(self.MSE)

    @property
    def MAE(self):
        return np.sum(np.absolute(self.Y.to_numpy() - self.X.to_numpy() @ self.B.to_numpy()))/self.n
    
    
    @property
    def var(self):
        return self.SSE/(self.n-self.d-1)
    
    @property
    def std(self):
        return np.sqrt(self.var)
    
    @property
    def Syy(self):
        return (self.n*np.sum(np.square(self.Y.to_numpy())) - np.square(np.sum(self.Y.to_numpy())))/self.n
    
    @property
    def SSR(self):
        return self.Syy-self.SSE
    
    @property
    def R2(self):
        return self.SSR / self.Syy
    
    @property
    def F_test(self):
        f = stats.f(self.d, self.n-self.d-1)
        f_stat = (self.SSR/self.d)/self.var
        return f.sf(f_stat)
    

    @property
    def covar_matrix(self):
        return (np.linalg.pinv(self.X.to_numpy()[:,1:].T @ self.X.to_numpy()[:,1:]))*self.var
    
    #Double sided T-test
    def T_test(self, feature):
        cindex = self.X.columns.get_loc(feature)
        Bhat = self.B.to_numpy()[cindex]
        C = self.covar_matrix[cindex-1,cindex-1] #cindex not reset to 0
        T_stat = Bhat/(self.std*np.sqrt(C))
        t_object = stats.t(self.n-self.d-1)
        p_value = 2*min(t_object.cdf(T_stat), t_object.sf(T_stat))
        return p_value
    
    @property
    def T_test_all(self):
        features = self.X.columns
        print(self.X.columns)
        output = list()
        for feature in features:
            output.append(f"{feature} p-value : {self.T_test(feature)}\n")
        return ''.join(output)
    
    #Compare all features with eachother
    @property
    def Pearson_pairs(self):
        output = list()
        features = self._X.drop("bias", axis=1).columns
        for x in range(len(features)):
            for y in range(x,len(features)):
                if features[x] == features[y]:
                    continue
                output.append(f"{features[x]}/{features[y]} : {stats.pearsonr(self._X[features[x]], self._X[features[y]])}\n")
        return  ''.join(output)
    
    @property
    def conf_interval_features(self):
        output = list()
        features = list(self.X.columns)
        features.remove('bias')
        t_object = stats.t(self.n-self.d-1)

        for index in range(len(features)):
            t_point = t_object.ppf(self.conf_level/2)*self.var*np.sqrt(self.covar_matrix[index][index])
            output.append(f"{features[index]} : {self.B[index+1]} +/- {t_point}\n") #not consider bias therefore +1
        return ''.join(output)
