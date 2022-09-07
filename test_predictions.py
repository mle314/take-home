"""
An example script to test predictions of a deployed model.
"""
import requests


def main():
    url = "http://localhost/predict-post"
    data = {"param1": "M", "param2": "white", "param3": 72}

    resp = requests.post(url, json=data)
    print(resp.json())


if __name__ == "__main__":
    main()
