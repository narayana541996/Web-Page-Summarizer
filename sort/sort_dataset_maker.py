import sys
sys.path.insert(0,r'C:\assignments\cs733-nlp\web-page-summarizer')

from dataset_tools import *





def make_dataset(html, features, dataset_path = r'sort/sort_dataset.csv'):
  feature_dict = {k: [] for k in features}
  selects = []
  for select in html.findAll('select'):
    selects.append(select)

    # has_sort_attribute
    feature_dict = search_attributes_with_children(select, 'sort', 'has_sort_attribute', feature_dict)

    # has_sort_label
    feature_dict = search_previous_label(select, 'sort', 'has_sort_label', feature_dict)

    # has_option
    feature_dict = find_child_number(select, 'option', 'has_option', feature_dict)
    
    # sort_class
    feature_dict = find_class(select, 'sort_class', feature_dict)
    
 
  # data=pd.DataFrame(feature_dict)
  # data.to_csv(dataset_path, mode= 'a', encoding= 'ISO-8859-1', header= False)
  # with open(r'search/selects.txt', mode = 'w', encoding= 'ISO-8859-1') as f:
  #   for item in selects:
  #     f.write(f'{selects.index(item)}) {item}\n')
  write_dataset(feature_dict, selects, dataset_path, r'sort/selects.txt')

# page = requests.get(url)
if __name__ == '__main__':
  features = ['has_sort_attribute','has_sort_label', 'has_option', 'sort_class']
  launch_make_dataset(features, make_dataset, dataset_path = r'sort/sort_dataset.csv')
