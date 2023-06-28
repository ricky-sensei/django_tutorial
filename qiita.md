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
  
