import json
import streamlit as st

class BookCollection:
    def __init__(self):
        self.book_list = []
        self.storage_file = "books_data.json"
        self.read_from_file()

    def read_from_file(self):
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    def save_to_file(self):
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)

    def add_book(self, title, author, year, genre, read):
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read,
        }
        self.book_list.append(new_book)
        self.save_to_file()

    def delete_book(self, title):
        self.book_list = [book for book in self.book_list if book["title"].lower() != title.lower()]
        self.save_to_file()

    def find_books(self, search_text):
        return [book for book in self.book_list if search_text.lower() in book["title"].lower() or search_text.lower() in book["author"].lower()]

    def update_book(self, old_title, new_data):
        for book in self.book_list:
            if book["title"].lower() == old_title.lower():
                book.update(new_data)
                self.save_to_file()
                return True
        return False

    def show_all_books(self):
        return self.book_list

    def reading_progress(self):
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])
        return total_books, completed_books, (completed_books / total_books * 100) if total_books > 0 else 0

book_manager = BookCollection()

st.title("📚 Personal Book Library 📖")

menu = st.sidebar.radio("📌 Navigation", ["➕ Add Book", "📚 View Books", "🔍 Search Book", "✏️ Update Book", "🗑️ Delete Book", "📊 Reading Progress"])

if menu == "➕ Add Book":
    with st.form("add_book_form"):
        title = st.text_input("📖 Book Title")
        author = st.text_input("✍️ Author")
        year = st.text_input("📅 Publication Year")
        genre = st.text_input("📂 Genre")
        read = st.checkbox("✅ Have you read this book?")
        submitted = st.form_submit_button("➕ Add Book")
    
    if submitted and title:
        book_manager.add_book(title, author, year, genre, read)
        st.success("🎉 Book added successfully!")

elif menu == "📚 View Books":
    books = book_manager.show_all_books()
    if books:
        for book in books:
            st.write(f"📖 **{book['title']}** by ✍️ {book['author']} ({book['year']}) - 📂 {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.write("🚫 No books in collection.")

elif menu == "🔍 Search Book":
    search_text = st.text_input("🔎 Search by Title or Author")
    if st.button("🔍 Search"):
        results = book_manager.find_books(search_text)
        if results:
            for book in results:
                st.write(f"📖 **{book['title']}** by ✍️ {book['author']} ({book['year']}) - 📂 {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.write("🚫 No matching books found.")

elif menu == "✏️ Update Book":
    book_title = st.text_input("✏️ Enter the title of the book to update")
    with st.form("update_book_form"):
        new_title = st.text_input("📖 New Title")
        new_author = st.text_input("✍️ New Author")
        new_year = st.text_input("📅 New Publication Year")
        new_genre = st.text_input("📂 New Genre")
        new_read = st.checkbox("✅ Mark as Read")
        update_submitted = st.form_submit_button("🔄 Update Book")
    
    if update_submitted and book_title:
        update_data = {"title": new_title, "author": new_author, "year": new_year, "genre": new_genre, "read": new_read}
        update_data = {k: v for k, v in update_data.items() if v}  # Remove empty values
        if book_manager.update_book(book_title, update_data):
            st.success("✅ Book updated successfully!")
        else:
            st.error("❌ Book not found!")

elif menu == "🗑️ Delete Book":
    delete_title = st.text_input("🗑️ Enter the title of the book to delete")
    if st.button("❌ Delete"):
        book_manager.delete_book(delete_title)
        st.success("🗑️ Book deleted successfully!")

elif menu == "📊 Reading Progress":
    total, completed, progress = book_manager.reading_progress()
    st.write(f"📚 **Total Books:** {total}")
    st.write(f"✅ **Books Read:** {completed}")
    st.write(f"📊 **Reading Completion:** {progress:.2f}%")
    st.progress(progress / 100)
