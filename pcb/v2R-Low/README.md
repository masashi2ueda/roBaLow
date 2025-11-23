## 基板の改修
1. proを開いて、設定→フットプリントライブラリ→プロジェクト固有→roBaのパスをroBaLow\pcb\_kicad_footprintsにする
1. 右上のフットプリントを割り当て→全てのスイッチを選択ChocV2_Hotswap:Choc_v2_Hotswap_1uをクリック
1. 

## pcbの作成手順
1. pcbエディター>ツール>スクリプトコンソール
1. shellで下記で部品を配置
    ```sh
    exec(open(r"<絶対パス>\roba_L_position.py").read())
    ```
1. shellで下記で外形線を描く
    ```sh
    exec(open(r"<絶対パス>\roba_L_outerline.py").read())
    ```
### 自動配線
1. KiCad PCB → ファイル → エクスポート → Specctra DSN
1. https://github.com/freerouting/freerouting/releases からFreeRoutingをダウンロード→install→起動→dsnを読み込む
1. キラキラしたアイコンを押下→自動配線
1. ファイル → 名前を付けて保存
1. KiCad PCB → ファイル → インポート → Specctra DSN→保存したsesを読み込む


### 発注
1. kicadのスタート画面→プラグイン&コンテンツ マネージャー→検索窓にJLC→インストールを押下→右下の保留中の変更を適用を押下
1. メニューバー下の最右のfablication toolkitを押下
1. Generate
1. productionの中に.zipがある
1. https://jlcpcb.com/jp/にアクセス、zipをアップロード