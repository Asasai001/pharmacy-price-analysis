from analysis.price_analysis import (price_range_sum)
from analysis.discount_analysis import total_number_distribution
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def total_number():
    df = price_range_sum()

    pivot_total = df.pivot(index='Category', columns='Pharmacy', values='Total Number Of Items')
    pivot_total.plot(kind='bar', figsize=(12, 8))
    plt.title('Total Items per Category by Pharmacy')
    plt.xticks(rotation=10)
    plt.savefig('total_number.png')
    plt.show()

def pharmacy_market_share():
    df = total_number_distribution()

    label = df['Pharmacy']
    size = df['Total Number of Items']
    total = size.sum()

    legend_label = [f'{ph}({pct:.1f}%) - {cnt:,}'
                    for ph, cnt, pct in zip(label, size, size/total*100)]

    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(size, autopct='%1.1f%%', startangle=90)
    plt.legend(wedges, legend_label, title="Number of Items - 12,990", loc="upper left", bbox_to_anchor=(1, 0.8))
    plt.title('Pharmacy Market Share')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('pharmacy_market_share.png')
    plt.show()


