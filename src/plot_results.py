import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv("results/results.csv")

    print("CSV columns:", list(df.columns))

    memory_means = {
        "Adaptive": df["adaptive_memory_accuracy"].mean(),
        "Window": df["window_memory_accuracy"].mean(),
        "Summary": df["summary_memory_accuracy"].mean()
    }

    query_means = {
        "Adaptive": df["adaptive_query_correct"].mean(),
        "Window": df["window_query_correct"].mean(),
        "Summary": df["summary_query_correct"].mean()
    }

    plt.figure(figsize=(8, 5))
    plt.bar(memory_means.keys(), memory_means.values())
    plt.ylim(0, 1.05)
    plt.title("Memory Accuracy by Method")
    plt.ylabel("Accuracy")
    plt.savefig("results/memory_accuracy.png", bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.bar(query_means.keys(), query_means.values())
    plt.ylim(0, 1.05)
    plt.title("Query Accuracy by Method")
    plt.ylabel("Accuracy")
    plt.savefig("results/query_accuracy.png", bbox_inches="tight")
    plt.close()

    print("Saved plots to results/memory_accuracy.png and results/query_accuracy.png")


if __name__ == "__main__":
    main()