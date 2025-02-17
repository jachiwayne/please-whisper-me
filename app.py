from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a random key

# Initialize database
def init_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id TEXT PRIMARY KEY, message TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def save_message():
    message = request.form['message']
    unique_id = str(uuid.uuid4())  # Generate unique link ID
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages VALUES (?, ?)", (unique_id, message))
    conn.commit()
    conn.close()
    return redirect(url_for('view_message', message_id=unique_id))

@app.route('/message/<message_id>')
def view_message(message_id):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("SELECT message FROM messages WHERE id = ?", (message_id,))
    result = c.fetchone()
    conn.close()
    if result:
        message = result[0]
        # Delete message after viewing
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        conn.commit()
        conn.close()
        return render_template('message.html', message=message)
    else:
        return "Message not found or already viewed."

if __name__ == '__main__':
    app.run(debug=True)
