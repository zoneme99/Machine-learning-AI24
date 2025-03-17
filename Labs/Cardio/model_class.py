from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay



class model_selection:
    def __init__(self, X, y, autoscale=True, autosplit=True):
        self.X = X
        self.y = y
        self.run = False #Låser upp andra funktioner om GridCV_pipeline_fit är exekverad
        if autoscale == True:
            self.standard_normal_scaling()
        if autosplit == True:
            self.train_test_split()

    def standard_normal_scaling(self):
        S_scaler = StandardScaler()
        self.X = S_scaler.fit_transform(self.X)
        N_scaler = MinMaxScaler()
        self.X = N_scaler.fit_transform(self.X)



    def train_test_split(self, test_size=0.33, random_state=None):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=test_size, random_state=random_state)
    
    def GridCV_pipeline_fit(self, param_grid):
        self.run = True # Variabel för att kunna köra predict method
        self.pipeline = Pipeline([
        ('classifier', LogisticRegression()) #Place Holder
        ])

        # Kör GridSearchCV
        self.grid_search = GridSearchCV(self.pipeline, param_grid, cv=5, scoring='accuracy', verbose=1)
        self.grid_search.fit(self.X_train, self.y_train)

        # Visa bästa modellen och dess hyperparametrar
        print("Bästa modellen:", self.grid_search.best_estimator_)
        print("Bästa score:", self.grid_search.best_score_)
    
    def predict_score(self):
        if self.run == False:
            raise ValueError('GridCV_pipeline_fit method must be executed first')
        self.y_hat = self.grid_search.predict(self.X_test)
        self.score = classification_report(self.y_test, self.y_hat)
        self.cm = confusion_matrix(self.y_test, self.y_hat)
        print(self.score)
        ConfusionMatrixDisplay(self.cm).plot()
    
    def get_all_best_params(self):
        #Loopar igenom alla modeller och tar fram de bästa parametrar för respektive modell
        if self.run == False:
            raise ValueError('GridCV_pipeline_fit method must be executed first')
        lst_params = self.grid_search.cv_results_['params']
        lst_scores = self.grid_search.cv_results_['mean_test_score']
        score_index = 0
        output = list()
        active = lst_params[0]
        for index, param in enumerate(lst_params):
            if active['classifier'] != param['classifier']:
                output.append(f"{active}, score: {lst_scores[score_index]}\n")
                active = param
                score_index = index
            else:
                if lst_scores[score_index] < lst_scores[index]:
                    score_index = index
                    active = param
        
        output.append(f"{active}, score: {lst_scores[score_index]}\n")
        return ''.join(output)




    



