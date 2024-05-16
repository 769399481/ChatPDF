# Flask 部分的代码
from flask import Flask, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import nltk
import warnings
from elasticsearch7 import Elasticsearch, helpers
from pdf_processing.pdf_utils import extract_text_from_pdf
from pdf_processing.elasticsearch_utils import search, to_keywords
from openai_interaction.openai_utils import get_completion, build_prompt
import os
import shutil

app = Flask(__name__)

warnings.simplefilter("ignore")  # 屏蔽 ES 的一些Warnings
nltk.download('punkt')  # 英文切词、词根、切句等方法
nltk.download('stopwords')  # 英文停用词库

# 1. 创建Elasticsearch连接
es = Elasticsearch(
    hosts=['x'],  # 服务地址与端口
    http_auth=("x", "x"),  # 用户名，密码
)

# 2. 定义索引名称
index_name = "x"

# 3. 如果索引已存在，删除它（仅供演示，实际应用时不需要这步）
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# 4. 创建索引
es.indices.create(index=index_name)

# 文件上传配置
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 删除并重新创建 upload 文件夹的函数
def recreate_upload_folder():
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        recreate_upload_folder()  # 调用重新构建 upload 文件夹的函数
        return f.read()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 处理文件上传
        if 'pdfFile' not in request.files:
            return 'No file part'
        file = request.files['pdfFile']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # 提取文本内容并存储到Elasticsearch中
            global paragraphs
            paragraphs = extract_text_from_pdf(file_path, min_line_length=10)
            actions = [
                {
                    "_index": index_name,
                    "_source": {
                        "keywords": to_keywords(para),
                        "text": para
                    }
                }
                for para in paragraphs
            ]
            helpers.bulk(es, actions)
            return redirect(url_for('qa'))
        else:
            return 'File type not allowed'
    else:
        # 处理GET请求，返回上传文件夹内的文件列表
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify(files)
    
# 路由：问答页面
@app.route('/qa')
def qa():
    with open('qa.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/pdf_viewer/<path:filename>')
def pdf_viewer(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 路由：搜索问答
@app.route('/search', methods=['POST'])
def search_result():
    prompt_template = """
    你是一个问答机器人。
    你的任务是根据下述给定的已知信息回答用户问题。
    确保你的回复完全依据下述已知信息。不要编造答案。
    如果下述已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。

    已知信息:
    __INFO__

    用户问：
    __QUERY__

    请用英文回答用户问题。
    """

    user_query = request.form['query']
    search_results = search(es, index_name, paragraphs, user_query, 2)
    print(search_results)
    prompt = build_prompt(prompt_template, info=search_results, query=user_query)
    response = get_completion(prompt)
    return response

if __name__ == '__main__':
    app.run(debug=True)
