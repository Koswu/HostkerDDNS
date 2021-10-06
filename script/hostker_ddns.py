#!/bin/python3

import os
import json
import requests
import logging

logging.basicConfig(level=logging.INFO)
EMAIL = os.getenv("EMAIL")
assert EMAIL
TOKEN = os.getenv("TOKEN")
assert TOKEN
AUTH_PARAMS = {'email':EMAIL,'token':TOKEN}
DOMAIN = os.getenv('DOMAIN')
assert DOMAIN
HEADER = os.getenv('HEADER')
assert HEADER
TTL = os.getenv('TTL')
assert TTL
EXIST_ID = os.getenv("EXIST_ID") # force change


def get_current_ip():
    res = requests.get("http://whatismyip.akamai.com")
    return res.text

def get_dns_status():
    data = {
            **AUTH_PARAMS,
            'domain':DOMAIN,
    }
    res = requests.post("https://i.hostker.com/api/dnsGetRecords", data=data)
    res = json.loads(res.text)
    assert res['success'] == 1
    return res

def add_record(ip):
    data = {
            **AUTH_PARAMS,
            'domain': DOMAIN,
            'header': HEADER,
            'type': 'A',
            'data': ip,
            'ttl': TTL,
    }
    res = requests.post("https://i.hostker.com/api/dnsAddRecord", data=data)
    res = json.loads(res.text)
    assert res['success'] == 1
    print(res)

def edit_record(record_id, ip):
    data = {
            **AUTH_PARAMS,
            'id': record_id,
            'data': ip,
            'ttl': TTL,
    }
    res = requests.post("https://i.hostker.com/api/dnsEditRecord", data=data)
    res = json.loads(res.text)
    assert res['success'] == 1

def delete_record(record_id):
    data = {
            **AUTH_PARAMS,
            'id': record_id,
    }
    res = requests.post("https://i.hostker.com/api/dnsDeleteRecord", data=data)
    res = json.loads(res.text)
    assert res['success'] == 1

def main():
    now_ip = get_current_ip()
    logging.info(f"current ip is {now_ip}")
    status = get_dns_status()
    records = [record for record in status['records'] if record['header'] == HEADER and record['type'] == 'A']
    if EXIST_ID or records:
        map(lambda x: delete_record(x['id']),records[1:])
        if EXIST_ID or records[0]['data'] != now_ip:
            logging.info("record ip is not same as now_ip, changing")
            edit_record(EXIST_ID or records[0]['id'], now_ip)
        else:
            logging.info("record ip is same as now_ip, skip")
    else:
        logging.info("record is not exists, changeing")
        add_record(now_ip)
    logging.info("DDNS update success")



if __name__ == "__main__":
    main()