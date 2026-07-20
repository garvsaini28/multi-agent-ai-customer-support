import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score


class IntentClassifier:

    def __init__(self):

        self.model = Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        lowercase=True,
                        ngram_range=(1, 2),
                        max_features=20000
                    )
                ),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=1000
                    )
                )
            ]
        )

        self.is_trained = False

    def train(self):

        dataset_path = "banking77/train.csv"

        df = pd.read_csv(dataset_path)

        X = df["text"]
        y = df["label_gt"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        self.model.fit(
            X_train,
            y_train
        )

        self.is_trained = True

        predictions = self.model.predict(
            X_test
        )

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        print(
            f"Intent Classifier Accuracy: {accuracy:.2%}"
        )

    def predict(
        self,
        message: str
    ):

        if not self.is_trained:

            self.train()

        prediction = self.model.predict(
            [message]
        )

        probability = self.model.predict_proba(
            [message]
        )

        confidence = max(
            probability[0]
        )

        return {
            "intent": int(prediction[0]),
            "confidence": float(confidence)
        }


intent_classifier = IntentClassifier()