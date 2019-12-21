import logging
import os
import io
import json
import azure.functions as func

import numpy as np
from PIL import Image
import onnxruntime
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:

    if req.method != 'POST':
        return func.HttpResponse("Bad request", status_code=400)

    # 画像の取得
    post_img = req.get_body()
    in_memory = io.BytesIO(post_img)

    # リサイズと正規化
    ximg = Image.open(in_memory)
    ximg_resize = ximg.resize((224, 224))
    ximg224 = np.array(ximg_resize)
    ximg224 = ximg224 / 255

    # MobileNetに渡す次元は (N x 3 x H x W) である必要があるので、転置します （参考: https://github.com/onnx/models/tree/master/vision/classification/mobilenet）
    x = ximg224.transpose(2, 0, 1)
    x = x[np.newaxis, :, :, :]  # (1, 3, 224, 224) になります
    x = x.astype(np.float32)


    # モデル、ラベル辞書のダウンロード
    try:
        blob_service_client = BlobServiceClient.from_connection_string(os.environ['BLOB_CONNECTION_STRING']) # BLOBサービスとの接続。ConnectionStringは環境変数（ローカルの場合はlocal.setting.json）に格納しています
        container_client = blob_service_client.get_container_client('<your_container>') # コンテナーの指定
        model_blob = container_client.get_blob_client('mobilenetv2-1.0.onnx') # ファイル名の指定
        json_blob = container_client.get_blob_client('imagenet_class_index.json') # ラベル辞書 : https://gist.github.com/PonDad/4dcb4b242b9358e524b4ddecbee385e9

        print("Downloading model and JSON...")
        download_stream_model = model_blob.download_blob()
        download_stream_json = json_blob.download_blob()

    except Exception as e:
        logging.error(e)
        return func.HttpResponse("Download failed.", status_code=503)

    # モデルをONNX Runtimeで読み込み
    model = download_stream_model.readall()
    session = onnxruntime.InferenceSession(model)

    session.get_modelmeta()
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    # 推論
    probs = session.run([output_name], {input_name: x})
    results = np.argsort(-(probs[0][0])) # 推論結果の確率を降順でソート、"高い順のindex"がリストで返ります。

    # インデックスとラベルテキストの対応付け
    labels_dict = download_stream_json.readall() # JSONの読み込み
    labels_dict = json.loads(labels_dict.decode('utf-8'))
    display_results = [labels_dict[i]['ja'] for i in results[:10]] # 上位10件のラベルを抽出

    return func.HttpResponse(json.dumps(display_results, ensure_ascii=False))
