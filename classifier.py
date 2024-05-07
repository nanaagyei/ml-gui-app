from taipy.gui import Gui  # Importing Gui from taipy library
from tensorflow.keras import models  # Importing models from tensorflow.keras
from PIL import Image  # Importing Image from PIL library
import numpy as np  # Importing numpy library

class_names = {  # Defining a dictionary to map class indices to class names
    0: "airplane",
    1: "automobile",
    2: "bird",
    3: "cat",
    4: "deer",
    5: "dog",
    6: "frog",
    7: "horse",
    8: "ship",
    9: "truck",
}

# Load the model
model = models.load_model("baseline_mariya.keras")  # Loading the pre-trained model

def predict_image(model, path_to_img):  # Function to predict the class of an image
    img = Image.open(path_to_img)  # Opening the image
    img = img.convert("RGB")  # Converting the image to RGB
    img = img.resize((32, 32))  # Resizing the image to 32x32 pixels
    data = np.asarray(img)  # Converting the image to numpy array
    data = data / 255  # Normalizing the pixel values
    probs = model.predict(np.array([data])[:1])  # Predicting the class probabilities

    top_prob = probs.max()  # Getting the maximum probability
    top_pred = class_names[np.argmax(probs)]  # Getting the class with maximum probability

    return top_prob, top_pred  # Returning the maximum probability and the predicted class

content = ""  # Initializing content variable
img_path = "placeholder_image.png"  # Initializing image path
prob = 0  # Initializing probability variable
pred = ""  # Initializing prediction variable

index = """ 
<|text-center|
<|{"logo.png"}|image|width=25vw|>

<|{content}|file_selector|extensions=.png|>
Select an image from your file system

<|{pred}|>

<|{img_path}|image|>

<|{prob}|indicator|value={prob}|min=0|max=100|width=25vw|>
>
"""


def on_change(state, var_name, var_val):  # Function to handle changes in the GUI
    if var_name == "content":  # If the changed variable is 'content'
        state.img_path = var_val  # Update the image path
        top_prod, top_pred = predict_image(model, var_val)  # Predict the class of the new image
        state.prob = round(top_prod * 100)  # Update the probability
        state.pred = f"This is a {top_pred}!"  # Update the prediction
    # print(var_name, var_val)  # Print the changed variable and its new value


app = Gui(page=index)  # Creating a Gui object with the defined HTML template

if __name__ == "__main__":  # If the script is run directly
    app.run(port=8000, use_reloader=True)  # Run the app on port 8000 with reloader enabled

