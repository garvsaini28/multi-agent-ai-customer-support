import pandas as pd


def generate_label_mapping():

    dataset_path = "banking77/train.csv"

    df = pd.read_csv(dataset_path)

    label_mapping = (
        df.groupby("label_gt")["text"]
        .first()
        .sort_index()
    )

    print("\nBANKING77 LABEL MAPPING\n")
    print("=" * 80)

    for label, example in label_mapping.items():

        print(
            f"Label {label}: {example}"
        )


if __name__ == "__main__":

    generate_label_mapping()