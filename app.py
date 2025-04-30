from flask import Flask, request, redirect, url_for, render_template, send_from_directory

app = Flask(__name__, static_folder='assets')  # Serve assets like CSS/JS

# Home route – returns index.html manually from root directory
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')  # Serve index.html directly

# Handle file upload – if file uploaded, go to next page
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('book-upload')

    if file:
        # Save file to uploads folder
        file.save(f'uploads/{file.filename}')
        return redirect(url_for('next_page'))
    
    return redirect(url_for('home'))

# Next page – rendered from templates folder
@app.route('/nextpage')
def next_page():
    return render_template('nextpage.html')

if __name__ == '__main__':
    app.run(debug=True)
