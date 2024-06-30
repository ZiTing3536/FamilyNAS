from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'  # 上傳文件的存儲目錄
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'mkv'}

# 檢查文件名是否具有允許的擴展名
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 首頁路由
@app.route('/')
def index():
    # 列出上傳文件夾中的所有文件
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

# 文件上傳路由
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))

    return redirect(request.url)

# 文件下載路由
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 文件刪除路由
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': f'{filename} 刪除成功'})
    except Exception as e:
        return jsonify({'message': f'刪除 {filename} 時出錯: {str(e)}'}), 500

if __name__ == '__main__':
    # Use '0.0.0.0' to listen on all network interfaces
    app.run(host='0.0.0.0', port=5000)
