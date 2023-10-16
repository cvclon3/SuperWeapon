import pandas as pd
import matplotlib.pyplot as plt


# Read file
df = pd.read_csv('data.csv')

x_shell = df['x_shell'].to_list()
y_shell = df['y_shell'].to_list()

# Draw plot
plt.scatter(x_shell, y_shell, marker='o')
plt.show()