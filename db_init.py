import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('bastion.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE chathistory
        (date text, channel text, user text, msg text)''')
    conn.commit()
    conn.close()
