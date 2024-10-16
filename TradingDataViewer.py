from datetime import datetime as dt
import threading
import time
import tkinter as tk
from tkinter import ttk
from tradingview_ta import TA_Handler, Interval


class TradingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Trading Data Viewer")
        self.master.geometry("900x800")

        self.create_widgets()

    def create_widgets(self):
        # Input frame
        input_frame = ttk.Frame(self.master, padding="10")
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="Symbol:").grid(row=0, column=0, sticky=tk.W)
        self.symbol_entry = ttk.Entry(input_frame)
        self.symbol_entry.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(input_frame, text="Screener:").grid(row=1, column=0, sticky=tk.W)
        self.screener_entry = ttk.Entry(input_frame)
        self.screener_entry.insert(0, "america")
        self.screener_entry.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(input_frame, text="\t"*2, wraplength=400).grid(row=1, column=2, sticky=tk.W)
        ttk.Label(input_frame, text="Screener Info:").grid(row=1, column=3, sticky=tk.W)
        exchange_info = ("If you're looking for stocks, enter the exchange's country as the screener.\n"
                         "If you're looking for cryptocurrency, enter 'crypto' as the screener.\n"
                         "If you're looking for forex, enter 'forex' as the screener.")
        ttk.Label(input_frame, text=exchange_info, wraplength=400).grid(row=1, column=4, sticky=tk.W)
        
        ttk.Label(input_frame, text="Exchange:").grid(row=2, column=0, sticky=tk.W)
        self.exchange_entry = ttk.Entry(input_frame)
        self.exchange_entry.insert(0, "NASDAQ")
        self.exchange_entry.grid(row=2, column=1, sticky=tk.W)

        self.interval_values = {
             "1 min" : Interval.INTERVAL_1_MINUTE,
             "5 min" : Interval.INTERVAL_5_MINUTES,
             "15 min" : Interval.INTERVAL_15_MINUTES,
             "30 min" : Interval.INTERVAL_30_MINUTES,
             "1 hour" : Interval.INTERVAL_1_HOUR,
             "2 hours" : Interval.INTERVAL_2_HOURS,
             "4 hours" : Interval.INTERVAL_4_HOURS,
             "1 day" : Interval.INTERVAL_1_DAY,
             "1 Week" : Interval.INTERVAL_1_WEEK,
             "1 Month" : Interval.INTERVAL_1_MONTH
        }
        ttk.Label(input_frame, text="Interval:").grid(row=3, column=0, sticky=tk.W)
        self.interval_entry = ttk.Combobox(input_frame, values=list(self.interval_values.keys()))
        self.interval_entry.insert(0, "1 min")
        self.interval_entry.grid(row=3, column=1, sticky=tk.W)

        ttk.Label(input_frame, text="Update Rate (seconds):").grid(row=4, column=0, sticky=tk.W)
        self.update_rate_entry = ttk.Entry(input_frame)
        self.update_rate_entry.grid(row=4, column=1, sticky=tk.W)

        # Indicators frame
        indicators_frame = ttk.LabelFrame(self.master, text="Indicators")
        indicators_frame.pack(fill=tk.Y, expand=True)

        self.indicators = {
            "ADX": ["ADX", "ADX+DI", "ADX+DI[1]", "ADX-DI", "ADX-DI[1]"],
            "AO": ["AO", "AO[1]", "AO[2]"],
            "BB": ["BB.lower", "BB.upper", "BBPower"],
            "CCI": ["CCI20", "CCI20[1]"],
            "EMA": ["EMA5", "EMA10", "EMA20", "EMA30", "EMA50", "EMA100", "EMA200"],
            "MACD": ["MACD.macd", "MACD.signal"],
            "MOM": ["Mom", "Mom[1]"],
            "Pivot.M.Camarilla": ["Pivot.M.Camarilla.Middle", "Pivot.M.Camarilla.R1", "Pivot.M.Camarilla.R2", "Pivot.M.Camarilla.R3", "Pivot.M.Camarilla.S1", "Pivot.M.Camarilla.S2", "Pivot.M.Camarilla.S3"],
            "Pivot.M.Classic": ["Pivot.M.Classic.Middle", "Pivot.M.Classic.R1", "Pivot.M.Classic.R2", "Pivot.M.Classic.R3", "Pivot.M.Classic.S1", "Pivot.M.Classic.S2", "Pivot.M.Classic.S3"],
            "Pivot.M.Demark": ["Pivot.M.Demark.Middle", "Pivot.M.Demark.R1", "Pivot.M.Demark.S1"],
            "Pivot.M.Fibonacci": ["Pivot.M.Fibonacci.Middle", "Pivot.M.Fibonacci.R1", "Pivot.M.Fibonacci.R2", "Pivot.M.Fibonacci.R3", "Pivot.M.Fibonacci.S1", "Pivot.M.Fibonacci.S2", "Pivot.M.Fibonacci.S3"],
            "Pivot.M.Woodie": ["Pivot.M.Woodie.Middle", "Pivot.M.Woodie.R1", "Pivot.M.Woodie.R2", "Pivot.M.Woodie.R3", "Pivot.M.Woodie.S1", "Pivot.M.Woodie.S2", "Pivot.M.Woodie.S3"],

            "RSI": ["RSI", "RSI[1]"],
            "REC": ["Rec.BBPower", "Rec.HullMA9", "Rec.Ichimoku", "Rec.Stoch.RSI", "Rec.UO", "Rec.VWMA", "Rec.WR"],
            "SMA": ["SMA5", "SMA10", "SMA20", "SMA30", "SMA50", "SMA100", "SMA200"],
            "STOCH": ["Stoch.D", "Stoch.D[1]", "Stoch.K", "Stoch.K[1]", "Stoch.RSI.K"],
            "OTHER": ["HullMA9", "Ichimoku.BLine", "P.SAR", "UO", "VWMA", "W.R", "change", "volume"]
        }

        self.indicator_vars = {}
        for indicator_group, indicators in self.indicators.items():
            subgroup = ttk.Checkbutton(indicators_frame, variable=list(indicators))
            subgroup.pack()

            for i, indicator in enumerate(indicators):
                var = tk.BooleanVar()
                ttk.Checkbutton(subgroup, text=indicator, variable=var).grid(row=i//8, column=i%8, sticky=tk.W)
                self.indicator_vars[indicator] = var

        # Output frame
        output_frame = ttk.Frame(self.master)
        output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = tk.Text(output_frame, wrap=tk.WORD, height=5)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Start button
        ttk.Button(self.master, text="Start", command=self.start_fetching).pack(pady=10, padx=5)

    def start_fetching(self):
        symbol = self.symbol_entry.get()
        screener = self.screener_entry.get()
        exchange = self.exchange_entry.get()
        interval = self.interval_values[self.interval_entry.get()]
        update_rate = self.update_rate_entry.get()

        selected_indicators = [ind for ind, var in self.indicator_vars.items() if var.get()]

        if not symbol or not screener or not exchange:
            self.output_text.insert(tk.END, "Please fill in all required fields.\n")
            return

        try:
            update_rate = float(update_rate) if update_rate else None
        except ValueError:
            self.output_text.insert(tk.END, "Invalid update rate. Using default (no update).\n")
            update_rate = None

        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, f"Fetching data for {symbol} on {exchange} in {self.interval_entry.get()} interval ...\n")

        threading.Thread(target=self.fetch_data, args=(symbol, screener, exchange, interval, selected_indicators, update_rate), daemon=True).start()

    def fetch_data(self, symbol, screener, exchange, interval, indicators, update_rate):
        handler = TA_Handler(
            symbol=symbol,
            screener=screener,
            exchange=exchange,
            interval=interval
        )

        while True:
            try:
                analysis = handler.get_analysis()
                self.output_text.delete('1.0', tk.END)
                now = dt.now()
                self.output_text.insert(tk.END, f"{now:%Y/%m/%d  %H:%M:%S} \n")
                self.output_text.insert(tk.END, f"Data for {symbol} on {exchange} in {self.interval_entry.get()} interval:\n")
                self.output_text.insert(tk.END, f"Open: {analysis.indicators['open']}\n")
                self.output_text.insert(tk.END, f"Close: {analysis.indicators['close']}\n")
                self.output_text.insert(tk.END, f"High: {analysis.indicators['high']}\n")
                self.output_text.insert(tk.END, f"Low: {analysis.indicators['low']}\n\n")

                for indicator in indicators:
                    if indicator in analysis.indicators:
                        self.output_text.insert(tk.END, f"{indicator}: {analysis.indicators[indicator]}\n")

                if update_rate is None:
                    break
                time.sleep(update_rate)
            except Exception as e:
                self.output_text.insert(tk.END, f"Error: {str(e)}\n")
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingApp(root)
    root.mainloop()