from flask import Flask, render_template, request, Response
import requests
import matplotlib
from datetime import datetime, time as dt_time
import time
matplotlib.use('Agg')  # Use 'Agg' backend for non-interactive plotting
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import datetime
import yfinance as yf

app = Flask(__name__)

# Define the cookies and headers
cookies = {
    'PHPSESSID': 'du7u85s8imhpka97hdvn789onh',
    '_ga': 'GA1.1.2100889719.1706939697',
    '_ga_LB470LF5SH': 'GS1.1.1725029890.344.1.1725029905.0.0.0',
}
##NIFTY-25100C-19SEP24:NIFTY-24900P-19SEP24:NIFTY-25000C-26SEP24:NIFTY-25000P-26SEP24
##NIFTY-25500C-26SEP24:NIFTY-25000C-26SEP24:NIFTY-25000P-26SEP24:NIFTY-24500P-26SEP24
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}


user = 'saravanan46'
sid = 'du7u85s8imhpka97hdvn789onh'

def fetch_data(url):
    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

def parse_data(data):
    rows = data.splitlines()
    dates = []
    values = []
    for row in rows:
        parts = row.split(',')
        if len(parts) > 1:
            try:
                date_time = pd.to_datetime(parts[0], format='%d.%m.%y %H:%M:%S')
                value = float(parts[1])
                dates.append(date_time)
                values.append(value)
            except ValueError as e:
                print(f"Data parsing error: {e}")
    rowss = pd.DataFrame({'DateTime': dates, 'Value': values})
    return rowss

def parse_data_cal(data):
    rows = data.splitlines()
    dates = []
    values = []

    for row in rows:
        parts = row.split(',')
        if len(parts) > 1:
            try:
                date_time = pd.to_datetime(parts[0], format='%d.%m.%y %H:%M:%S')
                value = float(parts[1])
                dates.append(date_time)
                values.append(value)
            except ValueError as e:
                print(f"Data parsing error: {e}")

    return pd.DataFrame({'DateTime': dates, 'Value': values})

def parse_data_if(data):
    rows = data.splitlines()
    dates = []
    values = []

    for row in rows:
        parts = row.split(',')
        if len(parts) > 1:
            try:
                date_time = pd.to_datetime(parts[0], format='%d.%m.%y %H:%M:%S')
                value = float(parts[-1])
                dates.append(date_time)
                values.append(value)
            except ValueError as e:
                print(f"Data parsing error: {e}")

    return pd.DataFrame({'DateTime': dates, 'Value': values})

def downsample_data(df, freq):
    df_downsampled = df.resample(freq, on='DateTime').last().dropna().reset_index()
    return df_downsampled

def plot_data(df_merged, symbol_nf, symbol_sx, start_date, end_date):
    fig, ax1 = plt.subplots(figsize=(16, 8))
    
    if not df_merged.empty:
        # Plot NIFTY data on the primary y-axis
        ax1.plot(df_merged['DateTime'], df_merged['Value_NF'], label=f'{symbol_nf}', color='blue', linewidth=2, marker='o')
        ax1.plot(df_merged['DateTime'], df_merged['Value_SX'], label=f'{symbol_sx}', color='red', linewidth=2, marker='o')
        ax1.plot(df_merged['DateTime'], df_merged['Difference'], label='Difference', color='green', linewidth=2, linestyle='--')

        # Annotate each point with its value
        for i, row in df_merged.iterrows():
            ax1.text(row['DateTime'], row['Value_NF'], f'{row["Value_NF"]:.2f}', color='blue', fontsize=8, ha='right', va='bottom')
            ax1.text(row['DateTime'], row['Value_SX'], f'{row["Value_SX"]:.2f}', color='red', fontsize=8, ha='right', va='bottom')
            ax1.text(row['DateTime'], row['Difference'], f'{row["Difference"]:.2f}', color='green', fontsize=8, ha='right', va='bottom')

        # Highlight sections where Difference is increasing
        highlight = df_merged['Difference_Increasing']
        plt.fill_between(df_merged['DateTime'], df_merged['Value_NF'].min(), df_merged['Value_NF'].max(),
                        where=highlight,
                        color='green', alpha=0.3, label='Increasing Difference Highlight')
        
        ax1.set_xlabel('DateTime')
        ax1.set_ylabel('Value')
        ax1.set_title(f'{symbol_nf} and {symbol_sx} with Difference for {start_date} to {end_date}')
        ax1.legend(loc='upper left')
        ax1.grid(True)
        ax1.tick_params(axis='x', rotation=45)

        # Create a secondary y-axis for FUTURE
        ax2 = ax1.twinx()
        ax2.plot(df_merged['DateTime'], df_merged['Value_FUTURE'], label='FUTURE', color='black', linewidth=2, marker='o')
        
        # Annotate each point for FUTURE
        for i, row in df_merged.iterrows():
            ax2.text(row['DateTime'], row['Value_FUTURE'], f'{row["Value_FUTURE"]:.2f}', color='black', fontsize=8, ha='right', va='bottom')

        ax2.set_ylabel('FUTURE Value', color='black')
        ax2.tick_params(axis='y', labelcolor='black')
        
        # Combine legends from both y-axes
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc=(0.5, 0.5), fontsize='small', frameon=True)

        plt.tight_layout()
    else:
        print("DataFrame is empty. No data to plot.")
    
    # Save plot to BytesIO object and return it
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img

def plot_data_cal_if(df_merged, symbol_nf, symbol_sx, start_date, end_date):
    fig, ax1 = plt.subplots(figsize=(16, 8))
    
    if not df_merged.empty:
        # Plot NIFTY data on the primary y-axis
        ax1.plot(df_merged['DateTime'], df_merged['Value_CAL'], label=f'{symbol_nf}', color='blue', linewidth=2, marker='o')
        ax1.plot(df_merged['DateTime'], df_merged['Value_IF'], label=f'{symbol_sx}', color='red', linewidth=2, marker='o')
        ax1.plot(df_merged['DateTime'], df_merged['Difference'], label='Profit and Loss', color='green', linewidth=2, linestyle='--')

        # Annotate each point with its value
        for i, row in df_merged.iterrows():
            ax1.text(row['DateTime'], row['Value_CAL'], f'{row["Value_CAL"]:.2f}', color='blue', fontsize=8, ha='right', va='bottom')
            ax1.text(row['DateTime'], row['Value_IF'], f'{row["Value_IF"]:.2f}', color='red', fontsize=8, ha='right', va='bottom')
            ax1.text(row['DateTime'], row['Difference'], f'{row["Difference"]:.2f}', color='green', fontsize=8, ha='right', va='bottom')

        ax1.set_xlabel('DateTime')
        ax1.set_ylabel('Value')
        ax1.set_title(f'{symbol_nf} and {symbol_sx} with Difference for {start_date} to {end_date}')
        ax1.legend(loc='upper left')
        ax1.grid(True)
        ax1.tick_params(axis='x', rotation=45)

        # Create a secondary y-axis for FUTURE
        ax2 = ax1.twinx()
        ax2.plot(df_merged['DateTime'], df_merged['Value_FUTURE'], label='FUTURE', color='black', linewidth=2, marker='o')
        
        # Annotate each point for FUTURE
        for i, row in df_merged.iterrows():
            ax2.text(row['DateTime'], row['Value_FUTURE'], f'{row["Value_FUTURE"]:.2f}', color='black', fontsize=8, ha='right', va='bottom')

        ax2.set_ylabel('FUTURE Value', color='black')
        ax2.tick_params(axis='y', labelcolor='black')
        
        # Combine legends from both y-axes
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc=(0.5, 0.5), fontsize='small', frameon=True)

        plt.tight_layout()
    else:
        print("DataFrame is empty. No data to plot.")
    
    # Save plot to BytesIO object and return it
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img

def plot_data_doublcal(df_merged, symbol_nf, start_date, end_date):
    fig, ax1 = plt.subplots(figsize=(16, 8))
    
    if not df_merged.empty:
        # Plot NIFTY data on the primary y-axis
        ax1.plot(df_merged['DateTime'], df_merged['Value_CAL'], label=f'{symbol_nf}', color='blue', linewidth=2, marker='o')
        # Annotate each point with its value
        for i, row in df_merged.iterrows():
            ax1.text(row['DateTime'], row['Value_CAL'], f'{row["Value_CAL"]:.2f}', color='blue', fontsize=8, ha='right', va='bottom')

        ax1.set_xlabel('DateTime')
        ax1.set_ylabel('Value')
        ax1.set_title(f'{symbol_nf}  for {start_date} to {end_date}')
        ax1.legend(loc='upper left')
        ax1.grid(True)
        ax1.tick_params(axis='x', rotation=45)

        # Create a secondary y-axis for FUTURE
        ax2 = ax1.twinx()
        ax2.plot(df_merged['DateTime'], df_merged['Value_FUTURE'], label='FUTURE', color='black', linewidth=2, marker='o')
        
        # Annotate each point for FUTURE
        for i, row in df_merged.iterrows():
            ax2.text(row['DateTime'], row['Value_FUTURE'], f'{row["Value_FUTURE"]:.2f}', color='black', fontsize=8, ha='right', va='bottom')

        ax2.set_ylabel('FUTURE Value', color='black')
        ax2.tick_params(axis='y', labelcolor='black')
        
        # Combine legends from both y-axes
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc=(0.5, 0.5), fontsize='small', frameon=True)

        plt.tight_layout()
    else:
        print("DataFrame is empty. No data to plot.")
    
    # Save plot to BytesIO object and return it
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol_nf = request.form.get('symbol_nf')
        symbol_sx = request.form.get('symbol_sx')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        resample_freq = request.form.get('resample_freq', '15T')  # Default to '15T' if not provided

        # Check if start_date is today
        today = datetime.now().date()
        is_today = datetime.strptime(start_date, '%Y-%m-%d').date() == today

        # Check current time
        current_time = datetime.now().time()
        is_in_time_range = dt_time(9, 15) <= current_time <= dt_time(23, 55)

        # Construct URLs with conditional latestData parameter
        if is_today and is_in_time_range:
            nifty_url = f"https://www.icharts.in/opt/hcharts/stx8req/php/getdataForStraddleChartsATMFP_v6.php?mode=INTRA&symbol={symbol_nf}&timeframe=1min&rdDataType=latest&u={user}&sid={sid}&latestData=1"
            sensex_url = f"https://www.icharts.in/opt/hcharts/stx8req/php/getdataForStraddleChartsATMFP_v6.php?mode=INTRA&symbol={symbol_sx}&timeframe=1min&rdDataType=latest&u={user}&sid={sid}&latestData=1"
        else:
            nifty_url = f"https://www.icharts.in/opt/hcharts/stx8req/php/getdataForStraddleChartsATMFP_v6.php?mode=INTRA&symbol={symbol_nf}&timeframe=1min&rdDataType=latest&u={user}&sid={sid}"
            sensex_url = f"https://www.icharts.in/opt/hcharts/stx8req/php/getdataForStraddleChartsATMFP_v6.php?mode=INTRA&symbol={symbol_sx}&timeframe=1min&rdDataType=latest&u={user}&sid={sid}"
        print(nifty_url)
        print(sensex_url)
        data_nf = fetch_data(nifty_url)
        data_sx = fetch_data(sensex_url)
        print(get_symbol_url(symbol_nf, symbol_sx))
        data_future = fetch_data(get_symbol_url(symbol_nf, symbol_sx))
        if data_nf and data_sx and data_future:
            df_nf = parse_data(data_nf)
            df_sx = parse_data(data_sx)
            df_future = parse_data(data_future)
            df_nf_downsampled = downsample_data(df_nf, resample_freq)
            df_sx_downsampled = downsample_data(df_sx, resample_freq)
            df_future_downsampled = downsample_data(df_future, resample_freq)
            # Merge the data on 'DateTime' column
            df_merged = pd.merge(df_nf_downsampled, df_sx_downsampled, on='DateTime', suffixes=('_NF', '_SX'))
            pd.set_option('display.max_rows', None)  # Display all rows
            pd.set_option('display.max_columns', None)  # Display all columns
            df_merged = pd.merge(df_merged, df_future_downsampled, on='DateTime')
            df_merged.rename(columns={'Value': 'Value_FUTURE'}, inplace=True)
            df_merged = df_merged[(df_merged['DateTime'] >= start_date) & (df_merged['DateTime'] <= end_date)]
            df_merged['Difference'] = df_merged['Value_NF'] - df_merged['Value_SX']
            # Calculate the increase in Difference
            #df_merged['Difference_Increasing'] = df_merged['Difference'].diff().fillna(0) > 0 & (df_merged['Difference'] > 20)
            df_merged['Difference_Increasing'] = df_merged.index.map(lambda idx: check_difference_increase(idx, df_merged))
            img = plot_data(df_merged, symbol_nf, symbol_sx, start_date, end_date)
    
    return Response(img, mimetype='image/png')

def check_difference_increase(row_index, df):
                current_diff = df.loc[row_index, 'Difference']
                previous_diffs = df.loc[:row_index, 'Difference']
                return any(current_diff - prev_diff > 10 for prev_diff in previous_diffs)

@app.route('/cal', methods=['GET', 'POST'])
def index_cal():
    if request.method == 'POST':
        symbols1 = request.form.get('symbols1')
        q1_1 = request.form.get('q1_1')
        q2_1 = request.form.get('q2_1')
        q3_1 = request.form.get('q3_1')
        q4_1 = request.form.get('q4_1')
        start_date1 = request.form.get('start_date1')
        end_date1 = request.form.get('end_date1')
        resample_freq1 = request.form.get('resample_freq1', '15T')

        ##second input
        symbols2 = request.form.get('symbols2')
        q1_2 = request.form.get('q1_2')
        q2_2 = request.form.get('q2_2')
        q3_2 = request.form.get('q3_2')
        q4_2 = request.form.get('q4_2')
        start_date2 = request.form.get('start_date2')
        end_date2 = request.form.get('end_date2')
        resample_freq2 = request.form.get('resample_freq2', '15T')  # Default to '15T' if not provided

        # Construct the URL
        base_url = 'https://www.icharts.in/opt/hcharts/stx8req/php/getdataForDoubleCalendar_beta.php'
        mode = 'INTRA'
        
        # Assuming you need to format symbols, timeframe, and other parameters
        timeframe = '1min'
        
        # Build the complete URL
        url_cal = (f"{base_url}?mode={mode}&symbol={symbols1}&timeframe={timeframe}&u={user}&sid={sid}"
               f"&q1={q1_1}&q2={q2_1}&q3={q3_1}&q4={q4_1}")
        url_if = (f"{base_url}?mode={mode}&symbol={symbols2}&timeframe={timeframe}&u={user}&sid={sid}"
               f"&q1={q1_2}&q2={q2_2}&q3={q3_2}&q4={q4_2}")
        data_cal = fetch_data(url_cal)
        data_if = fetch_data(url_if)
        data_future = fetch_data(get_symbol_url(symbols1,symbols2))
        if data_cal and data_if and data_future:
            df_cal = parse_data_cal(data_cal)
            df_cal_downsampled = downsample_data(df_cal, resample_freq1)
            df_if = parse_data_if(data_if)
            df_if_downsampled = downsample_data(df_if, resample_freq2)
            df_future = parse_data(data_future)
            df_future_downsampled = downsample_data(df_future, resample_freq2)
            df_merged = pd.merge(df_cal_downsampled, df_if_downsampled, on='DateTime', suffixes=('_CAL', '_IF'))
            df_merged = df_merged[(df_merged['DateTime'] >= start_date1) & (df_merged['DateTime'] <= end_date1)]
            df_merged['Difference'] = df_merged['Value_CAL'] + df_merged['Value_IF']
            df_merged = pd.merge(df_merged, df_future_downsampled, on='DateTime')
            df_merged.rename(columns={'Value': 'Value_FUTURE'}, inplace=True)
            img = plot_data_cal_if(df_merged, symbols1, symbols2, start_date1, end_date1)

    return Response(img, mimetype='image/png')


@app.route('/ironfly', methods=['GET', 'POST'])
def index_ironfly():
    if request.method == 'POST':
        ##second input
        symbols2 = request.form.get('symbols2')
        q1_2 = request.form.get('q1_2')
        q2_2 = request.form.get('q2_2')
        q3_2 = request.form.get('q3_2')
        q4_2 = request.form.get('q4_2')
        start_date2 = request.form.get('start_date2')
        end_date2 = request.form.get('end_date2')
        resample_freq2 = request.form.get('resample_freq2', '15T')  # Default to '15T' if not provided

        # Construct the URL
        base_url = 'https://www.icharts.in/opt/hcharts/stx8req/php/getdataForDoubleCalendar_beta.php'
        mode = 'INTRA'
        
        # Assuming you need to format symbols, timeframe, and other parameters
        timeframe = '1min'
        
        # Build the complete URL
        url_if = (f"{base_url}?mode={mode}&symbol={symbols2}&timeframe={timeframe}&u={user}&sid={sid}"
               f"&q1={q1_2}&q2={q2_2}&q3={q3_2}&q4={q4_2}")
        data_cal = fetch_data(url_if)
        print(url_if)
        data_future = fetch_data(get_symbol_url(symbols2, symbols2))
        if data_cal and data_future:
            df_cal = parse_data_cal(data_cal)
            df_cal_downsampled = downsample_data(df_cal, resample_freq2)
            df_future = parse_data(data_future)
            df_future_downsampled = downsample_data(df_future, resample_freq2)
            df_merged = pd.merge(df_cal_downsampled, df_future_downsampled, on='DateTime', suffixes=('_CAL', '_FUTURE'))
            df_merged = df_merged[(df_merged['DateTime'] >= start_date2) & (df_merged['DateTime'] <= end_date2)]
            df_merged.rename(columns={'Value': 'Value_FUTURE'}, inplace=True)
            img = plot_data_doublcal(df_merged, symbols2, start_date2, end_date2)

    return Response(img, mimetype='image/png')

@app.route('/doubleCal', methods=['GET', 'POST'])
def index_doubleCal():
    if request.method == 'POST':
        symbols1 = request.form.get('symbols1')
        q1_1 = request.form.get('q1_1')
        q2_1 = request.form.get('q2_1')
        q3_1 = request.form.get('q3_1')
        q4_1 = request.form.get('q4_1')
        start_date1 = request.form.get('start_date1')
        end_date1 = request.form.get('end_date1')
        resample_freq1 = request.form.get('resample_freq1', '15T')

        # Construct the URL
        base_url = 'https://www.icharts.in/opt/hcharts/stx8req/php/getdataForDoubleCalendar_beta.php'
        mode = 'INTRA'
        
        # Assuming you need to format symbols, timeframe, and other parameters
        timeframe = '1min'
        
        # Build the complete URL
        url_cal = (f"{base_url}?mode={mode}&symbol={symbols1}&timeframe={timeframe}&u={user}&sid={sid}"
               f"&q1={q1_1}&q2={q2_1}&q3={q3_1}&q4={q4_1}")
        data_cal = fetch_data(url_cal)
        data_future = fetch_data(get_symbol_url(symbols1, symbols1))
        if data_cal and data_future:
            df_cal = parse_data_cal(data_cal)
            df_cal_downsampled = downsample_data(df_cal, resample_freq1)
            df_future = parse_data(data_future)
            df_future_downsampled = downsample_data(df_future, resample_freq1)
            df_merged = pd.merge(df_cal_downsampled, df_future_downsampled, on='DateTime', suffixes=('_CAL', '_FUTURE'))
            df_merged = df_merged[(df_merged['DateTime'] >= start_date1) & (df_merged['DateTime'] <= end_date1)]
            df_merged.rename(columns={'Value': 'Value_FUTURE'}, inplace=True)
            img = plot_data_doublcal(df_merged, symbols1, start_date1, end_date1)

    return Response(img, mimetype='image/png')

@app.route('/spreadchart', methods=['GET', 'POST'])
def index_spreadchart():
    if request.method == 'POST':
        symbols2 = request.form.get('symbols2')
        q1_2 = request.form.get('q1_2')
        q2_2 = request.form.get('q2_2')
        start_date2 = request.form.get('start_date2')
        end_date2 = request.form.get('end_date2')
        resample_freq2 = request.form.get('resample_freq2', '15T')  # Default to '15T' if not provided

        # Construct the URL
        base_url = 'https://www.icharts.in/opt/hcharts/stx8req/php/getdataForSpreadQty_m_curr.php'
        mode = 'INTRA'
        # Assuming you need to format symbols, timeframe, and other parameters
        timeframe = '1min'
        # Build the complete URL
        url_spread = (f"{base_url}?mode={mode}&symbol={symbols2}&timeframe={timeframe}&u={user}&sid={sid}"
               f"&q1={q1_2}&q2={q2_2}")
        data_cal = fetch_data(url_spread)
        data_future = fetch_data(get_symbol_url(symbols2, symbols2))
        if data_cal and data_future:
            df_cal = parse_data_cal(data_cal)
            df_cal_downsampled = downsample_data(df_cal, resample_freq2)
            df_future = parse_data(data_future)
            df_future_downsampled = downsample_data(df_future, resample_freq2)
            df_merged = pd.merge(df_cal_downsampled, df_future_downsampled, on='DateTime', suffixes=('_CAL', '_FUTURE'))
            df_merged = df_merged[(df_merged['DateTime'] >= start_date2) & (df_merged['DateTime'] <= end_date2)]
            df_merged.rename(columns={'Value': 'Value_FUTURE'}, inplace=True)
            img = plot_data_doublcal(df_merged, symbols2, start_date2, end_date2)

    return Response(img, mimetype='image/png')

@app.route('/trend', methods=['GET', 'POST'])
def trend():
    # Define the symbols for DOW Futures, NASDAQ Futures, VIX, NSEBANK, and NSEI
    symbols = {
            'DOW Futures': 'YM=F',       # DOW Jones Index
            'NSEBANK': '^NSEBANK',       # Nifty Bank Index
            'NSEI': '^NSEI'              # Nifty 50 Index
    }

    # Fetch data with 1-minute intervals
    data = {}
    for name, symbol in symbols.items():
        df = yf.download(tickers=symbol,period='1d',interval='1m')
        # Normalize the 'Close' column to plot only the patterns
        df['Normalized Close'] = (df['Close'] - df['Close'].min()) / (df['Close'].max() - df['Close'].min())
        data[name] = df

    colors = {
            'DOW Futures': '#008080',      # Bright Orange
            'NASDAQ Futures': '#FF7F50',   # Bright Green
            'NSEBANK': '#000000',          # Bright Pink
            'NSEI': '#FF7F50',             # Bright Yellow
    }

    # Create a plot
    plt.figure(figsize=(14, 7))

    for name, df in data.items():
        plt.plot(df.index, df['Normalized Close'], label=name, color=colors.get(name, '#000000'))

    plt.title('Live Data for DOW Futures, BANKNIFTY, and NIFTY (Normalized Patterns)')
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.legend()
    plt.grid(True)
    plt.show()
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return Response(img, mimetype='image/png')

from datetime import datetime, timedelta

def last_weekday_of_month(year, month, weekday):
    # Calculate the last day of the month
    last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # Find the weekday of the last day
    last_day_weekday = last_day.weekday()
    
    # Calculate the difference from the target weekday
    diff = (last_day_weekday - weekday + 7) % 7
    
    # Calculate the date of the last target weekday
    last_weekday = last_day - timedelta(days=diff)
    
    return last_weekday

def get_last_weekday_date(symbol):
    today = datetime.today()
    year = today.year
    month = today.month
    if 'BANKNIFTY' in symbol:
        # 2 = Wednesday
        last_weekday = last_weekday_of_month(year, month, 2)
    elif 'NIFTY' in symbol:
        # 3 = Thursday
        last_weekday = last_weekday_of_month(year, month, 3)
    else:
        return None
    
    return last_weekday


from datetime import datetime, timedelta
import calendar

# Helper function to get the last weekday of a month
def get_last_weekday(year, month, weekday):
    # Get the number of days in the month
    last_day_of_month = calendar.monthrange(year, month)[1]
    last_date = datetime(year, month, last_day_of_month)
    
    # Go backwards to find the last specified weekday
    while last_date.weekday() != weekday:
        last_date -= timedelta(days=1)
    
    return last_date

# Function to extract month and year in MONYY format from symbol and get the last weekday
def get_last_weekday_date(symbol):
    # Extract the month and year from the symbol
    try:
        mon_yy = symbol[-5:]  # Extract last 5 characters for the format MONYY (e.g., JUN24)
        month_str = mon_yy[:3]  # e.g., 'JUN'
        year_str = mon_yy[3:]   # e.g., '24'
        month = datetime.strptime(month_str, "%b").month  # Convert month name to number
        year = 2000 + int(year_str)  # Convert year to 4 digits
    except ValueError:
        return None

    # Determine the last weekday based on the symbol type
    if 'BANKNIFTY' in symbol:
        # 2 = Wednesday
        last_weekday = get_last_weekday(year, month, 2)
    elif 'NIFTY' in symbol:
        # 3 = Thursday
        last_weekday = get_last_weekday(year, month, 3)
    else:
        return None
    
    return last_weekday

# Function to process symbols and get the last weekday for each
def process_symbols(symbols):
    # Split the symbols by ':'
    symbol_list = symbols.split(':')
    
    for symbol in symbol_list:
        last_weekday = get_last_weekday_date(symbol)
        if last_weekday:
            # Format the date to uppercase '26JUN2024'
            formatted_date = last_weekday.strftime('%d%b%y').upper()
            return formatted_date
        else:
            print(f"{symbol}: Could not extract date.")


def get_symbol_url(symbol_nf, symbol_sx):
    print(symbol_nf)
    symbol_date = process_symbols(symbol_nf)
    print(symbol_date)
    if symbol_date is None:
        symbol_date = process_symbols(symbol_sx)
    if symbol_date is None:
        last_weekday_date = get_last_weekday_date(symbol_nf)
        if last_weekday_date is None:
            last_weekday_date = get_last_weekday_date(symbol_sx)
        symbol_date = last_weekday_date.strftime('%d%b%y').upper()
    if 'BANKNIFTY' in symbol_nf:
        symbol_val = 'BANKNIFTY'
    elif 'NIFTY' in symbol_nf:
        symbol_val = 'NIFTY'
    elif 'BANKNIFTY' in symbol_sx:
        symbol_val = 'BANKNIFTY'
    elif 'NIFTY' in symbol_sx:
        symbol_val = 'NIFTY'
    return f"https://www.icharts.in/opt/hcharts/stx8req/php/getdataForPremium_m_cmpt_curr_tj.php?mode=INTRA&symbol={symbol_val}-{symbol_date}&timeframe=1min&u={user}&sid={sid}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
