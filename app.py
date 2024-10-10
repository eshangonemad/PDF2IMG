import os#thjgh
import fitz  # jgu
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
#thhj
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
EXTRACT_FOLDER = 'home'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXTRACT_FOLDER'] = EXTRACT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)
    
@app.route('/')
def upload_pdf():
    return render_template('upload.html')
   
@app.route('/upload', methods=['POST'])
def handle_upload():
    if 'pdf_files' not in request.files:
        return "No file part", 400
    
    files = request.files.getlist('pdf_files')  

    if not files or files[0].filename == '':
        return "No selected files", 400 

    response_messages = []

    for file in files:
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(pdf_path)

            # Extract pages as high-quality images for each PDF
            extract_high_quality_images_from_pdf(pdf_path)
            response_messages.append(f"Processed {filename} successfully!")

    return jsonify({"messages": response_messages})

def extract_high_quality_images_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)

    zoom = 6.0  
    mat = fitz.Matrix(zoom, zoom)  

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)  
        pix = page.get_pixmap(matrix=mat)  
        image_filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{page_num+1}.png"
        image_path = os.path.join(app.config['EXTRACT_FOLDER'], image_filename)
        pix.save(image_path)  

    pdf_document.close()

if __name__ == "__main__":
    app.run(debug=True)
