# Import libraries
import os
import csv
import pandas as pd
from flask import Flask, render_template, url_for
from flask import request, redirect
from werkzeug.utils import secure_filename
from PIL import Image


# Creat Flask app
app = Flask(__name__)


# Route for displaying recipes
@app.route('/recipes')
def recipes():
    # Read CSV file using Pandas
    df = pd.read_csv('recipes.csv')

    # Convert DataFrame to a dictionary so that it can be passed to the template
    recipes = df.to_dict(orient='records')

    # Render the 'recipes.html' template and pass the recipes data to it
    return render_template('recipes.html', recipes=recipes)


# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')


# Route for adding a new recipe
@app.route('/add-recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        recipe_name = request.form['name']
        image = request.files['image']
        ingredients = request.form['ingredients']
        preparation = request.form['preparation']
        serving = request.form['serving']

        # Validate recipe name
        if not recipe_name or len(recipe_name) > 100:
            return "Invalid recipe name, go back and try again!", 400

        # Validate ingredients
        if not ingredients or len(ingredients) > 500:
            return "Invalid ingredients, go back and try again!", 400

        # Validate preparation instructions
        if not preparation or len(preparation) > 500:
            return "Invalid preparation instructions, go back and try again!", 400

        # Validate serving instructions
        if not serving or len(serving) > 100:
            return "Invalid serving instructions, go back and try again!", 400

        # Validate image file
        image_filename = secure_filename(image.filename)
        image_path = os.path.join('static', image_filename)
        image.save(image_path)

        # Check if the file is an image using Pillow
        try:
            with Image.open(image_path) as img:
                img.verify()  # Verifies that the file is an image
        except Exception:
            os.remove(image_path)  # Remove the file if it's not an image
            return "Invalid image file, go back and try again!", 400  # Return an error response

        # Append the new recipe to the CSV file
        with open('recipes.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([recipe_name, image.filename, ingredients, preparation, serving])

        return redirect(url_for('recipes'))
    return render_template('add-recipe.html')


# Route for removing a recipe
@app.route('/remove-recipe', methods=['GET', 'POST'])
def remove_recipe():
    if request.method == 'POST':
        remove_name = request.form['remove']
        df = pd.read_csv('recipes.csv')
        df = df[df['Recipe Name'] != remove_name]
        df.to_csv('recipes.csv', index=False)
        return redirect(url_for('recipes'))
    else:
        df = pd.read_csv('recipes.csv')
        recipes = df.to_dict(orient='records')
        return render_template('remove-recipe.html', recipes=recipes)


# Route for searching recipes
@app.route('/search', methods=['GET'])
def search_recipes():
    search_query = request.args.get('search', '')

    df = pd.read_csv('recipes.csv')

    if search_query:
        # Filter recipes based on the search query
        df = df[df.apply(lambda row: search_query.lower() in (str(row['Recipe Name']).lower() + str(row['Ingredients']).lower()), axis=1)]

    # Convert DataFrame to a dictionary so that it can be passed to the template
    recipes = df.to_dict(orient='records')

    return render_template('search.html', recipes=recipes)


# Start the Flask app with debugging enabled
if __name__ == '__main__':
    app.run(debug=True)
