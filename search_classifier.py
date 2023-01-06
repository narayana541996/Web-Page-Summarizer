# import sys
# sys.path.insert(0,r'C:\assignments\cs733-nlp\web-page-summarizer')

from classifier_tools import *

from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.tree import DecisionTreeClassifier

dic = {'search' : {'dataset_path' : r'search\search_dataset.csv', 'x' : ['has_search_attribute', 'has_search_text', 'has_text_input', 'has_button'], 'y' : 'search_class'},
'filter' : {'dataset_path' : r'filter\filter_dataset.csv', 'x' : ['has_filter_attribute', 'has_filter_text', 'has_checkbox_input', 'has_radio_input'], 'y' : 'filter_class'}}

for key in dic.keys():
    print(key,'---------------------')
    train_x, test_x, train_y, test_y = prep_dataset(dic[key]['dataset_path'], dic[key]['x'],  dic[key]['y'])

    for cls in [LogisticRegression, DecisionTreeClassifier, Perceptron]:
        print('classifier: ',repr(cls))
        model, predictions, score = build_classifier(train_x, test_x, train_y, test_y, cls)
        print('predictions: ',predictions)
        print('score: ',score)
