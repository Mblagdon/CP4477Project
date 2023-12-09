from flask import Flask, render_template, request
from joblib import load

app = Flask(__name__)

# Load models
model = load(r"C:\Users\Marcu\PycharmProjects\CP4477Project\models\mpg_linear_regression_model.joblib")
diabetes_model = load(r"C:\Users\Marcu\PycharmProjects\CP4477Project\models\diabetes_model.joblib")


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

        # Format the result
        result = f"The predicted MPG is: {prediction}"
        return render_template('prediction_result.html', result=result)

    return render_template('predict.html')


@app.route('/predict_diabetes', methods=['GET', 'POST'])
def predict_diabetes():
    if request.method == 'POST':
        # Extract data from form, excluding 'Glucose'
        pregnancies = request.form.get('pregnancies', type=int)
        bloodPressure = request.form.get('bloodPressure', type=int)
        skinThickness = request.form.get('skinThickness', type=int)
        insulin = request.form.get('insulin', type=int)
        bmi = request.form.get('bmi', type=float)
        diabetesPedigreeFunction = request.form.get('diabetesPedigreeFunction', type=float)
        age = request.form.get('age', type=int)

        # Prepare input data array
        input_data = [pregnancies, bloodPressure, skinThickness, insulin, bmi, diabetesPedigreeFunction, age]

        # After making a prediction
        prediction = diabetes_model.predict([input_data])[0]
        result = f"The predicted glucose level is: {prediction}"
        return render_template('prediction_result.html', result=result)

    return render_template('diabetes_predict.html')


if __name__ == '__main__':
    app.run(debug=True)


