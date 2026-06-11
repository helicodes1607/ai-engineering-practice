import os
import numpy as np
import matplotlib.pyplot as plt

from openai import OpenAI
from sklearn.manifold import TSNE
from dotenv import load_dotenv


# -----------------------------
# 1. Load OpenAI API key
# -----------------------------

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------
# 2. Example product data
# -----------------------------

products = [
    {
        "title": "Smartphone X1",
        "short_description": "The latest flagship smartphone with AI-powered features and 5G connectivity.",
        "price": 799.99,
        "category": "Electronics",
        "features": [
            "6.5-inch AMOLED display",
            "Quad-camera system with 48MP main sensor",
            "Face recognition and fingerprint sensor",
            "Fast wireless charging"
        ]
    },
    {
        "title": "Running Shoes Pro",
        "short_description": "Lightweight running shoes designed for comfort, speed, and long-distance performance.",
        "price": 129.99,
        "category": "Sportswear",
        "features": [
            "Breathable mesh upper",
            "Cushioned sole",
            "Durable rubber outsole"
        ]
    },
    {
        "title": "Organic Green Tea",
        "short_description": "Premium organic green tea with a fresh aroma and smooth taste.",
        "price": 14.99,
        "category": "Food & Drink",
        "features": [
            "Organic ingredients",
            "Rich antioxidants",
            "Eco-friendly packaging"
        ]
    },
    {
        "title": "Noise-Cancelling Headphones",
        "short_description": "Wireless headphones with active noise cancellation and high-quality sound.",
        "price": 249.99,
        "category": "Electronics",
        "features": [
            "Bluetooth connectivity",
            "Active noise cancellation",
            "Long battery life"
        ]
    },
    {
        "title": "Yoga Mat",
        "short_description": "Non-slip yoga mat made for stretching, balance exercises, and daily workouts.",
        "price": 39.99,
        "category": "Fitness",
        "features": [
            "Non-slip surface",
            "Lightweight design",
            "Easy to clean"
        ]
    },
    {
        "title": "Ceramic Dinner Set",
        "short_description": "Elegant ceramic dinnerware set suitable for everyday meals and special occasions.",
        "price": 89.99,
        "category": "Home & Kitchen",
        "features": [
            "Dishwasher safe",
            "Microwave safe",
            "Modern design"
        ]
    }
]


# -----------------------------
# 3. Extract product descriptions
# -----------------------------

product_descriptions = [
    product["short_description"] for product in products
]


# -----------------------------
# 4. Create embeddings
# -----------------------------

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=product_descriptions
)

response_dict = response.model_dump()


# -----------------------------
# 5. Store embeddings in products
# -----------------------------

for i, product in enumerate(products):
    product["embedding"] = response_dict["data"][i]["embedding"]


# -----------------------------
# 6. Create categories and embeddings lists
# -----------------------------

categories = [product["category"] for product in products]
embeddings = [product["embedding"] for product in products]


# -----------------------------
# 7. Reduce embeddings to 2D using t-SNE
# -----------------------------

tsne = TSNE(
    n_components=2,
    perplexity=5,
    random_state=42
)

embeddings_2d = tsne.fit_transform(np.array(embeddings))


# -----------------------------
# 8. Create scatter plot
# -----------------------------

plt.figure(figsize=(10, 6))

plt.scatter(
    embeddings_2d[:, 0],
    embeddings_2d[:, 1]
)

for i, category in enumerate(categories):
    plt.annotate(
        category,
        (embeddings_2d[i, 0], embeddings_2d[i, 1])
    )

plt.title("2D Visualization of Product Description Embeddings")
plt.xlabel("t-SNE dimension 1")
plt.ylabel("t-SNE dimension 2")

plt.show()