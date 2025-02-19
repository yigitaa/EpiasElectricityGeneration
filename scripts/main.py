# main.py
from auth import get_tgt
from fetch_data import fetch_real_time_generation

def main():
    # EPIAS account id pw
    USERNAME = "********"
    PASSWORD = "********"

    # tgt fetch
    tgt = get_tgt(USERNAME, PASSWORD)

    if tgt:
        start_date = "2023-01-01T00:00:00+03:00"
        end_date = "2024-01-01T00:00:00+03:00"

        # data fetch
        df = fetch_real_time_generation(tgt, start_date, end_date)

        # console
        if not df.empty:
            print("\nFetched Data Head:")
            print(df.head())
            print("\nFetched Data Tail:")
            print(df.tail())
            print(f"Total records: {len(df)}")

            # save file
            df.to_csv("../data/real_time_generation.csv", index=False)
            print("Data saved to ../data/real_time_generation.csv")
        else:
            print("No data fetched.")
    else:
        print("Failed to fetch TGT.")

if __name__ == "__main__":
    main()