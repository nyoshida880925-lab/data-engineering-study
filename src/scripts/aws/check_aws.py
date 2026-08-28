import boto3

def main() -> None:
    sts = boto3.client("sts")
    identity = sts.get_caller_identity()

    print(f"Account: {identity['Account']}")
    print(f"User ID: {identity['UserId']}")
    print(f"ARN: {identity['Arn']}")

if __name__ == "__main__":
    main()