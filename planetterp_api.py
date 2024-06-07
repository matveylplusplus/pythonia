import pandas as pd
import requests


def main():
    grade_data = requests.get(
        "https://api.planetterp.com/v1/grades?course=math410"
    )
    x = grade_data.json()
    print(pd.DataFrame.from_dict(x))


if __name__ == "__main__":
    main()
