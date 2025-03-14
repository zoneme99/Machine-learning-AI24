from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression



class model_selection:
    def __init__(self, X, y, autoscale=True, autosplit=True):
        self.X = X
        self.y = y
        if autoscale == True:
            self.standard_normal_scaling()
        if autosplit == True:
            self.train_test_split()

    def standard_normal_scaling(self):
        S_scaler = StandardScaler()
        self.X = S_scaler.fit_transform(self.X)
        N_scaler = Normalizer()
        self.X = N_scaler.fit_transform(self.X)



    def train_test_split(self, test_size=0.33, random_state=None):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=test_size, random_state=random_state)
    
    def GridCV_pipeline_fit(self, param_grid):
        self.run = True # Variabel för att kunna köra predict method
        self.pipeline = Pipeline([
        ('classifier', LogisticRegression()) #Place Holder
        ])

        # Kör GridSearchCV
        self.grid_search = GridSearchCV(self.pipeline, param_grid, cv=5, scoring='accuracy', verbose=5)
        self.grid_search.fit(self.X_train, self.y_train)

        # Visa bästa modellen och dess hyperparametrar
        print("Bästa modellen:", self.grid_search.best_estimator_)
        print("Bästa score:", self.grid_search.best_score_)
    
    def predict_score(self):
        if self.run == False:
            raise ValueError('GridCV_pipeline_fit method must be executed first')
        self.y_hat = self.grid_search.predict(self.X_test)




    



