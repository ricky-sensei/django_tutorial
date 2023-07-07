とりあえず、[前回]()どんな感じだったかを、runserverして確認しましょう。pollsというアプリを作成したので,urlに/pollsをつけて、「はじいめてのview作成」という文字が出てくればOKです！
※前回最後に２つのurls.pyをいじったので、チュートリアル通りに戻しておきましょう。

うまく表示されているのを確認したら、runserverを打ち込んだターミナルを確認してみましょう。一番最初に、こんな文章があるはず。　　
　　
```
You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
```

「18個の適用されていないマイグレーションがあるよ！こいつらちゃんとマイグレーションしないと『思てたんとちゃう！』ってなるかも！」っていわれてます。　
　　
はて、マイグレーションとは？って感じだと思いますので、その辺の話から始めようと思います。　　
　　
# migration：データベースの変更の「予約」

世の中、流れに合わせてスピーディーに対応することも確かにイイですが、ひと呼吸おいてから実行する報がよかったりすることって、ありますよね。　　
　　
djangoに限らず、多くのアプリケーションでは、「データベース」というもの」を使って、サイト利用者の管理や、表示する情報などを整理しています。「整理」というざっくりとした言葉を使いましたが、その中には  

・新しいユーザーの情報を**保存**したり  
・既存のユーザーの住所などの情報を**修正・変更**したり  
・もう売れてしまった商品のページを**削除**したり　　  

など、いろいろあります。これらを担当してくれるのが、「データベース言語」とか「クエリ言語」とかっていわれるやつで、MySQLとか、PostgreSQLなどいろいろあります。  

pythonには便利なことに、最初からsqlite3というデータベース言語が入っています。が、たとえばウェブサイトの規模が大きくなって来た時に、ほかのデータベース言語に変更する必要が出てきたりすると、結構悩ましい事態になったりすることもあるので。最初は練習・勉強目的ではSQLite３で十分だけど、必要に応じてsettings.pyを変更してね、とチュートリアル先輩が言ってます。　　
　　  

話が少しそれてしまいましたが。こういうデータベースの変更って、アプリの核心の部分の変更だったりするので、pycharmでコードを打って即変更！となると、間違ってデータが削除されてしまったり、いろんな事件が起きてしまうものです、マイグレーションとは、それを防ぐために　**「SQLつかってこういう変更がしたい」というお願い事を、「migrationファイル」というカタチで書き留めておくシステム**のことです。　
  
エラー文の後半のほうを見てみると　　
```
 the migrations for app(s): admin, auth, contenttypes, sessions.
```  
admin, auth, contenttypes, sessionsというアプリのマイグレーションができてない、って書いてあります。ここでいうアプリは前回作ったpollsアプリと同じ扱いです。初期状態で用意されてるアプリは、settings.pyの、INSTALLED＿APPSというリストに書かれています。のちにここにアプリケーションを追加していきます。　　
　　
```python:mysite/settings.py
#　略
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls.apps.PollsConfig',
]
```  
ここで、pollsディレクトリを見てみましょう。自動的に、「migrations」というディレクトリができているはずです。ここが、「こういう変更したいよ！」というマイグレーションの予約を書きためておくディレクトリです。  
　　
---
とりあえず、デフォルトの状態で必要なマイグレーションをしてから、その後でpollsアプリでマイグレーションをしてみましょう。  
  
runserver同様、django に対するコマンドは、manage.py先輩に任せましょう。  
```
python manage.py migrate
```
migrationの動詞形はmigrateです。「移行する」という意味ですが、migrationディレクトリからdjango本体に移行、という感じでしょうか（テキトーこいてます💦）  
  
okokok！という表示が出てると思いますが、なにかマズいことがあるとここでエラーが表示されます。念のため、runserverの時にエラーが消えていることを確認しましょう。  
  
migrateコマンドがやっていることは、settings.pyのINSTALLED_APPを参照しながら、アプリごとに決められたデータベーステーブルを作成する、ということです。  
   
---
# モデルを作ってみよう  
モデルというのを、作成していきましょう
公式のチュートリアル様は,

>モデルは、手持ちのデータに対する唯一無二の決定的なソースです。モデルには自分が格納したいデータにとって必要不可欠なフィー ルドと、そのデータの挙動を収めます。 Django は DRY 則 に従っています。 Django のモデルの目的は、ただ一つの場所でデータモデルを定義し、そこから自動的にデータを取り出すことにあります。
これはマイグレーションを含みます - たとえば、Ruby On Rails と違って、マイグレーションは完全にモデルのファイルから生成されます。マイグレーションは本質的には単なる履歴です。Django はデータベーススキーマをアップデートしながら履歴を進んでいき、現在のモデルに合致させることができます。  

などと意味不明な供述をしており、動機はいまだ不明です。この辺見てdjangoや～めた、ってなる人多いんじゃないでしょうか。  
  
### ここで一旦、Djangoの本質のおはなし  
本来なら前回この話をするべきだったというか、大体の技術書とかウェブサイトは「djangoとは」みたいな話から入ると思いますが、こうして詰まったところで、「Djangoってなんなのよ」というところから見つめ直すのも結構大事です。  
  
# Django=MTVフレームワーク  
webフレームワークはdjango以外にも、いろんな種類があります。Djangoを形容する言葉として、この「MTVフレームワーク」という言葉がよく使われます。それぞれ
- M:model(モデル) → データベースを担当するところ  
- T:template(テンプレート) → HTMLなどの表示を担当するところ  
- V:view(ビュー) → バックエンド(見えない部分)を担当するところ  

から来ていて、この3つの組み合わせでアプリを形成していくのが「MTVフレームワーク」です。  
  
この3つの関係を図にすると、こんな感じになります。  
では、その「モデル」というものを、もう少し掘り下げましょう。  
  
データベースからデータを検索、削除、追加、取得など、何をするにもモデルをつかって行います。それらを担当するのが、プロジェクト内各アプリにある **models.py** です。モデルにはいくつかの特徴というか、ルールがあります。  
- 1つのモデルが1つのテーブルと対応する  
- モデル名は大文字で始める  
- idは自動的についかされる  
   
ここまできても、うーん、という感じだと思います。では、ここでひとつ、polls/models.pyを書いてみましょう。チュートリアル通り、questionとchoiceという、2つのモデルを作ります。  
```python:polls/models.py
from django.db import models

# モデルを作成  
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeFiels("発行日")

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes= models.IntegerField(default=0)
```

こんへんで、モデルの正体を丸裸にしていきましょう！モデルとは、このmodels.pyのクラス、つまり、django.models.Modelのサブクラスのことなんです。これらのクラスは、先のルール通りそれぞれひとつのテーブルを形成します。それぞれのモデルにはプロパティ(クラス変数)があり、それらはテーブルの各フィールドにあたります。  
各フィールドにどんなデータが入るかを、CharFieldやDateTimeFieldで指定しています。例えばQuestionモデルには  
- question_textというCharField型(文字列)のフィールド  
- pub_dateというDateTime型のフィールド  

が含まれています。各フィールドの第一引数では、フィールド名を指定することができます。pub_dateの「発行日」というのがそれですね。
  
ForeignKeyによって、QuestionテーブルとChoiceテーブルのリレーションが構築されています。
CharFieldとかForeignKeyとかっていうのは、SQLの基礎用語なので、全くわからん！ていう方はSQLの基礎を勉強して戻ってくるのもいいですが、とりあえず必要なものだけ調べて先に進んで行きましょう。もう無理！となったら、迷わずSQLに行けばいいんです。  

# モデルを有効化しよう  
モデルを作成したら、早速マイグレーション！と行きたいところですが、まだdjango先輩は、pollsというアプリがあることを知らないので、pollsアプリのmodels.pyと言われてもなんのこっちゃ？となります。なので、アプリケーションを登録してあげる必要があります。  
インストールされたアプリリストの中にpollsを入れてあげましょう。あれ、どこかで聞いたような。  
そう。settings.pyの中のINSTALLED_APPリストですね。このように編集しましょう。  
```python/settings.py
# 略  
INSTALLED_APPS = [
    # ここにpollsアプリを追加
    'polls.apps.PollsConfig',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

```  

### マイグレーションファイルの作成:makemigrations

マイグレーションを行うまでの流れは、こうです。  
- モデルの作成(済)  
- マイグレーションファイルの作成  
- マイグレーション  

2つ目のマイグレーションファイルの作成を担当するのが、**makemigration** コマンドです。とりあえず打ってみましょう。またmanage.py先輩にお願いしましょう。私のよくやるミスで、  
x makemigration
o makemigrations(複数形)  
なので気をつけて。

```
python manage.py makemigrations polls
```  
うまくいくと、こんな表示が出てきます。
```
  polls\migrations\0001_initial.py
    - Create model Question
    - Create model Choice
```  
makemigrationsコマンドを実行すると、アプリのmigrationフォルダに、migrationファイルというのが作成されます、どんなファイルか見に行ってみましょう。0001_initial.pyというファイルがあるはずです。
  
```python:0001_initial.py
# Generated by Django 4.2.2 on 2023-06-29 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='発行日')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question')),
            ],
        ),
    ]

```

ぱっとみただけでも、questionとchoiceっていうモデル作るよ！ていうのがわかると思います。  
  
ではmakemigrationsでさくせいしたマイグレーションを実行していきましょう。  
と、その前に、心優しい公式チュートリアル先輩が、実際にどういうクエリが実行されているのか見ることができるコマンドを紹介してくれているので、やってみましょう。(まだマイグレーションは実行されません)  
```
python manage.py sqlmigrate polls 0001
```
公式ドキュメント先輩が見やすく整形してくれていたので、ターミナルの出力を見てみましょう  
```
BEGIN;
--
-- Create model Question
--
CREATE TABLE "polls_question" (
    "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "question_text" varchar(200) NOT NULL,
    "pub_date" timestamp with time zone NOT NULL
);
--
-- Create model Choice
--
CREATE TABLE "polls_choice" (
    "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "choice_text" varchar(200) NOT NULL,
    "votes" integer NOT NULL,
    "question_id" bigint NOT NULL
);
ALTER TABLE "polls_choice"
  ADD CONSTRAINT "polls_choice_question_id_c5b4b260_fk_polls_question_id"
    FOREIGN KEY ("question_id")
    REFERENCES "polls_question" ("id")
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");

COMMIT;
```

では、実際にマイグレーションを実行しましょう。  
```python
# 追加
from django.shortcut import render, get_object_or404
from django.http import Http404

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question":question})

```  
先程のindexテンプレートのように、polls/templates/polls/に detai.htmlを追加しましょう。  
```html

```