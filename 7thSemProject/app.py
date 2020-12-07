from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from flask import Flask, request, render_template, url_for, redirect
import os
from gensim.models import Word2Vec
from pprint import pprint
import re

app = Flask(__name__)

def convertPDFToText(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    string = retstr.getvalue()
    retstr.close()
    return string

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/about', methods=['GET'])
def about():
    return render_template("about.html")

@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':            
            photo.save(os.path.join("/Users/malcolm/Desktop/FinalProjectEndToEnd/7thSemProject/uploads", photo.filename))
        else:
            return render_template("index.html", message="Upload your resume first!")

    path = "/Users/malcolm/Desktop/FinalProjectEndToEnd/7thSemProject/uploads/" + str(photo.filename)
    text = convertPDFToText(path)
    text = text.replace('|',',')
    text = text.replace('/',',')
    text = text.replace('-',',')
    text = text.replace('_',',')
    text = text.replace(':',',')
    text = text.replace('\n',',')
    text = text.split(',')
    text = [word for word in text if word]
    index_of_skills = text.index('SKILLS')
    index_of_skills += 1
    candidate = []
    while text[index_of_skills] != 'PERSONAL PROJECTS':
        candidate.append(text[index_of_skills])
        index_of_skills += 1

    write_skills = [['html5', 'css3', 'javascript'],
    ['microsoft office', 'management', 'microsoft excel'],
    ['microsoft office', 'customer service', 'management'],
    ['c++', 'data structure ', 'graphic design'],
    ['secondary research', 'team building', 'handling of uv equipment'],
    ['microsoft office', 'microsoft excel', 'microsoft word'],
    ['data analytics', 'r', 'sas programming'],
    ['c', 'microsoft office', 'c  '],
    ['technical recruiting', 'contract recruitment', 'headhunting'],
    ['chemical engineering', 'microsoft office', 'powerpoint'],
    ['strategic planning', 'data analysis', 'statistical data analysis'],
    ['microsoft excel', 'microsoft word', 'c'],
    ['microsoft office', 'c', 'microsoft powerpoint'],
    ['java', 'oracle', 'project management'],
    ['management', 'public speaking', 'team leadership'],
    ['event management', 'management', 'public speaking'],
    ['market research', 'data analysis', 'microsoft powerpoint'],
    ['management', 'public speaking', 'team leadership'],
    ['sql', 'c', 'c++'],
    ['html', 'java', 'css'],
    ['microsoft office', 'microsoft excel', 'microsoft word'],
    ['html', 'c++', 'powerpoint'],
    ['object-oriented programming', '(oop)', 'test planning'],
    ['c', 'c++', 'microsoft office'],
    ['c++', 'django', 'cascading style sheets (css)'],
    ['react.js', 'data structures', 'algorithms'],
    ['core java', 'spring framework', 'restful webservices'],
    ['laravel', 'c++', 'python'],
    ['c++', 'data structure ', 'graphic design'],
    ['management', 'public speaking', 'team leadership'],
    ['java', 'turbo c++', 'data structures'],
    ['finance', 'team leadership', 'team management'],
    ['microsoft office', 'microsoft excel', 'microsoft word'],
    ['microsoft excel', 'sql', 'public relations'],
    ['social media', 'blogging', ''],
    ['management', 'public speaking', 'team leadership'],
    ['microsoft office', 'social media marketing', 'social media'],
    ['java', 'c  ', 'c'],
    ['business strategy', 'operations management', 'project management'],
    ['c', 'html', 'social media'],
    ['mobile applications', 'user experience', 'web applications'],
    ['pick basic', 'unidata', 'c'],
    ['c++', 'c', 'cloud computing'],
    ['c', 'c++', 'microsoft office'],
    ['c++', 'c', 'html'],
    ['test cases', 'regression testing', 'testing'],
    ['software quality control', 'functional testing', 'testing'],
    ['core php', 'codeignitr', 'cake php'],
    ['html', 'asp.net', 'java'],
    ['talent acquisition', 'recruiting', 'screening'],
    ['node.js', 'javascript', 'java'],
    ['management', 'public speaking', 'team leadership'],
    ['machine learning', 'python', 'natural language processing'],
    ['java', 'c++', 'c'],
    ['finance', 'team leadership', 'team management'],
    ['java', 'c++', 'mysql'],
    ['business strategy', 'operations management', 'project management'],
    ['core java', 'sql', 'pl/sql'],
    ['algorithms', 'c++', 'python'],
    ['c', 'microsoft office', 'c  '],
    ['java', 'programming', 'spring framework'],
    ['python', 'c', 'html'],
    ['c', 'c++', 'hp qtp'],
    ['core java', 'salesforce', 'tdd'],
    ['c', 'programming', 'c++'],
    ['java', 'python', 'data structures'],
    ['php', 'javascript', 'mysql'],
    ['c', 'microsoft office', 'java'],
    ['java', 'core java', 'c'],
    ['django', 'ember.js', 'chef'],
    ['economics', 'analysis', 'operational excellence'],
    ['c', 'java', 'apache spark'],
    ['management', 'public speaking', 'team leadership'],
    ['java', 'oracle', 'project management'],
    ['data analytics', 'r', 'sas programming'],
    ['node.js', 'javascript', 'java'],
    ['operations management', 'management', 'data-driven decision making'],
    ['python', 'sql', 'c++'],
    ['supply chain management', 'project planning', 'logistics management']]


    f = open("/Users/malcolm/Desktop/FinalProjectEndToEnd/7thSemProject/uploads/resumes.txt", mode='r', encoding='utf-8')
    contents = f.read()
    contents = contents.replace('|', ',')
    contents = contents.replace(':', ',')
    contents = contents.replace('\t', ',')
    contents = contents.replace('~',',')
    contents = contents.replace('.',',')
    skills = contents.split(',')
    skills = [skill for skill in skills if skill]
    skills.remove('Skills')
    skills.extend(candidate)
    for list_write in write_skills:
        skills.extend(list_write)
    for skill in skills:
        skill = skill.strip()

    model = Word2Vec([skills], min_count = 1)

    l = []
    for word in candidate:
        similar = model.wv.most_similar(word)
        l.append(similar)

    recommendation = []
    for skill_list in l:
        for a,b in skill_list:
            if b >= 0.31:
                recommendation.append(a)

    cleaned_recommendations = []
    for r in recommendation:
        k = re.sub('[^A-Za-z]+', ' ', r)
        cleaned_recommendations.append(k.strip())

    final_recommendations = []
    for recommend in cleaned_recommendations:
        if recommend and len(recommend) < 8:
            final_recommendations.append(recommend)

    return render_template('index.html', answer=final_recommendations)

if __name__ == "__main__":
    app.run(debug=True, port=5000)