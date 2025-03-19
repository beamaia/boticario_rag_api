
import os
from dotenv import load_dotenv

load_dotenv()

class AppConfig:
    def __init__(self):
        self.index_name = os.environ.get(
            "INDEX_NAME", "mvp_cadastra_boticario"
        )

        self.es = {
            "url": os.environ.get("ELASTICSEARCH_URL"),
            "timeout": os.environ.get("ELASTICSEARCH_TIMEOUT", 30),
            "cloud_id": os.environ.get("ELASTICSEARCH_CLOUD_ID"),
            "api_key": os.environ.get("ELASTICSEARCH_API_KEY") 
        }

        self.huggingfacehub = {
            "repo_id": os.environ.get(
                "HUGGINGFACE_REPO_ID", "sentence-transformers/all-MiniLM-L6-v2"
            ),

            "task": os.environ.get("HUGGINGFACE_TASK", "feature-extraction"),
            "huggingfacehub_api_token": os.environ.get("HUGGINGFACE_API_TOKEN"),
        }

        self.aws = {
            "region_name": os.environ.get(
                "AWS_REGION",
                "us-east-2"
            ),
            "aws_access_key_id": os.environ.get("AWS_SECRET_ACCESS_ID"),
            "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        },

        self.s3_aws = {
            "s3_bucket_prefix":  os.environ.get("S3_BUCKET_PREFIX", "rag_backup_files/"),
            "s3_bucket": os.environ.get("S3_BUCKET", "cadastra-boticario-case") 
        }

        self.openai = {
            "key": os.environ.get("OPENAI_API_KEY")
        }

config = AppConfig()