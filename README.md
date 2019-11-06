# mgblog-django
使用Django框架搭建的博客


本文是参考[Django博客开发教程](https://www.django.cn/course/show-32.html)而完成的，只是对其中的命令做简要的记录，具体内容请移步至原教程。

## **创建项目**

**若使用Pycharm创建**，[参考](https://www.django.cn/course/show-35.html)

**若使用命令行创建**
1.创建工程文件夹

```bash
mkdir myproject
cd myproject
```

2.创建虚拟环境

```bash
virtualenv venv -p python3
```

3.开启虚拟环境

```bash
source venv/bin/activate
```

4.安装Django

```bash
pip install django==2.1.1
```

5.开始新项目

```bash
django-admin startproject myblog
```


6.启动django自带的服务器

```bash
python manage.py runserver
```

启动成功，在浏览器中打开 [http://127.0.0.1:8080](http://127.0.0.1:8080) 

7.创建APP

```bash
django-admin startup blog
```


## 基础配置

1.设置域名访问权限

```python
myblog/settings.py
ALLOWED_HOSTS = []      #修改前
ALLOWED_HOSTS = ['*']   #修改后，表示任何域名都能访问。如果指定域名的话，在''里放入指定的域名即可
```

2.添加模版templates的路径

```python
myblog/settings.py
#修改前
'DIRS': []
#修改后
'DIRS': [os.path.join(BASE_DIR, 'templates')]
注：使用pycharm创建的话会自动添加
```

3.添加APP应用名称

```python
myblog/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    ....
    'blog',#注册APP应用
]
#使用pycharm创建的话，这里自动添加了，如果是终端命令创建的话，需要手动添加应用名称如'blog',
```

4.修改项目语言和时区

```python
myblog/settings.py
#修改前为英文
LANGUAGE_CODE = 'en-us'
#修改后
LANGUAGE_CODE = 'zh-hans' #语言修改为中文
#时区，修改前
TIME_ZONE = 'UTC'
#修改后
TIME_ZONE = 'Asia/Shanghai' #
```

5.设置静态目录static和存放上传文件media

```python
myblog/settings.py

#设置静态文件目录和名称
STATIC_URL = '/static/'

#加入下面代码

#这个是设置静态文件夹目录的路径
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
#设置文件上传路径，图片上传、文件上传都会存放在此目录里
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 欢迎界面

用命令行执行，每次打开Terminal需要开启虚拟环境

创建管理账号和密码

```python
python manage.py runserver #默认使用8000端口
python manage.py runserver 8080 #指定启动端口
python manage.py runserver 127.0.0.1:9000 #指定IP和端口
```

打开blog目录下的views.py

```python
myblog/blog/views.py

from django.http import HttpResponse

def hello(request):
    return HttpResponse('欢迎使用Django！')
```

打开myblog目录下的urls.py

```python
myblog/myblog/urls.py

from django.contrib import admin
from django.urls import path
from blog import views         #+ 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello),   #+
]
```

启动服务，打开页面 [http://127.0.0.1:8080](http://127.0.0.1:8080) ，或者刷新页面。
访问  [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  自带的后台管理页面。

## 创建数据模型并进行数据库迁移

代码详情看[Demo](https://github.com/cxymq/mgblog-django)的 model.py

执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

产生错误，查看底部的 问题1。

## Admin后台管理

代码详情看[Demo](https://github.com/cxymq/mgblog-django)的 admin.py

在管理后台使用富文本添加数据

1.下载 [DjangoUeditor包](https://www.django.cn/media/upfile/DjangoUeditor_20181010013851_248.zip
)，解压到项目根目录。

2.settings.py中注册APP

```python
myblog/settings.y
INSTALLED_APPS = [
    'django.contrib.admin',
    ....
    'DjangoUeditor', #注册APP应用
]
```

3.myblog/urls.py 添加url

```python
myblog/urls.py
...
from django.urls import path, include
#留意上面这行比原来多了一个include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello),
    path('ueditor/', include('DjangoUeditor.urls')), #添加DjangoUeditor的URL
]
```

4.修改model的body字段

```python
blog/models.py
from DjangoUeditor.models import UEditorField #头部增加这行代码导入UEditorField

body = UEditorField('内容', width=800, height=500, 
                    toolbars="full", imagePath="upimg/", filePath="upfile/",
                    upload_settings={"imageMaxSize": 1204000},
                    settings={}, command=None, blank=True
                    )
```

**随后启动服务，在添加文章时出错，根据提示修改 boundfield.py，注释93行即可。**
下面是错误详情：

```python
render() got an unexpected keyword argument 'renderer'

/Users/wq/Desktop/backup/Codes/python/myblog/venv/lib/python3.7/site-packages/django/forms/boundfield.py in as_widget, line 93
```

在使用富文本编辑器时，上传图片，无法显示，需要在 myblog/urls.py 如下设置：

```python
myblog/urls.py
....
from django.urls import path, include, re_path
#上面这行多加了一个re_path
from django.views.static import serve
#导入静态文件模块
from django.conf import settings
#导入配置文件里的文件上传配置

urlpatterns = [
    path('admin/', admin.site.urls),
    ....
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),#增加此行
]
```

至此，准备工作基本完成。后续需要实现项目页面，如首页、文章列表、文章内容、标签、搜索等等。

查看[原教程](https://www.django.cn/course/show-32.html)

**注意：原作者并未完全开放源代码，原意是希望学习此教程的人都可以动手，然后完成整个项目。此举不仅能够熟悉项目流程，还可以实战操作Django。希望大家不要辜负原博主的一番苦心。**

我已经完成了[本文 demo](https://github.com/cxymq/mgblog-django)，所以你呢？

不过，就算实操一边，还是无法完全记住所有的配置，需要多学多练，若是工作中用到还好，用不到的话就是来混个脸熟（emmmm......尴尬，我就是）。


## 遇到的问题：

1.模型文件完成后，执行数据库迁移出错

```bash
python manage.py makemigrations
```

错误如下：

```bash
blog.Article.img: (fields.E210) Cannot use ImageField because Pillow is not installed.
 	HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "pip install Pillow".
blog.Banner.img: (fields.E210) Cannot use ImageField because Pillow is not installed.
 	HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "pip install Pillow".
```

根据提示，安装Pillow，完成之后再执行迁移工作。

```bash
pip install Pillow
```

2.如果遇到轮播图无法展示的情况，在后台管理页面增加轮播图即可，其他类别也是如此。

参考：

[Django博客开发教程](https://www.django.cn/course/show-32.html)



-----------------------------------------------------------

[个人博客](https://blog.csdn.net/Crazy_SunShine)

[Github](https://github.com/cxymq)

[个人公众号:Flutter小同学]![https://github.com/cxymq/Images/blob/master/0.失败预加载图片/error.jpg](https://github.com/cxymq/Images/blob/master/1.公众号二维码/qrcode.png)

[个人网站](http://chenhui.today/)




