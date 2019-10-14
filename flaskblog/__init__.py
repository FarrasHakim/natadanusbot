from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
from argparse import ArgumentParser

import psycopg2
import requests
import cloudinary
import cloudinary.uploader
import cloudinary.api
import json

from flask import Flask, request, abort, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent,TextMessage,TextSendMessage,
    SourceUser,SourceGroup,SourceRoom,TemplateSendMessage,
    ConfirmTemplate, MessageAction,ButtonsTemplate,ImageCarouselTemplate,
    ImageCarouselColumn,URIAction,PostbackAction,DatetimePickerAction,
    CarouselTemplate,CarouselColumn,PostbackEvent,StickerMessage,
    StickerSendMessage,LocationMessage,LocationSendMessage,ImageMessage,
    VideoMessage,AudioMessage,FileMessage,UnfollowEvent,
    FollowEvent,JoinEvent,LeaveEvent,ImageSendMessage,
    FlexSendMessage,CarouselContainer,QuickReply, QuickReplyButton
)

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# this is app configuration
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# this is cloudinary configuration
cloudinary.config(
    cloud_name='nataevent',
    api_key=os.getenv('CLOUDINARY_KEY'),
    api_secret=os.getenv('CLOUDINARY_SECRET') 
)
db = SQLAlchemy(app)

from flaskblog.models import *
from flaskblog.formatting import *
from flaskblog.create import *

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET')
print(channel_secret)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
print(channel_access_token)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

# this is linebot initiation
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_path = os.path.dirname(__file__)
static_tmp_path = os.path.join(static_path, 'static', 'tmp')

# use this function to create tmp directory
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise
make_static_tmp_dir()

dummy_list = [
    'proyektor','sound_system','microphone',
    'screen_proyektor','amplifier','kamera',
    'kursi_dan_meja','lampu_studio','barang_lain'
    ]
event_map = nata_map(dummy_list)
location_imageMap = nata_locationMap()

headers = { 'Authorization': 'Bearer ' + channel_access_token }

def nata_menu_checker():
    rich_menu_list = line_bot_api.get_rich_menu_list()
    if rich_menu_list: # Jika tidak kosong, menghapus yang lama
        for rich_menu in rich_menu_list:
            line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)
    
        # Menghapus Default Rich Menu
        requests.delete('https://api.line.me/v2/bot/user/all/richmenu', headers=headers)
    
    nata_menu_create() # Setelah dihapus / apabila kosong, membuat baru

def nata_menu_create():
   # Membuat rich menu baru
    rich_menu_to_create = nata_menu()
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    rich_menu_pic_url = os.path.join(static_path, 'static', 'new_rich_menu.jpg')
    with open(rich_menu_pic_url, 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, 'image/jpeg', f)

    # Set rich menu as default
    requests.post('https://api.line.me/v2/bot/user/all/richmenu/'+rich_menu_id, headers=headers)

''' Hanya gunakan fungsi ini apabila hendak membuat rich menu baru sekaligus menghapus yang lama '''
# nata_menu_checker()

@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = (event.message.text).lower()
    nata_id = event.source.user_id
    profile = line_bot_api.get_profile(nata_id)

    if 'profile' in msg:
        if isinstance(event.source, SourceUser):
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='Halo ' + profile.display_name + '!'),
                    TextSendMessage(text='Status message:\n ' + profile.status_message)
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))

    elif 'bye' in msg:
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='sampai jumpa lagi :)'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='sampai jumpa lagi :)'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="obrolan 1:1 tidak bisa di tinggalkan :("))
    
    elif '\\proyektor' == msg:
        dummy_message = FlexSendMessage(alt_text='list dummy_section', contents=dummy_buble())
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='proyektor yang kami sediakan'),
                dummy_message
            ]
        )
    elif '\\sound_system' == msg:
        dummy2_message = FlexSendMessage(alt_text='list dummy_section', contents=dummy2_buble())
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='sound system yang kami sediakan'),
                dummy2_message
            ]
        )
    elif '\\microphone' == msg:
        dummy3_message = FlexSendMessage(alt_text='list dummy_section', contents=dummy3_buble())
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='microphone yang kami sediakan'),
                dummy3_message
            ]
        )
    elif '\\screen_proyektor' == msg:
        dummy4_message = FlexSendMessage(alt_text='list dummy_section', contents=dummy4_buble())
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='screen proyektor yang kami sediakan'),
                dummy4_message
            ]
        )
    elif '\\amplifier' == msg:
        dummy5_message = FlexSendMessage(alt_text='list dummy_section', contents=dummy5_buble())
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='amplifier yang kami sediakan'),
                dummy5_message
            ]
        )
    elif '\\kamera' == msg:
        dummy6_message = FlexSendMessage(alt_text='list dummy_section', contents=dummy6_buble())
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='kamera yang kami sediakan'),
                dummy6_message
            ]
        )
    elif '\\kursi_dan_meja' == msg:
        dummy7_message = FlexSendMessage(alt_text='list dummy_section', contents=dummy7_buble())
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='kursi dan meja yang kami sediakan'),
                dummy7_message
            ]
        )
    elif '\\lampu_studio' == msg:
        dummy8_message = FlexSendMessage(alt_text='list dummy_section', contents=dummy8_buble())
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='lampu studio yang kami sediakan'),
                dummy8_message
            ]
        )
    elif '\\barang_lain' == msg:
        dummy9_message = FlexSendMessage(alt_text='list dummy_section', contents=dummy9_buble())
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='lain-lain...'),
                dummy9_message
            ]
        )
    
    

    elif 'hello' in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="hello " + profile.display_name +'!'))

    elif 'apa kabar' in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="baik"))

    elif 'nata_it' in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='struggle to make me :)'))

    elif '\\nama ' in msg:
        tmp_user = user_generator(nata_id, profile.display_name)
        tmp_user.user_name = msg[6:]
        db.session.commit()
        line_bot_api.reply_message(
            event.reply_token, [
            TextSendMessage(text='silahkan masukan email'),
            TextSendMessage(text='contoh : \\email nata@rocketmail.com ')
            ])

    elif '\\email' in msg:
        tmp_user = user_generator(nata_id, profile.display_name)
        tmp_user.user_email = msg[7:]
        db.session.commit()
        line_bot_api.reply_message(
            event.reply_token,[
                StickerSendMessage(
                    package_id=11538,
                    sticker_id=51626518
                ),
                TextSendMessage(text='silahkan pilih tanggal pengiriman'),
                datetime_msg()
            ]
        )
    
    
    # elif '\\nomor' in msg:
    #     cart_tmp = cart_generator(nata_id, profile.display_name)
    #     cart_tmp.user_number = msg[7:]
    #     db.session.commit()
    #     line_bot_api.reply_message(
    #         event.reply_token, [
    #         TextSendMessage(text='pilih lokasi, silahkan tap gambar dibawah ini'),
    #         location_imageMap
    #         ])

@handler.add(PostbackEvent)
def handle_postback(event):
    nata_id = event.source.user_id
    profile = line_bot_api.get_profile(nata_id)
    if event.postback.data == 'event':
        line_bot_api.reply_message(
            event.reply_token, [
            TextSendMessage(text='silahkan pilih kategori perlengkapan event'),
            event_map])
    
    elif event.postback.data == 'keranjang':
        tmp_user = user_generator(nata_id, profile.display_name)
        if len(tmp_user.user_events) > 0:
             line_bot_api.reply_message(
                event.reply_token, [
                TextSendMessage(text='keranjang kamu'),
                FlexSendMessage(alt_text="keranjang", contents=nata_receipt(tmp_user))
            ])
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='kamu belum pesan apapun'))

    elif 'pesan' in event.postback.data:
        tmp_parse = event.postback.data.split("%")
        tmp_id = tmp_parse[1]

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='untuk berapa lama?',
                quick_reply=QuickReply(
                    items=[
                    QuickReplyButton(
                        action=PostbackAction(label='1 hari', data='tambah%'+tmp_id+'%'+'1', text='untuk 1 hari')),
                    QuickReplyButton(
                        action=PostbackAction(label='2 hari', data='tambah%'+tmp_id+'%'+'2', text='untuk 2 hari')),
                    QuickReplyButton(
                        action=PostbackAction(label='3 hari', data='tambah%'+tmp_id+'%'+'3', text='untuk 3 hari')),
                    QuickReplyButton(
                        action=PostbackAction(label='4 hari', data='tambah%'+tmp_id+'%'+'4', text='untuk 4 hari')),
                    QuickReplyButton(
                        action=PostbackAction(label='5 hari', data='tambah%'+tmp_id+'%'+'5', text='untuk 5 hari')),
                    QuickReplyButton(
                        action=PostbackAction(label='6 hari', data='tambah%'+tmp_id+'%'+'6', text='untuk 6 hari')),
                    QuickReplyButton(
                        action=PostbackAction(label='1 minggu', data='tambah%'+tmp_id+'%'+'7', text='untuk 1 minggu'))
                ])))

    elif 'tambah' in event.postback.data :
        tmp_user = user_generator(nata_id, profile.display_name)
        tmp_parse = event.postback.data.split("%")
        tmp_id = tmp_parse[1]
        tmp_qnt = tmp_parse[2]

        tmp_arr = []
        for i in tmp_user.user_events:
            tmp_arr.append(i)
        tmp_arr.append([tmp_id, tmp_qnt])
        tmp_user.user_events = tmp_arr
        db.session.commit()

        tmp_event = Event.query.filter_by(id=tmp_id).first()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=(tmp_event.event_name).lower() + ' masuk dalam keranjang'))
    
    elif 'batalkan' == event.postback.data:
        cancel_msg = TemplateSendMessage(
                        alt_text='cancel pesanan',
                        template=ConfirmTemplate(
                            text='Batalkan pesanan?',
                            actions=[
                                PostbackAction(
                                    label='Ya',
                                    data='flush'
                                ),
                                PostbackAction(
                                    label='Tidak',
                                    data='not_canceled',
                                )
                            ]
                        )
                    )
        line_bot_api.reply_message(
            event.reply_token, cancel_msg
        )
    
    elif 'flush' == event.postback.data:
        tmp_user = user_generator(nata_id, profile.display_name)
        tmp_user.user_events = []
        db.session.commit()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='pesanan dibatalkan')
        )

    elif 'not_canceled' == event.postback.data:
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text='tidak jadi nata batalkan')
        )

    elif 'bayar' == event.postback.data:
        line_bot_api.reply_message(
            event.reply_token, 
            [
                TextSendMessage(text=
                    'pesanan Nata konfirmasi, silahkan masukan nama'),
                TextSendMessage(text=
                    'contoh : \\nama Azhar Difa')
            ]
        )

    elif event.postback.data == 'date_postback':
        tmp_user = user_generator(nata_id, profile.display_name)
        customer_date = event.postback.params['date']
        tmp_user.user_date = customer_date
        db.session.commit()
        line_bot_api.reply_message(
            event.reply_token,[
                TextSendMessage(text='sipp, satu langkah terakhir nih untuk konfirmasi pesanan kamu'),
                transfer_msg()
            ]
        )

    elif event.postback.data == 'transfer_bca':
        line_bot_api.reply_message(
            event.reply_token,[
                TextSendMessage(text='kirim bukti transfer ke-nomor rekening dibawah ini'),
                atm_map('BCA')
            ]
        )
    elif event.postback.data == 'transfer_bni':
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='kirim bukti transfer ke-nomor rekening dibawah ini'),
                atm_map('BNI')
            ]
        )
    elif event.postback.data == 'transfer_mandiri':
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='kirim bukti transfer ke-nomor rekening dibawah ini'),
                atm_map('Mandiri')
            ]
        )

# batas 2.0

    elif 'clear_cart_danus' in event.postback.data:        
        cart_tmp = Cart.query.filter_by(id=str(nata_id)).first()
        for order in cart_tmp.orders:
            if order.danus_flag:
                db.session.delete(order)
        db.session.commit()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='pesanan Nata batalkan'))

    elif 'clear_cart_event' in event.postback.data:
        cart_tmp = Cart.query.filter_by(id=str(nata_id)).first()
        for order in cart_tmp.orders:
            if order.event_flag:
                db.session.delete(order)
        db.session.commit()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='pesanan Nata batalkan'))

    elif 'confirm_cart' in event.postback.data:
        line_bot_api.reply_message(
            event.reply_token, [
            TextSendMessage(text=
            'pesanan Nata konfirmasi, silahkan masukan nama'),
            TextSendMessage(text=
            'contoh : \\nama Nata purnomo')
            ])
            

    elif 'confirm_cancel_danus' in event.postback.data:
        line_bot_api.reply_message(
            event.reply_token, confirm_cancel('danus'))

    elif 'confirm_cancel_event' in event.postback.data:
        line_bot_api.reply_message(
            event.reply_token, confirm_cancel('event'))

      

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    nata_id = event.source.user_id
    profile = line_bot_api.get_profile(nata_id)
    tmp_user = user_generator(nata_id, profile.display_name)
    cart_tmp.user_location = event.message.address
    line_bot_api.reply_message(
        event.reply_token,[
        StickerSendMessage(
            package_id=11538,
            sticker_id=51626518
            ),
        TextSendMessage(text='silahkan pilih tanggal pengiriman'),
        location_msg()
        ])

@handler.add(MessageEvent, message=(ImageMessage))
def last_handler(event):
    line_bot_api.reply_message(
        event.reply_token,[
            TextSendMessage(text='Pesanan kamu sudah di konfirmasi dan akan segera kami proses'),
            TextSendMessage(text='kamu akan mendapat konfirmasi maksimal 1x24 jam dari email yang kamu cantumkan'),
            StickerSendMessage(
                package_id=11537,
                sticker_id=52002759
            )
        ]
    )

    ext='jpg'
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name
    
    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    cloudinary.uploader.upload(request.host_url + os.path.join('static', 'tmp', dist_name), public_id=dist_name[4:])
    search_ord = 'public_id=' + dist_name[4:]
    search_cloud = cloudinary.Search().expression(search_ord).execute()
    print(search_cloud)
    json_tmp = json.dumps(search_cloud)
    print(json_tmp)
    json_tmp1 = json_tmp.split(",")
    print(json_tmp1)
    json_tmp2 = json_tmp1[18]
    print(json_tmp2)
    json_tmp3 = json_tmp2[16:-1]
    print(json_tmp3)

    # print(json_response)
    # print(json_response['resources'][0])
    
    # resources = json_response['resources'][0]

    nata_id = event.source.user_id
    profile = line_bot_api.get_profile(nata_id)
    tmp_user = user_generator(nata_id, profile.display_name)
    tmp_arr = []
    for i in tmp_user.user_events:
        tmp_arr.append(i)
    new_cart = cart(
        cart_id=str(nata_id), 
        cart_name=tmp_user.user_name, 
        cart_email=tmp_user.user_email,
        cart_date=tmp_user.user_date,
        cart_events=tmp_arr,
        cart_image_link=json_tmp3
        )
    
    tmp_user.user_name = ""
    tmp_user.user_email = ""
    tmp_user.user_date = ""
    tmp_user.user_events = []
    tmp_user.cart_image_link = ""

    db.session.add(new_cart)
    db.session.commit()
    
    