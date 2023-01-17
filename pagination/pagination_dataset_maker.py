import sys
sys.path.insert(0,r'C:\assignments\cs733-nlp\web-page-summarizer')

from dataset_tools import *

def make_dataset(html, features, dataset_path = r'pagination/pagination_dataset.csv', data_attribute = None):
  feature_dict = {k: [] for k in features}
  inner_items = []
#   print('data_attribute: ',data_attribute)
  for item in ['div','section','nav','li','ul','span','button','tr', 'footer','a','pagination','b']:
    for inner_item in html.findAll(item, {'data-attribute' : data_attribute}):
        inner_items.append(inner_item)

        # has_pagination_attribute
        feature_dict = search_attributes_with_children(inner_item, 'pagination', 'has_pagination_attribute', feature_dict)

        #common_url
        feature_dict = find_common_url_number(html, inner_item, 'common_url', feature_dict)

        # has_button
        feature_dict = find_button_number(inner_item, 'has_button', feature_dict)

        # has_a
        feature_dict = find_child_number(inner_item, 'a', 'has_a', feature_dict)
        
        # pagination_class
        # feature_dict = find_class(inner_item, 'pagination_class', feature_dict)
        if data_attribute:
            feature_dict['pagination_class'].append(1)
        else:
            feature_dict['pagination_class'].append(0)
        
    
    # data=pd.DataFrame(feature_dict)
    # data.to_csv(dataset_path, mode= 'a', encoding= 'ISO-8859-1', header= False)
    # with open(r'search/inner_items.txt', mode = 'w', encoding= 'ISO-8859-1') as f:
    #   for inner_item in inner_items:
    #     f.write(f'{inner_items.index(inner_item)}) {inner_item}\n')
  write_dataset(feature_dict, inner_items, dataset_path, r'pagination/inner_items.txt')

# page = requests.get(url)
if __name__ == '__main__':
    
    features = ['has_pagination_attribute', 'common_url','has_button', 'has_a', 'pagination_class']
    launch_make_dataset(features, make_dataset, dataset_path = r'pagination/pagination_dataset.csv', data_attribute = 'page')
    launch_make_dataset(features, make_dataset, dataset_path = r'pagination/pagination_dataset.csv', header_csv_mode= None)
