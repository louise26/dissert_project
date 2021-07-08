# Importing modules
import pandas as pd
from wordcloud import WordCloud

# Read data into papers
policy = pd.read_csv("Google.com.txt", delimiter = "\t")

# Print head
print(policy)