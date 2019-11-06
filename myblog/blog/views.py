from django.shortcuts import render

from django.http import HttpResponse
#从models导入Category类
from .models import Category, Banner, Article, Tag, Link
#导入分页插件包
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
#首页
def index(request):
    
    #查询所有幻灯片数据 并进行切片
    banner = Banner.objects.filter(is_active=True)[0:4]

    #查询推荐位ID为1的文章,tui_id=1表示通过文章里的外键推荐位进行筛选
    tui = Article.objects.filter(tui_id=1)[:3]

    #最新文章
    allArticle = Article.objects.all().order_by('-id')[0:10]

    #热门文章,通过浏览记录排序
    hot = Article.objects.all().order_by('views')[:10]

    #友情链接
    link = Link.objects.all()

    #把上下文传递到index.html页面
    return render(request, 'index.html', locals())

#列表页
def list(request, lid):
    #获取通过URL传进来的lid，然后筛选出对应文章
    list = Article.objects.filter(category_id=lid)
    #获取当前文章的栏目名
    cname = Category.objects.get(id=lid)

    #在URL中获取当前页面数
    page = request.GET.get('page')
    #对查询到的数据对象list进行分页，设置超过5条数据就分页
    paginator = Paginator(list, 5)
    try:
        #获取当前页码的记录
        list = paginator.page(page)
    except PageNotAnInteger:
        #如果用户输入的页码不是整数时,显示第1页的内容
        list = paginator.page(1)
    except EmptyPage:
        #如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        list = paginator.page(paginator.num_pages)



    #这个locals()代替了context，locals()的作用是返回一个包含当前作用域里面的所有变量和它们的值的字典。
    return render(request, 'list.html', locals())


#内容页
def show(request, sid):
    #查询指定ID的文章
    show = Article.objects.get(id=sid)

    #内容下面的您可能感兴趣的文章，随机推荐
    hot = Article.objects.all().order_by('?')[:10]
    previous_blog = Article.objects.filter(created_time__gt=show.created_time, category=show.category.id).first()
    next_blog = Article.objects.filter(created_time__lt=show.created_time, category=show.category.id).last()
    show.views = show.views+1
    show.save()
    return render(request, 'show.html', locals())

#标签页
def tag(request, tag):
    #通过文章标签进行查询文章
    list = Article.objects.filter(tags__name=tag)
   
    #获取当前搜索的标签名
    tname = Tag.objects.get(name=tag)
    page = request.GET.get('page')
    paginator = Paginator(list, 5)
    try:
        #获取当前搜索的标签名
        list = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户输入的页码不是整数时,显示第1页的内容
        list = paginator.page(1)
    except EmptyPage:
        # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        list = paginator.page(paginator.num_pages)

    return render(request, 'tags.html', locals())


#搜索页
def search(request):
    #获取搜索关键词
    ss = request.GET.get('search')
    #获取到搜索关键词通过标题进行匹配
    list = Article.objects.filter(title__icontains=ss)
    
    page = request.GET.get('page')

    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page) # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1) # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'search.html', locals())

#关于我们
def about(request):
    return render(request, 'page.html', locals())


def global_variable(request):
    #通过Category类表查出所有的分类
    allcategory = Category.objects.all()

    #右侧热门推荐
    remen = Article.objects.filter(tui_id=2)[:6]

    #右侧所有标签的实现
    tags = Tag.objects.all()

    return locals()
