# путь до базы данных (если ее несуществует, то создает новую)
path_database = "database.db"
# путь до папки конфигураций клиентов. По умолчанию: /etc/wireguard/clients/
path_to_conf = ''
# первые три октавы адреса vpn
part_address = '10.200.200.'
# шаблон conf файла клиентов
temp_conf = """
[Interface]
PrivateKey = {private_key}
Address = {address}/24
DNS = 8.8.8.8,8.8.4.4

[Peer]
PublicKey = {pub_key}
Endpoint = 123.123.123.1:1234
AllowedIPs = 0.0.0.0/0,::/0
"""