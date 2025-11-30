from label_studio_sdk import LabelStudio ,Client
import sys
import json
from collections import defaultdict

def export_predictions_from_label_studio(ls, project_id, output_file="prediction_analysis.json", url="http://localhost:8080"):
    category_data = defaultdict(lambda: {"count": 0, "indices": []})
    
    total_tasks = 0
    tasks_with_predictions = 0
    tasks_without_predictions = 0
    
    print(f"Extracting predictions from project {project_id}...")
    
    for task in ls.tasks.list(project=project_id):
        total_tasks += 1
        
        # Check if task has predictions
        if task.predictions:
            tasks_with_predictions += 1
            commit_index = task.data.get('commit_index', None)
            
            if commit_index is None:
                print(f"Warning: Task {task.id} has no commit_index in data")
                continue
            
            for prediction in task.predictions:
                if 'result' in prediction and len(prediction['result']) > 0:
                    result = prediction['result'][0]
                    
                    if 'value' in result and 'choices' in result['value']:
                        choices = result['value']['choices']
                        
                        for category in choices:
                            category_data[category]["count"] += 1
                            category_data[category]["indices"].append(commit_index)
        else:
            tasks_without_predictions += 1

    result = {
        "summary": {
            "total_tasks": total_tasks,
            "tasks_with_predictions": tasks_with_predictions,
            "tasks_without_predictions": tasks_without_predictions,
            "total_categories": len(category_data)
        },
        "categories": dict(category_data)
    }
    
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    


if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Not correctly input key")
        sys.exit(1)

    key = sys.argv[1]
    project_id = sys.argv[2]

    ls = LabelStudio(base_url="http://localhost:8080", api_key=key)
    
    export_predictions_from_label_studio(
        ls=ls, 
        project_id=project_id,
        output_file="bug_predictions_analysis_textModel.json"
    )