import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from analysis.discount_analysis import (discount_model_pharmacy, direct_percent,
                                        bulk_min_qty, buy_x_get_y)

from analysis.brand_analysis import brand_avg_pharm
from analysis.load_data import load_query


def discount_distribution():
    df = discount_model_pharmacy()

    pivot = df.pivot(index='Discount Model', columns='Pharmacy', values='Total Number of Items')
    pivot.plot(kind='bar', figsize=(12, 8))
    plt.title('Discount Models in Pharmacies')
    plt.xticks(rotation=10, fontsize=8, ha='right')
    plt.savefig('discount_distribution.png')
    plt.show()

def direct_discount():
    df = direct_percent()

    pivot = df.pivot(index='Pharmacy Name', columns='Item Category', values='Final Price With Discount')
    pivot.plot(kind='bar', figsize=(12, 9))
    plt.title('Direct Discount Models Distribution in Pharmacies')
    plt.xticks(rotation=10, fontsize=10, ha='right')
    plt.savefig('direct_discount.png')
    plt.show()

def bulk_min_qty_discount():
    df = bulk_min_qty()

    pivot = df.pivot(index='Pharmacy Name', columns='Item Category', values='Final Price With Discount')
    pivot.plot(kind='bar', figsize=(12, 9))
    plt.title('Buy Min Required Qantity Models Distribution in Pharmacies')
    plt.xticks(rotation=10, fontsize=10, ha='right')
    plt.savefig('bulk_min_qty_discount.png')
    plt.show()

def buy_get_free_discount():
    df = buy_x_get_y()

    pivot = df.pivot(index='Pharmacy Name', columns='Item Category', values='Final Price With Discount')
    pivot.plot(kind='bar', figsize=(12, 9))
    plt.title('Buy Get Free Models Distribution in Pharmacies')
    plt.xticks(rotation=10, fontsize=10, ha='right')
    plt.savefig('buy_get_free_discount.png')
    plt.show()

def brand_price_range_5():
    df = brand_avg_pharm()

    company_pharmacy_count = df.groupby('Company Name')['Pharmacy'].nunique()
    companies_with_two = company_pharmacy_count[company_pharmacy_count >= 2].index
    filtered = df[
        (df['Total Number of Items'] > 2) &
        (df['Average Price Per Model'] <= 5) &
        (df['Company Name'].isin(companies_with_two))
        ]

    pivot = filtered.pivot(index='Company Name', columns='Pharmacy', values='Average Price Per Model')

    pivot = pivot[pivot.count(axis=1) >= 2]
    pivot = pivot.sort_values('camelia', na_position='last')

    plt.figure(figsize=(12, 10))
    sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn_r', center=pivot.mean().mean())
    plt.title('Average Price by Brand < 5 eur')
    plt.savefig('brand_price_range_5.png')
    plt.show()

def brand_price_range_10():
    df = brand_avg_pharm()

    company_pharmacy_count = df.groupby('Company Name')['Pharmacy'].nunique()
    companies_with_two = company_pharmacy_count[company_pharmacy_count >= 2].index
    filtered = df[
        (df['Total Number of Items'] > 2) &
        (df['Average Price Per Model'] > 5) &
        (df['Average Price Per Model'] <= 10) &
        (df['Company Name'].isin(companies_with_two))
        ]

    pivot = filtered.pivot(index='Company Name', columns='Pharmacy', values='Average Price Per Model')

    pivot = pivot[pivot.count(axis=1) >= 2]
    pivot = pivot.sort_values('camelia', na_position='last')

    plt.figure(figsize=(12, 10))
    sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn_r', center=pivot.mean().mean())
    plt.title('Average Price by Brand Between 5-10 eur')
    plt.savefig('brand_price_range_10.png')
    plt.show()

def brand_price_range_20():
    df = brand_avg_pharm()

    company_pharmacy_count = df.groupby('Company Name')['Pharmacy'].nunique()
    companies_with_two = company_pharmacy_count[company_pharmacy_count >= 2].index
    filtered = df[
        (df['Total Number of Items'] > 2) &
        (df['Average Price Per Model'] > 10) &
        (df['Average Price Per Model'] <= 20) &
        (df['Company Name'].isin(companies_with_two))
        ]

    pivot = filtered.pivot(index='Company Name', columns='Pharmacy', values='Average Price Per Model')

    pivot = pivot[pivot.count(axis=1) >= 2]
    pivot = pivot.sort_values('camelia', na_position='last')

    plt.figure(figsize=(12, 10))
    sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn_r', center=pivot.mean().mean())
    plt.title('Average Price by Brand Between 10-20 eur')
    plt.savefig('brand_price_range_20.png')
    plt.show()

def brand_price_range_20plus():
    df = brand_avg_pharm()

    company_pharmacy_count = df.groupby('Company Name')['Pharmacy'].nunique()
    companies_with_two = company_pharmacy_count[company_pharmacy_count >= 2].index
    filtered = df[
        (df['Total Number of Items'] > 2) &
        (df['Average Price Per Model'] > 20) &
        (df['Company Name'].isin(companies_with_two))
        ]

    pivot = filtered.pivot(index='Company Name', columns='Pharmacy', values='Average Price Per Model')

    pivot = pivot[pivot.count(axis=1) >= 2]
    pivot = pivot.sort_values('camelia', na_position='last')

    plt.figure(figsize=(12, 10))
    sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn_r', vmin=20, vmax=100)
    plt.title('Average Price by Brand > 20 eur')
    plt.savefig('brand_price_range_20plus.png')
    plt.show()




