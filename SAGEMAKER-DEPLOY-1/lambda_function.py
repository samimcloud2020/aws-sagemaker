import boto3
import json

# Initialize SageMaker runtime client
sagemaker_runtime = boto3.client("sagemaker-runtime")

def lambda_handler(event, context):
    try:
        # Print the event for debugging
        print("Event:", event)
        
        # Handle event["body"] depending on its type
        if isinstance(event["body"], str):
            body = json.loads(event["body"])  # Parse JSON string to dictionary
        elif isinstance(event["body"], dict):
            body = event["body"]  # Already a dictionary
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid request format"})
            }
        
        # Validate the input
        if "YearsExperience" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'YearsExperience' in request body"})
            }
        
        # Extract the 'YearsExperience' value
        years_experience = body["YearsExperience"]
        
        # Format the input for SageMaker (CSV format)
        payload = f"{years_experience}"
        
        # Invoke the SageMaker endpoint
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName="linear-learner-2025-01-26-15-49-10-686",  # Replace with your endpoint name
            ContentType="text/csv",  # Expected data format for SageMaker
            Body=payload
        )
        
        # Parse the SageMaker response
        result = json.loads(response["Body"].read().decode())
        predicted_salary = result["predictions"][0]["score"]

        # Return the prediction
        return {
            "statusCode": 200,
            "body": json.dumps({
                "YearsExperience": years_experience,
                "PredictedSalary": predicted_salary
            })
        }
    except Exception as e:
        # Handle errors gracefully
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
