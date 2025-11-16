# pcbの作成手順
1. pcbエディター>ツール>スクリプトコンソール
1. shellで下記で部品を配置
    ```sh
    exec(open(r"<絶対パス>\roba_L_position.py").read())
    ```
1. shellで下記で外形線を描く
    ```sh
    exec(open(r"<絶対パス>\roba_L_outerline.py").read())
    ```
