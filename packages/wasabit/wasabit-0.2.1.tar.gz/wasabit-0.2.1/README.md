# Wasabit

This package offers a solution for uploading files, creating folders, and authenticating with Wasabi. It contains scripts to simplify file uploads, folder creation, and authentication to the Wasabi environment. Streamline your Wasabi workflows with this package as a starting point for further customization and development.

## Installation

Use the package manager [pip](https://github.com/bippisb/wasabit.git) to install wasabit.

```bash
pip install wasabit
```

## Usage

```python
from wasabit.wasabi_auth import wasabi_auth
from wasabit.wasabi_upload import upload_to_wasabi

ACCESS_KEY = "YOUR WASABI_ACCESS_KEY"
WASABI_SECRET = "YOUR WASABI_SECRET_KEY"

bucket_name = 'dev-data'
wasabi_path = 'DGCIS_EXPORT_ALL_HS/processed/Final/'
folder_path = "D:/Saurabh/data/processed/Final/"

# 'upload data to wasabi'
upload_to_wasabi(folder_path, bucket_name,wasabi_path,access_key = ACCESS_KEY, secret_key = WASABI_SECRET)

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
