だんだんとdjangoの全体像をつかみつつあると思います！どんどん行きましょう！　　
前回はモデル：データベース関連のことを中心にやりました。今回はMVCモデルのV：ビューの作成を重点的にやっていきます。　　
　　
viewがどういう役割だったか思い出してみましょう。urlConfからアクセスされているurlを判別し。適切な画面を表示することでした。　　
念のため、現在のpolls/views.py, urls.pyが現在どんな感じになっているかを確認してみましょう。　　
　　
djangoでは、ビューはview.pyの関数、もしくはクラスメソッドとして実装されます。それが、urls.pyのpath関数の第二引数としてつかわれるんでしたね。　　
　　
みなさん気づきましたか？ここでDjangoチュートリアル先輩のアメリカンジョークがさく裂しています。「今あなたのウェブ上でME2/site/...」っていうやつです。「こんなURL見にくくてチョー汚いだろジェシー。もっとアメイジングなurlを見せてあげるからウチにおいでよ」って意味です。はいここ笑うところ！HAHAHA！　　
　　
# URLからの入力を受け取る  
もうちょっとviewを書き足して、ビューの数を増やしていきましょう。　　
```python:views.py
# 追加
def detail(request, question_id):
    response = "質問 %s をみてるよ"
    return HttpResponse(response % question_id)

def result(request, question_id):
    response = "質問 %s の結果をみてるよ"
    return HttpResponse(response % question_id)

def vote(request, question_id):
    response = "質問 %s の投票結果をみてるよ"
    return HttpResponse(response % question_id)


```
%s は、f記法のようなストリングリテラルです。[参考はこちら](https://coroconlab.com/percent_operator/)  
ではビューができたので、Urlとの紐づけを行いましょう。urls.pyを編集します.  
```pythpn
# 追加
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/result/", views.result, name="result"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```
ここで、path引数の第一引数に注目、って言われなくても注目しますよね。ここで/polls/の次のurlを、question_IDというデータとして受け取ります。そしてviews.pyの各関数（ビュー）の第二引数として与えられ、のちに該当するデータをモデルから参照するわけです。runserverしてpolls/34/vote とかをみにいくとこんな感じになります  
　![img.png](images%2Fimg.png)
　　
# 404か、404以外か　　
〇ーランドか笑　今回のチュートリアル先輩、キレッキレですね。　
まあつまり、HttpResponseを受け取ったあとのビューの仕事は、実のところ、404(そんなurlねーよエラー)を返すか、用意されたページを表示するかのどっちかしかなく、表示したいならなんでも表示できるってわけです。　　
今回はデータベースからデータを持ってきたりしてますが、おしゃれでファンシーなHTML・CSSを書いてもよし、Hello　Worldを表示するでもよし、ということです。  
### 動的なビューを書いてみる  
前回のdatabase apiを使って、index(/polls/)のビューをつくりましょう。  
まずは、Questionモデルにアクセスしなくちゃいけないので、  
```python
from .models import Question
```  
とします。  
そして、questionモデルの質問の最新5件を、新着順に並べて表示するコードを書いていきます。  
```python:polls/models.py
from django.template import loader
from django.http import  HttpResponse
from .models import Question

def index(request):
    latest_question_list =  Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)  
# 以下略
```  
このコード、うまくいってはいると思いますが、一つ問題があります。  
本来views.pyは、ページの見栄えを変えるものではないのですが、今のままでは、例えばページのデザインを一新するときに、pythonコードを書き直さなくてはいけません。データの出し入れと表示の部分をそれぞれ分離したほうが良さそうです。  
pollsディレクトリにtemplatesというディレクトリを作成しましょう。djangoはここからテンプレートとなるhtmlファイルを探します。この中に入っているhtmlファイルが、見た目を構成するテンプレートファイルになります。    
ここで一つ注意しなくては行けないのは、polls/templates/index.html ではなく、polls/templates/polls/index.html  となることです。どうやら、同じ名前のテンプレートが別アプリにあったときなど、名前の混同を防ぐためだとか。  
では上述のようにディレクトリを作成し、テンプレートファイルを書いていきましょう。  
# テンプレートファイル  
こんな感じです。HTMLの中にpythonが埋め込まれているような見た目をしています
```html:polls/templates/polls/index.html
<!DOCTYPE html>
<html lang=ja>
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {% if latest_question_list %}
        <ul>
            {% for question in latest_question_list %}
            <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
            {% endfor %}
        </ul>
    {% else %}
        <p>No polls are available</p>
    {% endif %} 
</body>
</html>
```   
pythonの文を書くときは {% %}で囲います。for文やif文の終わりにそれぞれendfor endifという語句がついていますね。  
変数のみを挿入する場合, {{ }}のように二重中括弧でくくります。question.idをURLに加えていますね。  
  
index.htmlくんはまだこのquestion.idが何者か知りません。なので、views.pyから、contextという辞書型のカンペを渡してあげましょう。  
  
```python
# 前略
def index(request):
    # データを用意
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # テンプレートをロード
    template = loader.get_template("polls/index.html")
    # カンペを作成して渡す
    context = {'latest_question_list':latest_question_list}
    return HttpResponse(template.render(context, request))
# 後略
```  
# render()関数  
個々のコードでやっていることは、テンプレートをロードして、コンテキストにデータをいれてviewにわたす、という、djangoではめちゃくちゃ使う動きです。優しいdjango先輩は簡潔に書くためのショートカットを用意してくれています。せかっくなので使ってあげましょう。  

```python
from django.shortcut import render
# 中略
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # ショートカットを利用
    context = {'latest_question_list':latest_question_list}
    return render(request, "polls/index.html")
```  
index以外のページはとりあえずこのままで行くので、
```python
from Django.urils import HttpResponse
```
は残しておきます。  


# 404 link is dead  
![img_1.png](images%2Fimg_1.png)
  
detailのページを編集しましょう。ここは質問のビューを表示するためのものです。ユーザーが正しくurlを打ってくれればいいのですが、かならずそうしてくれるとも限りません。間違ったquestion_idを入力された場合にしっかりとエラーを返して上げましょう、いきなりdjangoのエラーページが出てもユーザーさん困っちゃいますもんね。views.pyを編集していきましょう。  
python初心者の場合はまだあまり馴染みが無いかもしれない try exceptの例外処理を使っています。
```python:polls/views.py

```