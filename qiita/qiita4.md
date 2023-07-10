Djangoチュートリアルも、かなり大詰めにはいってきました。みなさん元気にdjangoしてますでしょうか 
  
![img.png](img.png)  

今回は、前回出てきたテンプレートをゴリゴリ書いていきます。detailページは今のところ選択肢が出ているだけですが、ここから選択肢を選んで投票できるように、投票フォームをつくっていきます。 

テンプレートを書く前に、プログラミング&HTMLコーディング初心者の方向けに、formタグの基本構造をおさらいしておきます。テンプレートを入れると見た目がごちゃごちゃしてしまうので。慣れている方も一旦おさらいしましょう。  
```html
<form action="送信先のURL" method="get/post">
    <div>
        名前 <input type="text" name="name">
    </div>
    <div>
        メールアドレス <input type="text" name="email">
    </div>
    <div>
        問い合わせ内容 
    </div>
    <input type="button" value="送信">
</form>
```
<p class="codepen" data-height="300" data-default-tab="html" data-slug-hash="VwVrmOW" data-user="ricky-sensei" style="height: 300px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; border: 2px solid; margin: 1em 0; padding: 1em;">
  <span>See the Pen <a href="https://codepen.io/ricky-sensei/pen/VwVrmOW">
  Untitled</a> by ricky-sensei (<a href="https://codepen.io/ricky-sensei">@ricky-sensei</a>)
  on <a href="https://codepen.io">CodePen</a>.</span>
</p>
<script async src="https://cpwebassets.codepen.io/assets/embed/ei.js"></script>    

formタグのmethodプロパティを見てみましょう。
## getとpost
クライアントからサーバーにリクエストをする場合の、HTTPメソッドです。
### get:サーバーから情報ちょうだい！  
サーバーから単に情報をもらうだけなのがgetメソッド  
### post:サーバー側に情報をあげる！  
今回のようにformから情報をサーバーに渡し、それをDBに登録したりする場合に使います。他にもブログ記事投稿やユーザーの追加などで使います。  

これを踏まえた上で、detail.htmlを編集していきましょう。  
```html:polls/templates/polls/detail.html

```







