'''
File ini berisi function untuk mempermudah insert Event
Untuk menggunakan file ini, cukup import function runner,
kemudian insert Event dengan format
'[nama event] [harga]' (tanpa tanda kutip)
Jika sudah selesai insert Event, masukkan query exit 
(akan error tapi tidak apa-apa karena Event sudah diinsert di function insert_query)
Karena function ini belum sempurna, jangan lupa untuk 
db.session.commit() setelah selesai insert Event
'''

from flaskblog import db
from flaskblog import Cart, Danus, Event, Order

def insert_query(name, price):
	event = Event(name=name, price=price)
	db.session.add(event)

def runner():
	query = input()
	if query is not 'exit':
		parsed_query = query.split(' ')
		name = (' ').join(parsed_query[:-1])
		price = int(parsed_query[-1])
		insert_query(name, price)
		runner()
	db.session.commit()