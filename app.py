from flask import Flask, render_template, request
from joblib import load

app = Flask(__name__)

# Load model
model = load(r"C:\Users\Marcu\PycharmProjects\CP4477Project\mpg_linear_regression_model.joblib")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Extracting input data from the form
        cylinders = request.form.get('cylinders', type=int)
        horsepower = request.form.get('horsepower', type=int)
        weight = request.form.get('weight', type=int)
        age = request.form.get('age', type=int)
        origin_japan = request.form.get('origin_japan', type=int)
        origin_usa = request.form.get('origin_usa', type=int)

        # Prepare the input data for the model
        input_data = [[cylinders, horsepower, weight, age, origin_japan, origin_usa]]

        # Make prediction
        prediction = model.predict(input_data)[0]

        # Return the result
        return f"The predicted MPG is: {prediction}"

    return render_template('predict.html')


if __name__ == '__main__':
    app.run(debug=True)


