from label_studio_sdk import LabelStudio ,Client
import sys
import json
from collections import defaultdict
import pandas as pd
import os


def read_json_index(filename="manual_label.json"):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        manual_result = []
        
        for key, value in data['index'].items():
            manual_result.append([key,value])

        return manual_result
            
    except FileNotFoundError:
        print(f"File {filename} not found!")
    except json.JSONDecodeError:
        print(f"Invalid JSON in file {filename}")

    return None

def compare_with(manual_result):
    categorys = ["Type Error","Missing Features","Test Fault","Tooling / Configuration Issue", "Performance Issue", "UI Behavior Bug", "API Misuse", "Missing Cases", "Logic Error", "Asynchrony / Event Handling Bug", "Runtime Exception", "Exception Handling"]

    for index, category in manual_result:
        if category not in categorys:
            print(f'Index: {index} not find the category: {category}')
    print("Finished checking")

def create_prediction_excels(correct_predicts, false_predicts, correct_file='correct_predictions.xlsx', false_file='false_predictions.xlsx'):

    correct_predicts_sorted = sorted(correct_predicts, key=lambda x: x[1])
    false_predicts_sorted = sorted(false_predicts, key=lambda x: x[1])
    
    correct_data = {
        'index': [item[0] for item in correct_predicts_sorted],
        'category': [item[1] for item in correct_predicts_sorted]
    }
    df_correct = pd.DataFrame(correct_data)
    
    false_data = {
        'index': [item[0] for item in false_predicts_sorted],
        'category': [item[1] for item in false_predicts_sorted],
        'predict result': [item[2] for item in false_predicts_sorted]
    }
    df_false = pd.DataFrame(false_data)
    
    df_correct.to_excel(correct_file, index=False)
    df_false.to_excel(false_file, index=False)
    
    print(f"Created {correct_file} with {len(correct_predicts_sorted)} correct predictions")
    print(f"Created {false_file} with {len(false_predicts_sorted)} false predictions")
    
    return df_correct, df_false

def compare_result(manual_result):
    with open('bug_predictions_analysis_textModel.json', 'r') as file:
            data = json.load(file)

    total_record = [0] * 12
    correct_record = [0] * 12
    categorize_index = {"UI Behavior Bug": 0, "Logic Error": 1, "Type Error": 2, "Missing Features": 3,
    "Test Fault":4, "Tooling / Configuration Issue": 5, "Asynchrony / Event Handling Bug": 6, "Missing Cases": 7,
    "API Misuse":8, "Runtime Exception":9, "Performance Issue":10, "Exception Handling": 11}

    correct_predicts = []
    false_predicts = []
    for category_name, category_data in data['categories'].items():
        index_array = category_data['indices']
        for index in index_array:
            for item in manual_result:
                if item[0] == index:
                    if item[1] != "Not Bug":
                        print(f"Category: {item[1]}")
                        total_record[categorize_index[item[1]]] += 1

                    if item[1] == category_name:
                        correct_record[categorize_index[item[1]]] += 1
                        correct_predicts.append([item[0], category_name])
                    else:
                        false_predicts.append([item[0],item[1],category_name])
                    break
    
    category_data = defaultdict(lambda: {"Correctness": ""})
    print("Correctness \n")
    for category in categorize_index:
        category_data[category]["Correctness"] = f"{correct_record[categorize_index[category]]} / {total_record[categorize_index[category]]}"
        print(f"{category}: {correct_record[categorize_index[category]]} / {total_record[categorize_index[category]]}")
    print("~~~~~~~~~~~~~")

    with open("Correctness_file.json", 'w') as f:
        json.dump(dict(category_data), f, indent=2)
    
    create_prediction_excels(correct_predicts,false_predicts)




if __name__ == "__main__":

    manual_result = read_json_index()
    if manual_result:
        compare_result(manual_result)
    else:
        print("Error happen ")