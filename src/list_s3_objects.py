import boto3

from config import get_s3_settings

def main() -> None:
    settings = get_s3_settings()
    s3_client = boto3.client(
        "s3",
        region_name=settings["AWS_REGION"]
    )

    response = s3_client.list_objects_v2(
        Bucket=settings["S3_BUCKET"],
        Prefix="raw/"
    )

    if "Contents" in response:
        print("S3オブジェクト一覧:")
        for obj in response["Contents"]:
            print(f"- {obj['Key']}")
    else:
        print("指定されたプレフィックスにオブジェクトは存在しません。")

if __name__ == "__main__":
    main()