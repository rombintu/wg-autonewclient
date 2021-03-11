import sqlite3
import sys
import os

from config import *
from datetime import date

# FUNCTIONS
def create_conf(name, address):
    os.system(f"wg genkey | sudo tee {path_to_conf}{name}_private.key | wg pubkey | sudo tee {path_to_conf}{name}_public.key")
    private_key = open(f"{path_to_conf}{name}_private.key", 'r').read()
    pub_key = open(f"{path_to_conf}{name}_public.key", 'r').read()
    with open(f"{path_to_conf}{name}.conf", 'w') as conf_file:
        conf_file.write(temp_conf.format(private_key=private_key, address=address, pub_key=pub_key))
    
    try:
        os.system(f"qrencode -t ansiutf8 < {path_to_conf}{name}.conf")
    except:
        print("Done.")

def new_client(name, end_address):
    db = sqlite3.connect(path_database)
    sql = db.cursor()
    today = date.today()
    full_address = part_address + end_address
    create_conf(name, full_address)
    script = f"""INSERT INTO clients (name, address, date_add)
                            VALUES (?, ?, ?)"""
    sql.execute(script, (name, full_address, today, ))
    db.commit()
    db.close()

def list_clients():
    db = sqlite3.connect(path_database)
    sql = db.cursor()
    script = "SELECT name, address FROM clients"
    sql.execute(script)
    data = sql.fetchall()
    for client in data:
        print(f"{client[0]} --> {client[1]}")
    db.close()

def main():
    if sys.argv[1] == '-a':
        list_clients()
    elif sys.argv[1] == '-h':
        print("Введите имя клиента, затем адрес, -a ключ покажет всех клиентов")
        print("Пример: python3 main.py test 100")
        print("Будет создан клиент test, test.conf, ключи и адрес 10.200.200.100")
    else:
        # try:
        adrr = sys.argv[2]
        if 0 <= int(adrr) < 255:
            new_client(sys.argv[1], adrr)
        else:
            print("Неверный адрес, попробуйте ключ -h для помощи")
        # except Exception as e:
        #     print(e)
        #     print("Скорее всего этот адрес или имя уже заняты")

# MAIN
if __name__ == "__main__":
    main()


