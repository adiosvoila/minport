import sqlite3, datetime
from app.main.config import ssh_key, ssh_port
from app.main.utils.ssh import SshClient

#Macros
CMD_DELETE_USER = 'deluser '


with sqlite3.connect("/home/MGSAPI/app/main/flask_boilerplate_prod.db") as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("select * from MGS_LEASE")
    rows = cur.fetchall()
    
    lease_list = []
    for row in rows:
        lease_dict = { 'node_name': row['node_name'], 'username': row['username'], 'expire_date': row['expire_date'] }
        lease_list.append(lease_dict)

    # Get IP Address List
    cur.execute("select * from MGS_NODE")
    rows = cur.fetchall()

    ip_addr_dict = {}
    for row in rows:
        ip_addr_dict[row['node_name']] = row['ip_addr']

    #Removes not expired account
    now = datetime.datetime.now()

    #Prepare list for remove
    delete_list = []

    for item in lease_list:
        if datetime.datetime.strptime(item['expire_date'], '%Y-%m-%d %H:%M:%S.%f') >  now:
            delete_list.append(item)

    #Delete not expired items
    for item in delete_list:
        lease_list.remove(item)
  
    #Delete expired account
    for item in lease_list:
        
        #delete account
        try:
            client = SshClient()
            client.connect(ip_addr=ip_addr_dict[item['node_name']], username='root',\
                password=ssh_key, port=ssh_port)
            cmd = CMD_DELETE_USER + item['username']
            client.exec_cmd(cmd)
        except Exception as e:
            print(str(e))
            continue
        client.disconnect()
        
        #if success, delete from DB
        cur.execute("select * from MGS_LEASE WHERE node_name=? AND username=?", (item['node_name'],\
            item['username']))
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.execute("DELETE from MGS_LEASE WHERE node_name=? AND username=?", (item['node_name'], \
            item['username']))
        conn.commit()

    cur.close()
