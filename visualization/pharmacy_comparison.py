from analysis.price_analysis import (price_range_sum, )
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def total_number():
    df = price_range_sum()

    pivot_total = df.pivot(index='Category', columns='Pharmacy', values='Total Number Of Items')
    pivot_total.plot(kind='bar', figsize=(12, 8))
    plt.title('Total Items per Category by Pharmacy')
    plt.xticks(rotation=10)
    plt.show()

