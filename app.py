
import streamlit as st
import json
import pandas as pd
import plotly.express as px

# ---------------------- Load & Save Books ----------------------
def load_books():
    try:
        with open("books.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_books(books):
    with open("books.json", "w") as file:
        json.dump(books, file, indent=4)

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")
st.title("📚 Personal Library Manager")
st.write("Easily track, add, and search your book collection!")

# ---------------------- Add Book Section ----------------------
st.subheader("➕ Add a New Book")
with st.form("add_book_form"):
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Book Title")
        author = st.text_input("Author")
    with col2:
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Mystery", "Sci-Fi", "Other"])
        rating = st.slider("Rating", 1, 5)
    submitted = st.form_submit_button("Add Book")
    if submitted and title and author:
        books = load_books()
        books.append({"title": title, "author": author, "genre": genre, "rating": rating})
        save_books(books)
        st.success("✅ Book added successfully!")
        st.rerun()

# ---------------------- Display Book Collection ----------------------
st.subheader("📖 Your Book Collection")
st.markdown("---")
books = load_books()

if books:
    search_query = st.text_input("🔍 Enter title or author to search")
    search_clicked = st.button("Search")

    filtered_books = books
    if search_clicked and search_query:
        filtered_books = [book for book in books if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]

    # Stylish Book Display
    col1, col2, col3 = st.columns(3)
    for i, book in enumerate(filtered_books):
        with [col1, col2, col3][i % 3]:
            st.markdown(
                f"""
                <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:10px; 
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1); transition: transform 0.2s ease-in-out;">
                    <h3 style="color:#333; margin-bottom:5px;">📖 {book['title']}</h3>
                    <p><strong>✍️ Author:</strong> {book['author']}</p>
                    <p><strong>📚 Genre:</strong> {book['genre']}</p>
                    <p><strong>⭐ Rating:</strong> {'⭐' * book['rating']}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

    # ---------------------- Data Visualization ----------------------
    st.subheader("📊 Library Insights")
    st.markdown("---")
    df = pd.DataFrame(books)
    col1, col2 = st.columns(2)
    with col1:
        genre_chart = px.pie(df, names="genre", title="Books by Genre", hole=0.3, color_discrete_sequence=px.colors.sequential.Plasma)
        st.plotly_chart(genre_chart)
    with col2:
        rating_chart = px.bar(df, x="rating", title="Books by Rating", text_auto=True, color="rating", color_continuous_scale="blues")
        st.plotly_chart(rating_chart)

    # ---------------------- Export Data ----------------------
    st.download_button("📥 Export as JSON", json.dumps(books, indent=4), "books.json", "application/json")
else:
    st.warning("No books found! Start adding books now.")
