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
```python

```
