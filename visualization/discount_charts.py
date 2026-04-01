import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from analysis.discount_analysis import (discount_model_pharmacy, direct_percent,
                                        bulk_min_qty, buy_x_get_y)


def discount_distribution():
    df = discount_model_pharmacy()

    pivot = df.pivot(index='Discount Model', columns='Pharmacy', values='Total Number of Items')
    pivot.plot(kind='bar', figsize=(12, 8))
    plt.title('Discount Models in Pharmacies')
    plt.xticks(rotation=10, fontsize=8, ha='right')
    plt.show()

def direct_discount():
    df = direct_percent()

    pivot = df.pivot(index='Pharmacy Name', columns='Item Category', values='Final Price With Discount')
    pivot.plot(kind='bar', figsize=(12, 9))
    plt.title('Direct Discount Models Distribution in Pharmacies')
    plt.xticks(rotation=10, fontsize=10, ha='right')
    plt.show()

def bulk_min_qty_discount():
    df = bulk_min_qty()

    pivot = df.pivot(index='Pharmacy Name', columns='Item Category', values='Final Price With Discount')
    pivot.plot(kind='bar', figsize=(12, 9))
    plt.title('Buy Min Required Qantity Models Distribution in Pharmacies')
    plt.xticks(rotation=10, fontsize=10, ha='right')
    plt.show()
