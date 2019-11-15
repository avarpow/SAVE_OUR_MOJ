import requests
import json
import os
import time
import urllib.request
request_url= "https://oj.vmatrix.org.cn/api/"
t = requests.session()
login_header = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "dnt": "1",
    "referer": "https://oj.vmatrix.org.cn/oj/problem/5",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
}
s = t.get(request_url + "auth/login", headers=login_header)
login_header['cookie'] = s.headers['Set-Cookie']
post_content={}
post_content["captcha"] = ""
if os.path.isdir('imports'):
    pass
else:
    os.mkdir('imports')
urllib.request.urlretrieve("https://cdn.jsdelivr.net/npm/marked/marked.min.js",'imports/marked.min.js')
urllib.request.urlretrieve("http://cdn.static.runoob.com/libs/jquery/1.10.2/jquery.min.js",'imports/jquery.min.js')
while (1):
    post_content['email'] = input("输入邮箱")
    post_content['password'] = input("输入密码")
    msg_login = t.post(request_url + "auth/login", headers=login_header, data=post_content)
    msg_login_json=json.loads(msg_login.text)
    if (msg_login_json['status'] == "OK"):
        print("登录成功")
        login_header['cookie'] = msg_login.headers['Set-Cookie']
        break
    print("登录失败，retry please")
#获取jquery marked
if os.path.isdir('imports'):
    pass
else:
    os.mkdir('imports')
urllib.request.urlretrieve("https://cdn.jsdelivr.net/npm/marked/marked.min.js",'imports/marked.min.js')
urllib.request.urlretrieve("http://cdn.static.runoob.com/libs/jquery/1.10.2/jquery.min.js",'imports/jquery.min.js')
#获取问题
if os.path.isdir('submissions'):
    pass
else:
    os.mkdir('submissions')
for i in range(1,151):
    s = t.get(request_url + "problems/" + str(i) + "/submissions", headers=login_header)
    f = open("submissions/"+str(i)+".json",'w',encoding='utf-8')
    f.write(s.text)
    f.close()
    time.sleep(0.05)
    print('提交'+str(i)+' 获取完成')
print("提交获取完成")
if os.path.isdir('problems'):
    pass
else:
    os.mkdir('problems')
for i in range(1,151):
    s = t.get(request_url + "problems/" + str(i) + "", headers=login_header)
    f = open("problems/"+str(i)+".json",'w',encoding='utf-8')
    f.write(s.text)
    f.close()
    time.sleep(0.05)
    print('问题'+str(i)+' 获取完成')
print("全部问题获取完成")
submission_ids = []
for i in range(1, 151):
    f = open('submissions/' + str(i) + '.json', 'r', encoding='utf-8')
    js = json.load(f)
    js_data=js['data']
    for j in js_data:
        submission_ids.append(j['sub_id'])
    print('代码'+str(i)+' 获取完成')
print("代码目录获取完成")
if os.path.isdir('codes'):
    pass
else:
    os.mkdir('codes')    
for i in submission_ids:
     s = t.get(request_url+"problems/45/submissions/"+str(i)+"",headers=login_header)
     f = open("codes/"+str(i)+".json",'w',encoding='utf-8')
     f.write(s.text)
     f.close()
     time.sleep(0.05)
     print('提交'+str(i)+' 获取完成')
print("代码获取完成")   
#生成主页
f = open("index.html", 'w', encoding='utf-8')
f.write(
    '''<!doctype html>
<html>

<head>
    <meta charset="utf-8" />
    <title>mirrors of moj</title>
    <style>
    body {
        text-align: center;
    }
    </style>
</head>

<body>
    '''
)
for i in range(1, 151):
    s="<div><a href=\"pages/"+str(i)+".html\">Problem "+str(i)+"</a></div>\n"
    f.write(s)
f.write(
'''</body>

</html>
''')
f.close()
print("生成主页完成")
#生成资源页面
if os.path.isdir('pages'):
    pass
else:
    os.mkdir('pages')
for i in range(1,151):
    f = open("pages/"+str(i)+".html", 'w', encoding='utf-8')
    head ='''
    <!doctype html>
        <html>
        <head>
        <meta charset="utf-8"/>
        <script src="../imports/marked.min.js"></script>
        <script src="../imports/jquery.min.js"></script>
        <style>
        body {
            text-align: left;
            width: 60%;
            margin: auto;
        }
        </style>
        <title>Problem  '''+str(i)+'''</title>
        </head>
        </html>
    '''
    body_start = '''
        <body>
        <h1>Problem  '''+str(i)+'''</h1>
        <div id="description"></div>
        <div>你的提交</div>
    '''
    discription_t  = open('problems/' + str(i) + '.json', 'r', encoding='utf-8')
    discriptionjs_t = json.load(discription_t)
    discriptionjs_data = discriptionjs_t['data']
    discription = discriptionjs_data[0]['description']
    discription_script="$('#description')[0].innerHTML= marked(" + repr(discription) + ");\n"
    submission_ids = []
    code_raws = []
    code_grades=[]
    submission_t = open('submissions/' + str(i) + '.json', 'r', encoding='utf-8')
    js_t = json.load(submission_t)
    js_data_t=js_t['data']
    for j in js_data_t:
        submission_ids.append(j['sub_id'])
    for j in submission_ids:
        codes_t = open('codes/' + str(j) + '.json', 'r', encoding='utf-8')
        codejs_t = json.load(codes_t)
        code_data_t = codejs_t['data']
        code_raw = code_data_t['code']
        code_raws.append(code_raw)
        code_grade = code_data_t['grade']
        code_grades.append(code_grade)
    code_start = '''
    <script>
    window.onload=function(){
    '''
    code_mid=""
    for j in range(0, len(code_raws)):
        code_mid = code_mid + "$('#code" + str(j) + "')[0].innerHTML='<pre><code>" + (repr(code_raws[j].replace('<', '&lt;').replace('>', '&gt;')))[1:-1] + " </pre></code>\';\n"
        code_mid=code_mid+"$('#code_grade" + str(j) + "')[0].innerHTML= '你以上代码的得分：" + str(code_grades[j]) + "';\n"
    code_end = "}\n</script>"
    code_script = code_start + code_mid + discription_script + code_end
    body_mid=""
    for j in range(0, len(code_raws)):
        body_mid = body_mid + "<div id='code" + str(j) + "'></div>\n"
        body_mid = body_mid + "<div id='code_grade" + str(j) + "'></div>\n"
    body_end = "</body>\n</html>"
    f.write(head + body_start + body_mid + code_script + body_end)
    print("pages/"+str(i)+".html 生成完成")
    f.close()

print("-----------------------------ALL FINISH---------------------------")




