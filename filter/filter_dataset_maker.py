import sys
sys.path.insert(0,r'C:\assignments\cs733-nlp\web-page-summarizer')

from dataset_tools import *

import pandas as pd

def make_dataset(html, features, dataset_path):
    feature_dict = {k: [] for k in features}

    for form in html.findAll('form'):

        # has_filter_attribute
        feature_dict = search_attributes_with_children(form, 'filter', 'has_filter_attribute', feature_dict)

        # has_filter_text
        feature_dict = search_text_with_children(form, 'filter', 'has_filter_text', feature_dict)

        # has_checkbox_input
        feature_dict = find_input_type_number(form, 'checkbox', 'has_checkbox_input', feature_dict)
        
        # has_radio_input
        feature_dict = find_input_type_number(form, 'radio', 'has_radio_input', feature_dict)

        # filter_class
        feature_dict = find_class(form, 'filter_class', feature_dict)
        
    
    pd.DataFrame(feature_dict).to_csv(dataset_path, mode= 'a', encoding= 'ISO-8859-1', header= False)


if __name__ == '__main__':
    features = ['has_filter_attribute', 'has_filter_text', 'has_checkbox_input', 'has_radio_input', 'filter_class']
    pd.DataFrame(columns= features).to_csv(r'filter/filter_dataset.csv', mode= 'w', encoding= 'ISO-8859-1')
    launch_make_dataset(features, pd.DataFrame, make_dataset, dataset_path= r'filter/filter_dataset.csv')
    