import os

import bs4 as bs

import pandas as pd

import re

def fetch_html(path):
    ''' Fetches html file from given path.'''
    for entry in os.scandir(path):
        if entry.is_dir():
            # print('entry: ',entry.name)
            for entry2 in os.scandir(entry):
                if entry2.is_file():
                    if entry2.path.endswith('.html'):
                        # print('entry2: ',entry2.path)
                        yield entry2.path

def launch_make_dataset(features, make_dataset, raw_data_path = r'Insupport-dataset', dataset_path = None):
    ''' Launches make_dataset function in dataset_maker. '''
    pd.DataFrame(columns= features).to_csv(dataset_path, mode= 'w', encoding= 'ISO-8859-1')
    for url in fetch_html(raw_data_path):
      # print('url: ',url)
      with open(url, encoding='ISO-8859-1') as page:
        html = bs.BeautifulSoup(page, features = 'html5lib')
      if dataset_path:
        make_dataset(html, features, dataset_path)
      else:
        make_dataset(html, features)

def search_attributes_with_children(element, search_value, feature, feature_dict):
    ''' Searches for the search_value in attributes of element and its children and updates the feature in feature_dict.
    returns the updated feature_dict '''
    feature_dict[feature].append(0)
    for value in element.attrs.values():
      if isinstance(value, str):
        if search_value in value.lower():
          feature_dict[feature][-1] += 1
      elif isinstance(value, list):
        for item in value:
          if search_value in item.lower():
            feature_dict[feature][-1] += 1

    for child in element.findChildren():
      for child_value in child.attrs.values():
        if isinstance(child_value, str):
          if search_value in child_value.lower():
            feature_dict[feature][-1] += 1
        elif isinstance(child_value, list):
          for item in child_value:
            if search_value in item.lower():
              feature_dict[feature][-1] += 1
    return feature_dict

def search_text_with_children(element, search_value, feature, feature_dict):
    ''' Searches for the search_value in text of element and its children and updates the feature in feature_dict.
      returns the updated feature_dict '''
    feature_dict[feature].append(0)
    if search_value in element.text.lower():
        feature_dict[feature][-1] += 1
    for child in element.findChildren():
        if search_value in child.text.lower():
            feature_dict[feature][-1] += 1
    return feature_dict

def find_input_type_number(element, type, feature, feature_dict):
    ''' Find number of child inputs of given type for the element and updates the feature in feature_dict.
    returns the updated feature_dict'''
    feature_dict[feature].append(0)
    for inp in element.findAll('input', {'type' : type}):
        feature_dict[feature][-1] += 1
    return feature_dict

def find_child_number(element, child, feature, feature_dict):
    ''' Find number of 'child' elements in element's children and updates feature_dict.
    returns the updated feature_dict.  '''
    feature_dict[feature].append(0)
    for button in element.findAll(child):
        feature_dict[feature][-1] += 1
    return feature_dict

def find_button_number(element, feature, feature_dict):
    ''' Find number of child buttons for the element and updates the feature in feature_dict.
    returns the updated feature_dict. '''
    # feature_dict[feature].append(0)
    # for button in element.findAll('button'):
    #     feature_dict[feature][-1] += 1
    feature_dict = find_child_number(element, 'button', feature, feature_dict)
    for inp in element.findAll('input',{'type' : ['button', 'submit']}):
        # print('type: ',inp.attrs['type'])
        feature_dict[feature][-1] += 1
    return feature_dict

def find_class(element, feature, feature_dict):
    ''' Finds the class(target for the classifier) of the element with data-attribute and updates the feature in feature_dict.
    returns the updated feature_dict. '''
    feature_dict[feature].append(0)
    # print('class: ',re.findall(r'^\S+_', feature)[0].strip('_'))
    if 'data-attribute' in element.attrs.keys():
      if element.attrs['data-attribute'].lower().strip() == re.findall(r'^\S+_', feature)[0].strip('_'):
        feature_dict[feature][-1] = 1
        return feature_dict
    # else:
    #   for child in element.findChildren():
    #     if 'data-attribute' in child.attrs.keys():
    #       if child.attrs['data-attribute'].lower().strip() == re.findall(r'^\S+_', feature)[0].strip('_'):
    #         feature_dict[feature][-1] = 1
    #         return feature_dict
      
      # for parent in element.findParents():
      #   if 'data-attribute' in parent.attrs.keys():
      #     if parent.attrs['data-attribute'].lower().strip() == re.findall(r'^\S+_', feature)[0].strip('_'):
      #       feature_dict[feature][-1] = 1
      #       return feature_dict
    return feature_dict

def search_previous_label(element, search_value, feature, feature_dict):
    ''' Checks if previous label is sort and updates the feature_dict.
    returns the updated feature_dict. '''
    feature_dict[feature].append(0)
    label = element.find_previous_sibling('label')
    if label:
        if label.text.strip().lower() == search_value:
          feature_dict[feature][-1] = 1
          return feature_dict
    return feature_dict

def write_dataset(feature_dict, log_list, dataset_path, log_path):
  data=pd.DataFrame(feature_dict)
  data.to_csv(dataset_path, mode= 'a', encoding= 'ISO-8859-1', header= False)
  with open(log_path, mode = 'w', encoding= 'ISO-8859-1') as f:
    for item in log_list:
      f.write(f'{log_list.index(item)}) {item}\n')

def func_map(feature, element, feature_dict):

    ''' Maps the functions with the feature and implements approppriate function. '''
    search_value = re.findall('_+\S+_', feature)
    if search_value:
      search_value = search_value[0].strip('_')
    if feature.startswith('has_') and feature.endswith('_attribute'):
      return search_attributes_with_children(element = element, search_value= search_value, feature = feature, feature_dict= feature_dict)
    
    elif feature.startswith('has_') and feature.endswith('_text'):
      return search_text_with_children(element = element, search_value= search_value, feature= feature, feature_dict= feature_dict)

    elif feature.startswith('has_') and feature.endswith('_input'):
      return find_input_type_number(element = element, feature= feature, feature_dict= feature_dict)

    elif feature.lower().strip() == 'has_button':
      return find_button_number(element = element, feature= feature, feature_dict= feature_dict)

    elif feature.endswith('_class'):
      return find_class(element = element, feature= feature, feature_dict= feature_dict)

if __name__ == '__main__':
    path = r'C:\assignments\cs733-nlp\web-page-summarizer\Insupport-dataset'
    # fetch_file = fetch_file()
    for f in fetch_html(path):
        print('fetched: ',f)
