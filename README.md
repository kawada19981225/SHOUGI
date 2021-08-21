# SHOUGI
Python/Pygameを使って将棋プログラムを作成しました

# 起動画面
<img src= "https://user-images.githubusercontent.com/73467116/130317638-6d2faa29-3179-4c93-ae7e-55fea1a577b9.png" width="500px">
将棋盤や駒台が表示されます。(駒台とは相手から奪った駒を置く場所です。)<br>
左上には現在の操作プレイヤー、右下には「成る」ことが出来る駒が存在するかお知らせします。<br>
(プレイヤーの持ち駒ごとに判定します)

# 操作画面(将棋盤)

<img src= "https://user-images.githubusercontent.com/73467116/130318071-dcc8da91-e19f-44d4-a1f4-9a7e2ed24ef6.png" width="325px">  <img src= "https://user-images.githubusercontent.com/73467116/130318122-21db493d-e494-4048-ba06-3e2705594f7b.png" width="325px">

動かしたい駒を選択すると、あらかじめ駒に設定されている移動可能な方向へ赤丸が表示されます(左図)。 移動したい赤丸を選択すると、駒が選択した座標に新しく生成され、元の場所にあった駒が削除されます(右図)。

# 操作画面(駒台)

<img src= "https://user-images.githubusercontent.com/73467116/130318510-a00f957c-bd17-42b7-8fe1-a93401dc3631.png" width="325px"> <img src= "https://user-images.githubusercontent.com/73467116/130318551-1d9df897-112c-4d5b-9bfd-578c94784e20.png" width="325px">

互いに「歩」を一つずつ取り合っており、Player_2が駒台から「歩」を置こうとしている状況です(上図)。「歩」は既に「歩」が存在する縦のラインには置くことが出来ないので(右図)のように表示されます。「歩」以外の駒は駒がない場所であれば、どこにでも置くことが出来ます。

<img src= "https://user-images.githubusercontent.com/73467116/130318708-10247fe0-43ef-42de-b3bb-b1dd576810c5.png" width="500px">

「歩」を置く場所を選択した結果、選択した座標に新しく駒が生成され、Player_2に紐づけられている駒台の「歩」の数が1減りました。

# 操作画面(成り)

<img src= "https://user-images.githubusercontent.com/73467116/130318852-83de79d6-eb3f-4e97-aa97-a0b83f4cc7e2.png" width="325px">  <img src= "https://user-images.githubusercontent.com/73467116/130318889-11238374-fe18-4a13-a1bc-8f77cdb2f2f1.png" width="325px">

Player_2の操作する「歩」が「成り」の条件である敵陣(上から3列)にたどり着いたことで、成るかどうかの判定が発生します。(左図)
「Yes」を押した場合、「歩」は金将に成ります。Noを押した場合はそのまま続行します。成るかどうかの判定は敵陣に駒が存在している間、その駒を動かす度に発生します。

# 終了条件


<img src= "https://user-images.githubusercontent.com/73467116/130319332-f305fc9e-59fa-41c2-a3de-92035e098e40.png" width="500px">

相手の王を倒すことでゲームが終了します。具体的には、自分または相手の駒台に「王」の駒が入ることで勝利判定を行っています。
