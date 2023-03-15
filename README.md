# diabetes-prediction-webapp

## Project setup

- Prereq: You have anaconda/miniconda installed and set up on your machine

- Create the conda environment from the environment.yml file and activate it. 
```bash
conda env create -f environment.yml
conda activate glucowise
```
Note: You might have to follow different steps to install the environment depending on your OS. But just use the environment.yml file as a reference and install the packages manually if needed.

- Start streamlit
```bash
streamlit run streamlit/main.py
```

## Project structure

- streamlit: Contains the streamlit app - all the frontend code.
- notebooks: Contains the notebooks used for data exploration and model training.
- data: Dump all data files here.
- src: Can add any helper functions and other reusable code here.