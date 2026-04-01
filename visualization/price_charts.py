from analysis.price_analysis import (avg_price_cat, avg_cat_pharm,
                                     price_range, price_range_sum)
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def compare_pharmacies_prices():
    df = avg_cat_pharm()

    pivot = df.pivot(index="Categories", columns="Pharmacy", values="Average Price")

    pivot.plot(kind="bar", figsize=(12,8))
    plt.title("Pharmacy Price Comparison")
    plt.xticks(rotation=10, fontsize=8, ha='right')
    plt.show()

def price_range():
    df = price_range_sum()

    df_long = df.melt(id_vars=['Pharmacy', 'Category'],
                      value_vars=['< 5€', '5€ - 10€', '10€ - 20€', '> 20€'],
                      var_name='Price Range', value_name='Total Number')

    sns.barplot(data=df_long, x='Pharmacy', y='Total Number', hue='Price Range', palette='viridis')
    plt.title('Price Range Distribution per Pharmacy')
    plt.show()

def category_range():
    df = price_range_sum()

    plt.figure(figsize=(16, 8))
    df_long = df.melt(id_vars=['Pharmacy', 'Category'],
                      value_vars=['< 5€', '5€ - 10€', '10€ - 20€', '> 20€'],
                      var_name='Price Range', value_name='Total Number')

    sns.barplot(data=df_long, x='Category', y='Total Number', hue='Price Range', palette='viridis')
    plt.xticks(rotation=10, ha='right')
    plt.title('Price Range Distribution per Pharmacy')
    plt.show()

def price_heatmap():
    df = avg_cat_pharm()

    plt.figure(figsize=(18,8))
    pivot = df.pivot(index='Categories', columns='Pharmacy', values='Average Price')
    sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn_r', center=pivot.mean().mean())
    plt.title('Average Price Heatmap')
    plt.show()

