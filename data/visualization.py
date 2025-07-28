import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# קריאת הקובץ
df = pd.read_csv('cleaned_data.csv')

correlation_matrix = df.corr(numeric_only=True)

# ציור קורלציה
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix')
plt.tight_layout()
#plt.savefig('graphs/correlation_matrix.png', dpi=300)
#plt.show()

# ציור היטמאפ מחיר
plt.figure(figsize=(8,6))
sns.histplot(df['price'], bins=30, kde=True)
plt.title('Price Distribution')
plt.xlabel('Price')
plt.ylabel('Count')
#plt.savefig('graphs/price_distribution.png', dpi=300)
#plt.show()

# מחיר מול התקרבות לטיסה
plt.figure(figsize=(8, 6))
# פיזור הנתונים בפועל
sns.scatterplot(x='days_before_departure', y='price', data=df, alpha=0.4)
# קו מגמה חלק (לא לינארי - lowess)
sns.regplot(x='days_before_departure', y='price', data=df, scatter=False, lowess=True, color='red')
plt.title('Price vs. Days Before Departure')
plt.xlabel('Days Before Departure')
plt.ylabel('Price')
plt.tight_layout()
#plt.savefig('graphs/price_vs_days_before.png', dpi=300)
#plt.show()

plt.figure(figsize=(8,6))
sns.barplot(x='day_of_week', y='price', data=df)
plt.title('Average Price by Day of Week')
#plt.savefig('graphs/price_by_day_of_week.png', dpi=300)
#plt.show()

plt.figure(figsize=(6,5))
sns.boxplot(x='is_summer', y='price', data=df)
plt.xticks([0, 1], ['Not Summer', 'Summer'])
plt.title('Price Distribution: Summer vs Not Summer')
#plt.savefig('graphs/price_summer_vs_not.png', dpi=300)
#plt.show()

plt.figure(figsize=(10,6))
sns.lineplot(x='hour', y='price', data=df)
plt.title('Average Price by Hour of Day')
#plt.savefig('graphs/price_by_hour.png', dpi=300)
#plt.show()

top_dest = df['destination'].value_counts().nlargest(10).index
plt.figure(figsize=(10,6))
sns.boxplot(x='destination', y='price', data=df[df['destination'].isin(top_dest)])
plt.title('Price Distribution by Destination')
#plt.savefig('graphs/price_by_destination.png', dpi=300)
#plt.show()

