import asyncio
import websockets
import json
import pandas as pd
import os
from datetime import datetime

SOCKET_URL = "wss://ws.coincap.io/prices?assets=bitcoin,ethereum,tether,binance-coin,solana,usd-coin"
CSV_FILE = 'stock_data.csv'
BATCH_SIZE = 10
MAX_RETRIES = 5

# Write a batch of data to the CSV file
def write_to_csv(data_batch):
    try:
        df = pd.DataFrame(data_batch)
        df.to_csv(CSV_FILE, mode='a', index=False, header=not os.path.exists(CSV_FILE))
    except Exception as e:
        print(f"Error writing to CSV: {e}")

# Handles the WebSocket connection and data processing
async def fetch_data():
    retry_attempts = 0
    data_batch = []

    while retry_attempts < MAX_RETRIES:
        try:
            async with websockets.connect(SOCKET_URL) as websocket:
                retry_attempts = 0  # Reset retry counter after successful connection
                print("Connected to WebSocket")

                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    timestamp = datetime.now().isoformat()
                    
                    for symbol, price in data.items():
                        data_batch.append({"symbol": symbol, "price": price, "timestamp": timestamp})
                    
                    # Write to CSV if batch size is met
                    if len(data_batch) >= BATCH_SIZE:
                        write_to_csv(data_batch)
                        data_batch.clear()  # Clear the batch

        except (websockets.ConnectionClosedError, asyncio.TimeoutError) as e:
            retry_attempts += 1
            delay = min(2 ** retry_attempts, 30)  # Exponential backoff up to 30 seconds
            print(f"Connection error: {e}. Reconnecting in {delay} seconds...")
            await asyncio.sleep(delay)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

    if retry_attempts == MAX_RETRIES:
        print("Max retries reached. Exiting.")

# Initializes the CSV file if it does not exist
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w') as f:
            f.write("symbol,price,timestamp\n")  # Header for the CSV file

# Main function to start the WebSocket connection
async def main():
    initialize_csv()
    await fetch_data()

# Run the WebSocket connection
if __name__ == "__main__":
    asyncio.run(main())
