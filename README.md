This is the waste classifier backend api.

In the Waste_Classifier_Main.ipynb you can see the model that was trained on the https://www.kaggle.com/datasets/alistairking/recyclable-and-household-waste-classification Recyclable and Household Waste Classification Dataset in order to classify 30 different types of materials in the household for waste with an accuracy of ~76%. Trying out different approaches, adding dropout, data augmentation and weight decay in different combinations with different parameters resulted in the best result using dropout rate of 20% with a simple data augmentation resulted in accuracy of 75.7% compared to a chance level of 3.125%.

The best model was then saved as a model (h5, json and keras in model folder) and deployed into a Dockerfile (mainly based on the fast.py in the project_waste/api folder).

This is then connected with an interface from Streamlit which is in a different repo:
https://github.com/jonasge1992/Waste_Classifier_Streamlit_App

The final app can be tested here: https://wasteclassifier.streamlit.app/
