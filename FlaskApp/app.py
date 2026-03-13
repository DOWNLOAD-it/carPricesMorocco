from flask import Flask
from Controllers.Home_Controller import home_bp
from Controllers.Predict_Controller import predict_bp

app = Flask(__name__)
app.register_blueprint(home_bp)
app.register_blueprint(predict_bp)

if __name__ == "__main__":
    app.run(debug=True)
