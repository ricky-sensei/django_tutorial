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
    return render(request, "polls/index.html", context)
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
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question":question})
```  

おそらく、このポエムを読んで頂いている方はウェブアプリ作成が初めてな方が多いと思うので、「404」とは？ってなる方もいなくはないと思います。HTTPステータスコードというのですが、ウェブサイトを見ているとたまに404などの数字がでてくると思います、これはその見ているサイトのいかがわしさを表す数字ではなく、ウェブサイトにリクエストを送った結果を表しています。  
リクエストされたURLが存在しない、あるいは指定の仕方が間違っていたときに、「え、誰？」って感じで返されるコードです。  
HTTPステータスコードについては、漫画でめちゃくちゃわかりやすく説明されている本があり、めちゃくちゃオススメです。

https://llminatoll.booth.pm/items/1036373

  
この404エラーに対しても、django先輩がniceでcoolなショートカットを用意してくれています。  
  
```python:views.py
# (get_object_or_404を追加)
from django.shortcuts import get_object_or_404, render

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question":question})

```  
# テンプレートを使う  
detailのビューに戻って、テンプレートを使って、質問文に対する選択肢を書き出してみましょう。
```python
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```  
for文のところをちょっと見てみましょう。ほとんどpythonコードと同じですがquestion.choice_set.all()と本来するところallのカッコがありません。pythonコードとtenplateのちょっとした違いがありそうですが、まずはdjangoの構造を理解することを優先していいかなと思うので、ここでは飛ばします。気になる方はテンプレートガイドなどをみて見るといいかなと思います
。  
# URLを柔軟にする
チュートリアル先輩は、どうやらtemplates/polls/index.htmlの書き方に激おこな様子。「ハードコード」されているのが良くないようで。  
ハードコードとは、柔軟性のない、変更がめんどくさい感じの書き方のことで、すごく雑に説明すると以下のようなコードです  
```python
print("今日の天気は晴れです")
```
これをソフトコードにしてみましょう  
```python
weather = "晴れ"
print("今日の天気は"+ weather)
```
こうすることで、あとでやっぱり雨だったら、weatherを変更すればいいだけで、簡単に変更できるようになりますね。  
index.htmlを確認してみると
```html
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
```  
となっています。ここのページで質問をクリックすると,polls/{{question_id}}のページ、つまりdetailに飛べるように<a>タグが貼られていますが、ココをソフトコードにしていきましょう。 
```html
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```
url ～ とかくだけで、なぜここのurlが/polls/{{ question.id }}/ だってわかるんでしょうか。秘密はurl.pyの中にあります。見てみましょう  
```python
path("<int:question_id>/", views.detail, name="detail"),
```  
path関数の最後のname引数で、テンプレートの{% url %}タグで使える名前を設定していたんですね。これで、たとえばdetailページの指定の仕方を変更したいときは、このpath関数のみを変更すればよくなりましたね。  
  
  
# アプリが複数あるときは  
今回のプロジェクトはpollsアプリだけですが、実際に制作するプロジェクトではもしかしたら2個3個、10個20個のアプリを作成するかもしれません。その場合、例えば先程のように{%url%}タグで、どのビューに対して、どのURLを作成すればいいか。それを解決する方法があります。  
先程はdetailという名前をurlpatternsから探していましたが、「pollsアプリの」detailを探したい！ということですね。  
やりかたは簡単。まずはurl.pyに、app_name変数を加えましょう。  
```python:urls.py
 # (ココを追加)
app_name = "polls"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/result/", views.result, name="result"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```  
そして、index.htmlで、 「detail」とだけ指定していたところを、「polls:detail」に変更します。  
```html
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```  

このようにして、django先輩は、大規模なウェブサイトを作るのに大変便利な機能を持っています。先輩かっこいい！  

ということで、チュートリアル3の内容でした。だんだん複雑になってきて、django先輩の言ってることもよく分からなくなってきたと思いますが、なるべくわかりやすく言い換えて書いていきますので、よろしくお願いします。  
では、その④に続きます。