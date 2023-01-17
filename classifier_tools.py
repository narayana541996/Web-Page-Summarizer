
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score

def prep_dataset(raw_data_path, x_features : list[str], y_feature : str):
    ''' Prepares dataset to train classifier and returns it as train_x, test_x, train_y, test_y'''
    data = pd.read_csv(raw_data_path)
    train_x, test_x, train_y, test_y = train_test_split(data[x_features], data[y_feature], test_size=0.25)
    print('train x:',train_x)
    print('train y:', train_y)
    return train_x, test_x, train_y, test_y

def build_classifier(train_x, test_x, train_y, test_y, classifier):
    ''' Builds a model with the given classifier and data.
    returns the built model, predictions and score. '''
    model = classifier()
    model.fit(train_x, train_y)
    predictions = model.predict(test_x)
    print('actual target value counts:\n',test_y.value_counts())
    print('prediction value counts:\n',pd.DataFrame(predictions).value_counts())
    # print(list(zip(predictions, test_y)))
    # print('manual accuracy: ',(predictions == test_y).astype(int) / len(test_y) )
    score = model.score(test_x, test_y)
    precision = precision_score(test_y, predictions)
    recall = recall_score(test_y, predictions)
    f1 = f1_score(test_y, predictions)
    return (model, predictions, score, precision, recall, f1)