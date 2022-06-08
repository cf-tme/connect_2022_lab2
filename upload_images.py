from email.mime import base
import requests
import json


#DO NOT  CHANGE this token will expire May 14th, 2022
images_token = "HBLM44C_QELdwRGKxhCXRYy23PxfQEp0vuAYAGnl"
images_account_id = "d6850012d250c1600028b55d1d879b16"

#CHANGE these are your value from your workers environment
kv_id = "ENTER YOU WORKERS KV NAMESPACE ID"
kv_account_id = "ENTER YOUR CLOUDFLARE ACCOUNT ID"
kv_token ="ENTER YOUR API TOKEN"


base_url = "api.cloudflare.com/client/v4"

#array of all images to upload
images=["gallery-images/cat1.jpeg",
        "gallery-images/cat2.jpeg",
        "gallery-images/cat3.jpeg",
        "gallery-images/pup1.jpeg",
        "gallery-images/pup2.jpeg",
        "gallery-images/pup3.jpeg"]

for image in images :
#upload the images to cloudflare
    img_upload_url = "https://{}/accounts/{}/images/v1".format(base_url,images_account_id)
    headers = {"Authorization" : "Bearer {}".format(images_token)}
    img = open(image, 'rb')
    files = {"file": img}
    r = requests.post(img_upload_url,headers=headers, files=files)
    img_details = r.json()

    img_id = img_details["result"]["id"]
    img_name = img_details["result"]["filename"]
    #grab the first variant as url
    img_url = img_details["result"]["variants"][0]
    img_time = img_details["result"]["uploaded"]

    #now we will build the data to insert into workers KV! and push the information - this data will be read out by our web application and be presented on our Gallery page.

    kv_key = "image:uploaded:{}".format(img_time)
    kv_metadata = {
                "id": img_id,
                "previewURLBase": img_url,
                "name": img_name,
                "alt": "uploaded-via-lab",
                "uploaded": img_time,
                "isPrivate": False
                }

    kv_url = "https://{}/accounts/{}/storage/kv/namespaces/{}/values/{}".format(base_url,kv_account_id,kv_id,kv_key)
    kv_headers = {"Authorization" : "Bearer {}".format(kv_token)}

    payload = {"value":'"Values stored in metadata"',
                "metadata":json.dumps(kv_metadata)}

    r_kv = requests.put(kv_url,headers=kv_headers, files=payload)
    print ("uploaded image {} and added KV metadata with status {}\n".format(image,r_kv.json()["success"]))

