import os


def main() -> None:
    app_name = os.getenv("APP_NAME", "sample-python-app")
    version = os.getenv("APP_VERSION", "dev")
    print(f"{app_name} is running with version {version}")


if __name__ == "__main__":
    main()