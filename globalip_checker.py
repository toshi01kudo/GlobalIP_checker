import requests, os, sys, logging
import logging.handlers
import parameter

def main():
    ##
    ## Logging 設定
    ##
    # 保存先の有無チェック
    if not os.path.isdir('./log'):
        os.makedirs('./log', exist_ok=True)
    # logファイル出力
    create_log(file_path('log/log.txt'))
    logging.info('#=== Start program ===#')
    ipchecker()
    logging.info('#=== Finished program ===#')

def ipchecker():
    # 現在のGlobal IP 取得
    current_globalip = requests.get('http://checkip.amazonaws.com').text
    # 前回のGlobal IP 取得
    with open('current_globalip.txt', 'r', encoding="utf-8") as f:
        previous_globalip = f.read()
    # Global IP の変更を確認
    if current_globalip == previous_globalip:
        logging.info('Global IP is unchanged.')
    else:
        logging.info('Global IP is changed.')
        # 新しいGlobal IPへ更新
        with open('current_globalip.txt', 'w', encoding="utf-8") as f:
            f.write(current_globalip)
        # LINEで通知
        send_text = 'New Global IP:\n'
        send_text = send_text + current_globalip
        logging.info(send_text)
        send_line_notify(send_text)

def send_line_notify(notification_message):
    """
    LINEに通知する
    """
    line_notify_token = parameter.Token_key
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

def file_path(filename):
    # 別のディレクトリで実行した際に、実行ファイルのパスを指定する関数
    return os.path.dirname(__file__) + '/' + filename

def create_log(filename):
    # log ファイルを出力する関数
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # ファイル出力時に log ファイルが無限に増大するのを防ぐ。
    # 10000 Bytes を超えたときバックアップを取り、3個までバックアップを取る。
    rt_file_handler = logging.handlers.RotatingFileHandler(
        filename, 
        encoding='utf-8',
        maxBytes=10000,
        backupCount=3
    )

    # 手動実行時に標準出力にも log を出力する。
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    # 例外も log 出力する。
    sys.excepthook = my_handler

    # logging の設定。file_handler と stream_handler はリストで渡す。
    logging.basicConfig(level=logging.INFO,
        format=' %(asctime)s - %(levelname)s - %(message)s',
        handlers=[stream_handler, rt_file_handler]
    )

def my_handler(type, value, tb):
    # 例外を log 出力するための関数
    logger = logging.getLogger(__name__)
    logger.exception("Uncaught exception: {0}".format(str(value)))

if __name__ == "__main__":
    main()
