import boto3

# LocalStack S3 Endpoint
LOCALSTACK_ENDPOINT = "http://localhost:4566"

# AWS Credentials (Dummy values for LocalStack)
AWS_ACCESS_KEY = "test"
AWS_SECRET_KEY = "test"
REGION_NAME = "us-east-1"

# Bucket and File details
BUCKET_NAME = "my-local-bucket"
FILE_NAME = "test_file.txt"
LOCAL_FILE_PATH = "test_file.txt"

# Initialize S3 Client
s3_client = boto3.client(
    "s3",
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    endpoint_url=LOCALSTACK_ENDPOINT,  # Important for LocalStack
)

# Step 1: Create Bucket
def create_bucket():
    try:
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        print(f"✅ Bucket '{BUCKET_NAME}' created successfully!")
    except Exception as e:
        print(f"⚠️ Error creating bucket: {e}")

# Step 2: Upload a File
def upload_file():
    with open(LOCAL_FILE_PATH, "w") as file:
        file.write("Hello from LocalStack!")  # Create a sample file

    s3_client.upload_file(LOCAL_FILE_PATH, BUCKET_NAME, FILE_NAME)
    print(f"✅ File '{FILE_NAME}' uploaded successfully!")

# Step 3: List Files in the Bucket
def list_files():
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    if "Contents" in response:
        print("📂 Files in bucket:")
        for obj in response["Contents"]:
            print(f"  - {obj['Key']}")
    else:
        print("📂 No files found in bucket.")

# Step 4: Download the File
def download_file():
    s3_client.download_file(BUCKET_NAME, FILE_NAME, f"downloaded_{FILE_NAME}")
    print(f"✅ File '{FILE_NAME}' downloaded successfully!")

# Run All Steps
if __name__ == "__main__":
    create_bucket()
    upload_file()
    list_files()
    download_file()
