[前回]()の続きですが、チュートリアルとはちょっと順番を変えてやっていきます。　　
　　
Djangoには、デフォルトで管理者用のインターフェースが用意されています。データベースに直接変更を加えたりするのに便利な機能です。  
  
では最初に、adminとしてログインするためのユーザーを作成しましょう。こういう系のお願いことが誰にお願いするんでしたっけ。  
  
```
python manage.py createsuperuser
```
そう、manage.py先輩でしたね。  
ここでユーザーのemailアドレスやユーザー名、パスワードなどを入力していきます。（こういう勉強用に急に作ったパスワードとかって忘れがちなので、ほんとはよくないですが、.gitignoreとかで退避してパスワード用のファイルを作るのがおすすめ）  
Superuser created successfully.  
と出たらユーザー作成成功です。  
  
# adminサイトを見てみよう  
mysite/urls.pyを見返してください。作成したpollsのurlパターンのほかに、デフォルトでadminというurlが書いてあります。  
では、書いてある通り、runserverして、
http://127.0.0.1:8000/admin  
にアクセスしてみましょう。ログイン画面が出てくるので、先ほど作成したユーザー情報を入力しましょう。
  
![img.png](images%2Fimg.png)
  
ログインボタンを押すと、管理画面が表示されます。  
![img_1.png](images%2Fimg_1.png)  
  
# pollsアプリを編集してみよう  
管理画面を見ても。pollsアプリを編集できそうなボタンが見つかりません。それができるようにするには、pollsの中のadmin.pyに対して、「Questionモデルをadminで編集したいよ」ということを伝えてあげる必要がありますので、admin.pyを編集していきます。  

```python:polls/admin.py
from django.contrib import admin

# quiestionモデルをインポート
from .models import Question

# モデルをadmin管理画面に登録
admin.site.register(Question)
```  

すると、pollsアプリのquestionモデルが表示されているはずです。  
![img_2.png](images%2Fimg_2.png)  
  
当然といえば当然なんですが、中は空っぽです。  ![img_3.png](images%2Fimg_3.png)  
  
この画面から編集・追加もできるのですが、先にPYTHONコンソールから追加する方法を紹介します。チュートリアルの **apiで遊んでみる** のところに戻ります。  
  
# Django Database APIで、コンソールからモデルを操作  
チュートリアルでいきなり「遊ぶ」とかっていわれてもなんのこっちゃ？？ってなりません？ここでは、前回作ったQuestionモデルとChoiceモデルにいろんあデータを追加・変更を行うことをさしています。  
では早速コンソールに入って行きましょう。django内部の環境変数にアクセスするためには、以下のようにしてコンソールに入ります。  
```
python manage.py shell
```  
このページを読んでいただいている方の中には、コンソールでpythonを打つことに慣れていない方も多いと思うので、読みながらご自分で打ってみて、一行づつ見比べてみるのがおすすめです。  

まず、pollsアプリから、これから操作する予定のモデルをインポートしましょう。また、questionクラスには question_text と pub_date というプロパティがあったのを思い出してください。pub_date用に、timezoneをインポートします。
```python
from polls.models import Choice, Question
from django.urils import timezone
```  
まだなんの質問文も用意していないので、↓のように打つと、こんな感じで出力されます。  
```python
Question.objects.all()
# <QuerySet []>
```  
では、最初の質問文と時間を登録していきましょう。
キーワード引数で各データを登録した後に、sava() メソッドを明示的に実行します。(ここでいう「明示的(explicitly)」は、「自動的にはやってくれないから、手動で、『savaしますよ！』っていうのを示さなあかんよ！」って感じの意味です。対義語としては「暗黙的(implicitly)」というのがあり、こういう系のドキュメントでよく出てくる言葉です)  
```python
q = Question(question_text="新着情報", pub_date=timezone.now())
q.save()
```  
これでデータベースに登録されたので、idが付与されています。確認してみましょう。  
```python
q.id
# 1
```  
それぞれのデータを出力してみましょう。  
```python
q.question_text
# '新着情報'
q.pub_date
# datetime.datetime(2023, 7, 4, 12, 6, 33, 301712, tzinfo=datetime.timezone.utc)
```  
  
### おお、なんかうまく行ってそう  
と思ったところで、次のコードを打ってみましょう。Questionモデルのデータを全て(all)出力しようとしています。  
```python
Question.objects.all()  
# <QuerySet [<Question: Question object (1)>]>
```  
うーん、これだとIDが出力されるだけで、どんなデータだったかちょっと分かりづらい！たのむぜDjango兄さん、ということで、models.pyを編集して、どんなデータだったかちゃんと出力されるようにしたいです。pythonコンソールで  
quit()  
と打って、コンソールを抜け出しましょう。  
問題です。Questionモデル(と、ついでにChoiceモデルを編集するには、どのpythonファイルを編集すればいいでしょう？  
<br />
<br />
<br />
<br />
<br />
<br />
<br />

正解は、polls/models.py !  これがわかれば、なんとなくではあってもdjangoの構造がわかってる証拠です！アヤしい人は、前回までの記事を560000回読んで、ついでに全部にイイねしてください笑  
Questionクラスとchoiceに、__str__(self)というメソッドを追加します。  
```python
from django.db import models


class Question(models.Model):
    # 追加
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    # 追加
    def __str__(self):
        return self.choice_text
```
 
この__str__(self)メソッドですが、pythonコンソールだけでなく、先程作成した管理画面でに表示する情報を決めて、レコード(データ)を判別しやすくする効果があります。  
pythonコンソールから戻ってきたついでに、Django先輩はもう一つ機能を追加したいみたいです。全くもう、しょうがないなぁ  
```python:models.py  

# 追加
import datetime

from django.db import models

# 追加
from django.utils import timezone


class Question(models.Model):
    # 追加
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
```  
何を追加したか、おわかりでしょうか。was_published_recentlyにアクセスがあったときに、python標準のdatetimeモジュールと、djangoのdjango.urils.timezoneモジュールを使って、記事が投稿されたのが一日前の時間より最近の時間か(=一日以内にとうこうされたか)を確認する機能です。  
ではでは、pythonコンソールに戻っていろいろ打ってみましょう。まずは先程のコードの出力がどうなっているか確認します。  
```python
>>>from polls.models import Choice, Question
>>>Question.objects.all()
# 新着情報
```  
OK！models.pyでquestion_textが返されるように書いたので、うまく行ってます！管理画面でどうなってるか気になるところですが、せっかくpythonコンソールにいるので、いろいろAPIで「遊んで」みましょう！  
DjangoのデータベースAPIは、そのメソッドとキーワード引数の組み合わせによって、様々な形の出力を得ることができます。 その内いくつかは、もともとのキーワード引数(question_text, pub_date)に**ダブルアンダースコア(__)**をつけたものです。

IDによるフィルタリング
```python
>>> Question.objects.filter(id=1) 
<QuerySet [<Question: 新着情報>]>

``` 
「新着」という文字で始まるquestion_textを検索  
question_textに、__startswithをつけます
```python
>>> Question.objects.filter(question_text__startswith="新着")       
<QuerySet [<Question: 新着情報>]>

```  
pub_date__yearをつかって、今年投稿されたものを表示してみましょう 
```python
>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)
<Question: 新着情報>

```  
ところで、存在しないIDでフィルタリングするとどうなるでしょう？ものは試しです。  
```python
>>>Question.objects.get(id=2)
# polls.models.Question.DoesNotExist: Question matching query does not exist.

```  
ですよね～  
<br />
---
ここからはちょっとだけSQLの知識が有るとわかりやすいです。「SQLなんて全く触ったことないぜ！」ていう方は、youtubeとかでSQL講座みたいなのをチラ見しておくといいかも！  
    
データベースでは主キー(=プライマリキー)というのがあります。データベースのレコードを識別するための、重複しないデータが入ったカラムのことです。
たとえば、社員氏名と部署名、社員番号が書かれたテーブルがあるとします。このうち、絶対に重複しないのは社員番号ですよね。同姓同名のひとがいるかもしれませんし。この場合、社員番号が主キーとなります。  
今回の場合は、自動生成されるIDが主キーとなっていますが、常にID=主キーとは限らないので、注意が必要です。  
以下のコードを打ってみましょう。引数のpkはペナルティーキック、ではなくPrimary Keyの略です。  
```python
>>> Question.objects.get(pk=1) 
<Question: 新着情報>
```  
では、いままでQuestionモデルしか操作してこなかったので、Choiceモデルにもデータを挿入していきましょう。  
質問に対する選択肢(Choice)を作成しているので、先程pk=1と指定して出力された質問に対し、その質問に対する複数の選択肢を用意していきます。  
まず、先程出力された内容("新着情報")を、変数に格納します。  
```python
q = Question.objects.get(pk=1)
```  
ここで、これから作る予定の choice_set というオブジェクトの中身を表示してみます。何を言っているか分からねえと思うが、おれも何をしているのかわからねえ！だってオブジェクトがないんだから！(あ、ちなみにポルナレフでした)  
```python
q.choice_set.all()
# <QuerySet []>
```  
エラーじゃなくて、[]が返ってくるのがミソです。  
  
ここで、models.pyを見返してみましょう。Choiceモデルはどんな感じになってたでしょうか。  
```python:models.py
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
```  
プロパティを見てみると  
・question: Questionモデルの外部キー
・choice_text: 文字列
・votes: 整数  
となっています。
  
では、choice_setオブジェクトの中身をつくっていきましょう。今回は選択肢を作るので、Choiceモデルのquestion, choice_text, モデルのなかみを作るには、SQLを発行する必要があり、カラムを作成するにはcreate文を発行します。Djangoでcreate文はこのようにして書くことができます。   
```python
q.choice_set.create(choice_text="まあまあ", votes=0) 
q.choice_set.create(choice_text="サイコー", votes=0) 
q.choice_set.create(choice_text="ハックしてるぜ", votes=0)
```  
※チュートリアルその1では質問が「what's new(最新情報)」となっていたのが、その2では「what's up(元気？)」になってます。しかも、choiceのふたつめで,whats upにたいして "the sky"とかっていうアメリカンジョークをいれてます。まったく、こういうわかりにくいことやめてほしいもんです。  
それはいいとして、3つの選択肢が入ったので、早速表示してみましょう。  
```python
>>> q.choice_set.all()
<QuerySet [<Choice: まあまあ>, <Choice: サイコー>, <Choice: ハックしてるぜ>]>
>>> q.choice_set.count()
3
```  
DjangoのAPIは自動的にリレーションに従ってくれます。そして、引数にダブルアンダースコア(__)をつけて各モデルのプロパティやメソッドにアクセスできるので、こんなこともできます。  
```python
# 今年投稿されたものだけフィルタリング  
>>> Choice.objects.filter(question__pub_date__year=current_year)  

# 「ハック」ではじまるchoice_textを削除
>>> c = q.choice_set.filter(choice_text__startswith="ハック")
>>> c
<QuerySet [<Choice: ハックしてるぜ>]>
>>> c.delete()
(1, {'polls.Choice': 1})
>>> q.choice_set.all()  
<QuerySet [<Choice: まあまあ>, <Choice: サイコー>]>

```  

# 管理画面を確認してみよう  
せっかくデータも用意できたので、管理画面で確認してみましょう.  
※せっかくなので、質問文を「元気？」と変えておきます。

![img_4.png](images%2Fimg_4.png)  

  
---  
今回はここまで。次はチュートリアルその3に入ります。  
ではでは！