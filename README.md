# Automatic-TypeScript-Bug-Classifier

## Table of Contents
1. [Dependecies Installation](#dependecies-install )
2. [Project Structure](#project-structure)
3. [Key Json files and configuration](#key-json-files-and-configuration)
4. [Key Scripts Usage ](#key-scripts-usage )
5. 


## Dependecies Install 
```bash
pip install requests nltk beautifulsoup4 label-studio-sdk setfit pandas
```

## Project Structure
```bash
TSBugsArtifact/
├── raw_data                           # All raw data we collect, include the clearing version data
├── Data_Collection                    # Collect bug-fix relative commit and extract the commit URLs from given repository
├── Model_Train_Predict_Setfit         # Training model on label data and use it to predict labels for untrain commit
├── Verification                       # Produce verification report for model predicted label result        
└── Control_Experiment_Predict_Result  # Collect result of control experiment

```

## Key Json Files and Configuration

### Key Json Files

**Json Files Path:** <realtive_path>/Automatic-TypeScript-Bug-Classifier/Verification   <br>

**Name:** `manual_label.json.json` <br>
**Description:** Verification set with manually label result

**Name:** `training_set_data_org` <br>
**Description:** training sample with 137 manually label result


### Key Configuration of Label studio

To correctly extract data from a Label Studio project, the projects must have the following configurations.

#### Labeling Interface
Label interface of the project has to follow this pattern:
```HTML
<View>
  <Text name="text" value="$commit_index"/>
  <View style="box-shadow: 2px 2px 5px #999;                padding: 20px; margin-top: 2em;                border-radius: 5px;">
    <Header value="Choose bug category"/>
    <Choices name="sentiment" toName="text" choice="single" showInLine="true">
      <Choice value="Test Fault"/>
      <Choice value="Asynchrony / Event Handling Bug"/>
      <Choice value="Tooling / Configuration Issue"/>
      <Choice value="Missing Cases"/>
      <Choice value="Exception Handling"/>
      <Choice value="Missing Features"/>
      <Choice value="Type Error"/>
      <Choice value="UI Behavior Bug"/>
      <Choice value="API Misuse"/>
      <Choice value="Logic Error"/>
      <Choice value="Runtime Exception"/></Choices>
  </View>
</View>
```

#### Automatic Upload Local File (Could Storage)
It’s not required, but it’s **strongly recommended** if you want to upload all local data to your Label Studio project at once.

Start Label Studio with following comment, fill in your root directory: 
```bash
LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=<YOUR_ROOT_DIRECTORY> label-studio
```
Connect local files to your project:
1. In your project Settings, open **Cloud Storage**.
2. Click **Add source storage** and set **Storage type** to Local files
3. Fill in the fields:
    - `Absolute local path`: <realtive_path>/Automatic-TypeScript-Bug-Classifier/raw_data/predict-sample-collection
    - `File Filter Regex`: .*json


## Key Scripts Usage 

### Data_Collection 

**Script:** `github_commits_collector` <br>
**Description:** extract commits relative to bug fix from given GitHub repository and create a json file under **current directory** to store them
**Arguments:**
 - agument 1: URL of Github repository that being targeted 
 - agument 2: Number of commit going to collect
 - agument 3: person access token (classic), optional

```bash
python github_commits_collector.py <GITHUB_REPOSITORY_URL> [<Collect_Commit_Number>] [<YOUR_GITHUB_TOKEN>]
```
<br>

**Script:** `index.py` <br>
**Description:** collect key information from commit/commits that realtive discussion (Github PR, issue and security page) that you given. These data will be store in json file at `/TSBugsArtifact/raw_data/output` directory (If not have such directory, then script will generate) <br>
**Arguments:**
 - agument 1: URL of Github commit that need to collect
 - agument 2: person access token (classic); defualt: None

For single commit:
```bash
python index.py <GITHUB_COMMIT_URL> [<YOUR_GITHUB_TOKEN>]
```

For multiple commits:

```bash
python index.py <JSON_FILE>
```

**Json File Format**

Reference to `collect_commit_template.json`
```Json
{
    "token": "YOUR_GITHUB_TOKEN" OR null,
    "urls": [
      "GITHUB_COMMIT_URL",
      .........
    ]
}
```
<br>

### Model_Train_Predict_Setfit


**Script:** `index.py` <br>
**Prerequisite:** You should have labe studio person access token and a project with a few label sample <br>
**Description:** fine-tun the model with label simples in your label studio project and upload the predict label for un-label simples into same project
**Arguments:**
 - agument 1: Label Studio person access token
 - agument 2: Label Studio project ID 

```bash
python index.py <YOUR_LabelStudio_Access_Token> <PROJECT_ID> 
```
<br>

### Verification

**Script:** `label_studio_extractor.py` <br>
**Prerequisite:** You should have labe studio person access token and a project with a few predict sample <br>
**Description:** get predict label result summarization for then given project
**Arguments:**
 - agument 1: Label Studio person access token
 - agument 2: Label Studio project ID

```bash
python label_studio_extractor.py <YOUR_LabelStudio_Access_Token> <PROJECT_ID> 
```
<br>

**Script:** `compare_manual_predict.py` <br>
**Prerequisite:** You should have a json file that store the summarize of predict label and its name should be `bug_predictions_analysis_textModel.json` (run `label_studio_extractor.py`) <br>
**Description:** Generate one json file and two Excel files: 
  - Correctness_file.json: contain the overall accuracy for each bug category
  - correct_predictions.xlsx: contain samples the model labeled correctly
  - false_predictions.xlsx: contain samples it mislabeled, based on comparsion between the model’s predicted labels and verification set

```bash
python compare_verification_predict.py 
```
