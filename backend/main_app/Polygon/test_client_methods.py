from PolygonAPIClient import PolygonAPIClient

def main():
    client  : PolygonAPIClient = PolygonAPIClient()

    ret = client.fetch_ticker_details("AAPL")

    if ret:
        for key, val in ret.items():
            print(f"{ret} : {val}")
    
    results = ret["results"]

    print()
    for k in results.keys():
        print(k)


if __name__ == "__main__":
    main()