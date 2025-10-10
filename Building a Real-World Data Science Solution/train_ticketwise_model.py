from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
import os
import boto3
from io import StringIO
from sklearn.model_selection import train_test_split

# ==========================================================
# TRAINING LOGIC
# This part runs when you call estimator.fit()
# ==========================================================
if __name__ == '__main__':
    # Read the training data
    # Download the Ticketwise data from S3
    BUCKET_NAME = 'ticketwise-pipeline'
    # Initialize S3 client 
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key="ticketwise_dataset.csv")
    
    # Read content into pandas DataFrame
    content = response['Body'].read().decode('utf-8')
    df = pd.read_csv(StringIO(content))
   
    # Features and label for model training
    features = ["attachments", "previous_interactions", "contract_value", 
                "account_age_months", "open_tickets"]
    label = "is_urgent"
    
    X = df[features]
    y = df[label]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                        test_size=0.2, random_state=42)

    # Training the model to classify tickets as urgent or not
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Save the model to the required model directory
    joblib.dump(model, os.path.join('/opt/ml/model', 'model.joblib'))


# ==========================================================
# HOSTING LOGIC (Functions needed for deployment)
# This part is used when you call estimator.deploy()
# ==========================================================

def model_fn(model_dir):
    """
    When you deploy, SageMaker calls this to load your model.
    model_dir is '/opt/ml/model'.
    """
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

def predict_fn(input_data, model):
    """
    SageMaker calls this to make a prediction.
    'input_data' is the data from your request, and 'model' is the
    model loaded by model_fn.
    """
    return model.predict(input_data)
























    