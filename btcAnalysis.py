import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_dir, 'btcAnalysis.csv')

def analyzation(file_path): 
    df = pd.read_csv(file_path, skiprows=1)
    # Convert Date column to proper datetime
    # The Date column format is like "2018-08-22 11-PM", we need to fix it to "2018-08-22 23:00:00"
    df['DateTime'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %I-%p')
    df = df.drop('Date', axis=1)  # Drop the old Date column
    df.set_index('DateTime', inplace=True)
    print(df.head())
    
    # Check market trend (up or down)
    if df['Close'].iloc[-1] > df['Close'].iloc[0]:
        print("Market is going up!")
    else:
        print("Market is going down!")
    
    # Simple investment check: if current close > 7-day moving average, good time to invest
    df['MA7'] = df['Close'].rolling(window=7).mean()
    if df['Close'].iloc[-1] > df['MA7'].iloc[-1]:
        print("Good time to invest (price above moving average)!")
    else:
        print("Not a good time to invest (price below moving average).")
    
    # Graph: Close price over time
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(range(len(df)), df['Close'])
        plt.title('BTC Close Price Over Time')
        plt.xlabel('Time Period')
        plt.ylabel('Close Price')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Could not display graph: {e}")

analyzation(filepath)