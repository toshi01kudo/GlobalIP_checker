import requests, os, sys, logging
import logging.handlers
import json
import parameter

def main():
    ##
    ## Logging 設定
    ##
    # 保存先の有無チェック
    if not os.path.isdir(file_path('./log')):
        os.makedirs(file_path('./log'), exist_ok=True)
    # logファイル出力
    create_log(file_path('log/log.txt'))
    logging.info('#=== Start program ===#')
    ipchecker()
    logging.info('#=== Finished program ===#')

def ipchecker():
    # 現在のGlobal IP 取得
    current_globalip = requests.get('http://checkip.amazonaws.com').text
    # 前回のGlobal IP 取得
    with open(file_path('current_globalip.txt'), 'r', encoding="utf-8") as f:
        previous_globalip = f.read()
    # Global IP の変更を確認
    if current_globalip == previous_globalip:
        logging.info('Global IP is unchanged.')
    else:
        logging.info('Global IP is changed.')
        # 新しいGlobal IPへ更新
        with open(file_path('current_globalip.txt'), 'w', encoding="utf-8") as f:
            f.write(current_globalip)
        # LINEで通知
        send_text = 'New Global IP:\n'
        send_text = send_text + current_globalip
        logging.info(send_text)
        send_line_masageapi(send_text)

def send_line_masageapi(notification_message: str) -> None:
    """
    Notificate to LINE
    """
    line_token = parameter.LINE_CHANNEL_ACCESS_TOKEN
    line_group_id = parameter.LINE_MESSAGE_API_GROUP_ID
    line_api_url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {line_token}',
    }
    data = {
        'to': line_group_id,
        'messages': [
            {
                'type': 'text',
                'text': notification_message,
            },
        ],
    }
    requests.post(line_api_url, headers=headers, data=json.dumps(data))

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
