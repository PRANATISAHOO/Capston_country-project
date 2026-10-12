import pandas as pd
import matplotlib.pyplot as plt


CSV_FILE = "exported_countries.csv"

def create_plot():
    df = pd.read_csv(CSV_FILE)

    df["population"] = pd.to_numeric(df["population"], errors="coerce")
    df["area"] = pd.to_numeric(df["area"], errors="coerce")
    df = df.dropna(subset=["population", "area"])
    plt.figure(figsize=(10, 6))
    plt.scatter(df["population"], df["area"], alpha=0.7)

    plt.title("Country Population vs Area")
    plt.xlabel("Population")
    plt.ylabel("Area(sq. km)")
    plt.grid(True, linestyle="--", alpha = 0.5)
    plt.tight_layout()
    plt.savefig("population_vs_area.png",dpi=300)
    plt.close()

    print("Plot saved as population_vs_area.png")

if __name__ == "__main__":
    create_plot()
