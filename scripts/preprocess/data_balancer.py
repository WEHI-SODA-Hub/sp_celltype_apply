
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import TomekLinks, EditedNearestNeighbours, RandomUnderSampler
from imblearn.combine import SMOTEENN, SMOTETomek
import pandas as pd

class DataBalancer:

    def __init__(self, random_state : int =42) -> None:
        self.random_state = random_state
        self.title = "Data Balancer"
        self.valid_scheme = {
                            "SMOTE" : SMOTE(random_state=self.random_state),
                            "SMOTEENN" : SMOTEENN(random_state=self.random_state),
                            "ADASYN" : ADASYN(random_state=self.random_state),
                            "TOMEK" : TomekLinks(), 
                            "SMOTETOMEK" : SMOTETomek(), 
                            "ENN" :  EditedNearestNeighbours(),
                            "RUS" : RandomUnderSampler()
                            }


    def balance_data(self, X : pd.DataFrame, y : pd.DataFrame, balance_scheme : str):
        """
        Apply the correct balancing
        """
        if not balance_scheme in self.valid_scheme:
            print("{}: Valid scheme for data balancing not found. Returning original X.".format(self.title))
            return X, y
        balancer = self.valid_scheme[balance_scheme]
        return balancer.fit_resample(X, y)
        
            

