import requests
import json
# lxml是一个流行的解析库，使用的是Xpath语法，可以解析HTML
from lxml import etree
from selenium import webdriver

query = '王祖贤'
downloadPath = 'D:/photos/'
# chromedriver需要配置环境变量，查看网上资料说建议放到python的Scripts目录下
chromedriverPath = 'C:/Users/xiaozhenzhen/PycharmProjects/unknown/Scripts/'

''' 下载图片 '''


def download(src, id):
    dir = downloadPath + str(id) + '.jpg'
    try:
        pic = requests.get(src, timeout=10)
        fp = open(dir, 'wb')
        fp.write(pic.content)
        fp.close()
    except requests.exceptions.ConnectionError:
        print('图片无法下载')


# 数据是json格式
def getPhotos():
    ''' for 循环 请求全部的 url '''
    for i in range(0, 100, 20):
        url = 'https://www.douban.com/j/search_photo?q=' + query + '&limit=20&start=' + str(i)
        html = requests.get(url).text  # 得到返回结果
        response = json.loads(html, encoding='utf-8')  # 将 JSON 格式转换成 Python 对象
        for image in response['images']:
            print(image['src'])  # 查看当前下载的图片网址
            download(image['src'], image['id'])  # 下载一张图片


# 数据是 html格式，有时候网页会用 JS请求数据，只有等JS都加载结束后，才能获取完成的html，但xpath不受限制
def getMoviePhotos():
    url = 'https://movie.douban.com/subject_search?search_text=' + query + '&cat=1002'
    driver = webdriver.Chrome(chromedriverPath)
    driver.get(url)
    # 初始化
    html = etree.HTML(driver.page_source)
    # 使用xpath helper, ctrl+shit+x 选中元素
    # xpath 语法 http://www.w3school.com.cn/xpath/xpath_syntax.asp
    src_xpath = "//div[@class='item-root']/a[@class='cover-link']/img[@class='cover']/@src"
    title_xpath = "//div[@class='item-root']/div[@class='detail']/div[@class='title']/a[@class='title-text']"

    srcs = html.xpath(src_xpath)
    titles = html.xpath(title_xpath)
    # zip()函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，返回由元祖组成的对象。优点是节约内存
    # 参考 http://www.runoob.com/python3/python3-func-zip.html
    for src, title in zip(srcs, titles):
        # join 字符串拼接
        print('\t'.join([str(src), str(title.text)]))
        download(src, title.text)

    driver.close()


getPhotos()
getMoviePhotos()