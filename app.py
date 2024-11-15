from flask import Flask, render_template

# Initialize the app
app = Flask(__name__)

# Define a route for the homepage
@app.route('/')
def home():
    return "Hello, this is my website!"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)