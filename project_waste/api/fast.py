from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import model_from_json
import numpy as np
import io

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing) to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Can be restricted to specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define class labels
class_labels = [
    'aerosol_cans', 'aluminum_food_cans', 'aluminum_soda_cans', 'cardboard_boxes',
    'cardboard_packaging', 'clothing', 'coffee_grounds', 'disposable_plastic_cutlery',
    'eggshells', 'food_waste', 'glass_beverage_bottles', 'glass_cosmetic_containers',
    'glass_food_jars', 'magazines', 'newspaper', 'office_paper', 'paper_cups',
    'plastic_cup_lids', 'plastic_detergent_bottles', 'plastic_food_containers',
    'plastic_shopping_bags', 'plastic_soda_bottles', 'plastic_straws', 'plastic_trash_bags',
    'plastic_water_bottles', 'shoes', 'steel_food_cans', 'styrofoam_cups',
    'styrofoam_food_containers', 'tea_bags'
]

# Define categories mapping
category_mapping = {
    'Plastic': [
        'plastic_water_bottles', 'plastic_soda_bottles', 'plastic_detergent_bottles',
        'plastic_shopping_bags', 'plastic_trash_bags', 'plastic_food_containers',
        'disposable_plastic_cutlery', 'plastic_straws', 'plastic_cup_lids'
    ],
    'Paper and Cardboard': [
        'newspaper', 'office_paper', 'magazines', 'cardboard_boxes', 'cardboard_packaging'
    ],
    'Glass': [
        'glass_beverage_bottles', 'glass_food_jars', 'glass_cosmetic_containers'
    ],
    'Metal': [
        'aluminum_soda_cans', 'aluminum_food_cans', 'steel_food_cans', 'aerosol_cans'
    ],
    'Organic Waste': [
        'food_waste', 'eggshells', 'coffee_grounds', 'tea_bags'
    ],
    'Textiles': [
        'clothing', 'shoes'
    ]
}

# Reverse mapping to find category by class label
label_to_category = {label: category for category, labels in category_mapping.items() for label in labels}

# Load JSON model architecture
with open("./model/model.json", "r") as json_file:
    loaded_model_json = json_file.read()
loaded_model = model_from_json(loaded_model_json)

# Load weights into new model
loaded_model.load_weights("./model/model.h5")

print("Model loaded")

# Function to preprocess image
def preprocess_image(img):
    img = img.convert('RGB')  # Ensure image is RGB (some images may be grayscale)
    img = img.resize((128, 128))  # Resize image to match model's expected sizing
    img_array = image.img_to_array(img)  # Convert image to numpy array
    img_array = img_array / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Expand dimensions to match batch size
    return img_array

@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    # Read image file
    contents = await file.read()
    image_stream = io.BytesIO(contents)

    # Load image using Keras image module
    img = image.load_img(image_stream, target_size=(128, 128))  # Adjust target size as per your model's input

    # Preprocess image
    img_array = preprocess_image(img)

    # Make prediction
    predictions = loaded_model.predict(img_array)

    # Get predicted class index
    predicted_class_index = int(np.argmax(predictions, axis=1)[0])  # Assuming batch size 1
    predicted_class_name = class_labels[predicted_class_index]

    # Find the category for the predicted class
    predicted_category = label_to_category.get(predicted_class_name, "Unknown")

    return {
        "predicted_class_index": predicted_class_index,
        "prediction_probabilities": predictions.flatten().astype(float).tolist(),
        "class_name": predicted_class_name,
        "category": predicted_category  # Return the category of the predicted class
    }

@app.get("/")
def root():
    return {
        "message": "Welcome to the Waste Classifier API"
    }
