## Project Documentation

### Project setup (for development)

- Prereq: You have anaconda/miniconda installed and set up on your machine. Follow steps from [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) if you don't have it installed already.

- Create the conda environment from the environment.yml file and activate it. 

```bash
conda env create -f environment.yml
conda activate gluco
```

Note: You might have to follow different steps to install the environment depending on your OS. But just use the environment.yml file as a reference and install the packages manually if needed.

- Go to the root of the project and start the streamlit app

```bash
streamlit run streamlit/main.py
```

### User Manual (for usage)

- Deployment was done with the help of streamlit. The final app can be accessed [here](https://anirudh58-diabetes-prediction-webapp-streamlitmain-35qwoi.streamlit.app/)

- Prediction Screen:
    - The user must first enter some basic health information related to diabetes prediction.
    - Then the user can choose a target feature to compare against the entire population. 
    - The user can also choose from the list of models to see the prediction results from that model. We provide a table containing descriptions of the models used in the app, so that the user can understand the model better before making a choice.
    - Once submitted, the user will see a table of probabilities of the patient having or not having diabetes, corresponding to each chosen model.
    - The user can also see a scatter plot of the entire population for the target feature (where red and blue dots represent diabetic and non-diabetic patients respectively). This can give the patient a good understanding of where they stand against the entire population.
    - Following is a sample screenshot of the prediction screen:

![Prediction Screen](/documentation/prediction_screen.png)

- Insights Screen:
    - The user can choose 2 features to explore simultaneously.
    - The plot on the first row shows the overall distribution of positive and negative labels from the dataset.
    - The plots on the second row show the mean of the selected features between the positive and negative labels. We also add a scatter plot to show the correlation between the 2 features.
    - Following is a sample screenshot of the insights screen:

![Insights Screen](/documentation/insights_screen.png)

### Architecture Diagram

![Architecture Diagram](/documentation/architecture_diagram.png)

