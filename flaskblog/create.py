from linebot.models import(
    RichMenuArea, RichMenuBounds, PostbackAction, RichMenuSize, URIAction,
    RichMenu, RichMenuSize, ImagemapSendMessage, BaseSize, MessageImagemapAction, 
    ImagemapArea, BubbleContainer, CarouselContainer, BoxComponent, TextComponent, ImageComponent,
    SpacerComponent, ButtonComponent, SeparatorComponent, URIImagemapAction, TemplateSendMessage, ConfirmTemplate,
    MessageAction, ButtonsTemplate,  DatetimePickerAction, FillerComponent
    )

from flask import request
from flaskblog.formatting import *
from flaskblog.models import *
from datetime import date
from datetime import timedelta
from flaskblog import db
from flaskblog.models import *

def nata_menu():
    rich_event=RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=2500, height=900),
                action=PostbackAction(label='event', data='event', text='pesan perlengkapan event')
            )
    rich_keranjang=RichMenuArea(
                bounds=RichMenuBounds(x=0, y=920, width=1242, height=780),
                action=PostbackAction(label='keranjang', data='keranjang', text='lihat keranjang')
            )
    rich_kontak=RichMenuArea(
                bounds=RichMenuBounds(x=1259, y=920, width=1242, height=780),
                action=URIAction(label='kontak', uri='https://www.instagram.com/nataevent/')
            )

    nata_menu = RichMenu(
        size=RichMenuSize(width=2500, height=1686),
        selected=False,
        name="Menu",
        chat_bar_text="Menu", 
        areas=[
            rich_event, 
            rich_keranjang,
            rich_kontak
            ]
    )

    return nata_menu

def nata_map(action_list):
    url = 'https://i.ibb.co/T1ZkZxB/new-event-map.jpg'
    nata_map = ImagemapSendMessage(
        base_url=url,
        alt_text='event_map',
        base_size=BaseSize(height=1040, width=1040),
        actions= nata_map_action(action_list)
    ) 
    return nata_map

def nata_map_action(actionList_pars):
    actions=[
            MessageImagemapAction(
                text='\\'+actionList_pars[0],
                area=ImagemapArea(
                    x=0, y=0, width=342, height=330
                )
            ),
            MessageImagemapAction(
                text='\\'+actionList_pars[1],
                area=ImagemapArea(
                    x=342, y=0, width=342, height=330
                )
            ),
            MessageImagemapAction(
                text='\\'+actionList_pars[2],
                area=ImagemapArea(
                    x=684, y=0, width=342, height=330
                )
            ),
            MessageImagemapAction(
                text='\\'+actionList_pars[3],
                area=ImagemapArea(
                    x=0, y=357, width=342, height=330
                )
            ),
            MessageImagemapAction(
                text='\\'+actionList_pars[4],
                area=ImagemapArea(
                    x=342, y=357, width=342, height=330
                )
            ),
            MessageImagemapAction(
                text='\\'+actionList_pars[5],
                area=ImagemapArea(
                    x=684, y=357, width=342, height=330
                )
            ),
            MessageImagemapAction(
                text='\\'+actionList_pars[6],
                area=ImagemapArea(
                    x=0, y=703, width=342, height=330
                )
            ),
            MessageImagemapAction(
                text='\\'+actionList_pars[7],
                area=ImagemapArea(
                    x=342, y=703, width=342, height=330
                )
            ),
            MessageImagemapAction(
                text='\\'+actionList_pars[8],
                area=ImagemapArea(
                    x=684, y=703, width=342, height=330
                )
            )
        ]
    return actions

def nata_flex_buble(id):
    event_db = Event.query.filter_by(id=id).first()
    tmp_name = event_db.event_name
    tmp_pvdr = event_db.event_pvdr
    tmp_price = 'Rp ' + parse_value(event_db.event_price) + '/ hari'
    tmp_desc = event_db.event_desc
    url = request.url_root + 'static/new_event/'+id+'.png'
    bubble = BubbleContainer(
                direction='ltr',
                hero=ImageComponent(
                    url=url,
                    size='full',
                    aspect_ratio='20:13',
                    aspect_mode='cover'
                ),
                body=BoxComponent(
                    layout='vertical',
                    spacing="sm",
                    contents=[
                        TextComponent(
                            text=tmp_name,
                            size='lg',
                            align='center',
                            weight='bold',
                            wrap=True
                            
                        ),
                        TextComponent(
                            text=tmp_pvdr,
                            size='sm',
                            align='center',
                        ),
                        FillerComponent(),
                        TextComponent(
                            text=tmp_price,
                            flex=0,
                            size='xl',
                            align='center',
                            weight='bold',
                            wrap=True
                        ),
                        FillerComponent(),
                        TextComponent(
                            text=tmp_desc,
                            flex=0,
                            margin='md',
                            size='xxs',
                            align='center',
                            color='#58948A',
                            wrap=True
                        )
                    ]
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=[
                        ButtonComponent(
                            action=PostbackAction(label="Masukan ke Keranjang", data='pesan%' + id, text='pesan ' + tmp_name.lower()),
                            flex=2,
                            style='primary',
                            color='#AAAAAA'
                        )
                    ]
                )
            )

    return bubble

'''
Function danus_receipt_order_box_components
Function ini membentuk 'tabel' menggunakan TextComponent 
Ratio tabel diatur menggunakan attribute flex
total_cart_price menjumlahkan price dari tiap order
Kemudian, total_cart_price diappend ke index terakhir danus_receipt_order_box_components
'''
def nata_receipt(tmp_user):
    tmp_main=generate_main_arr(tmp_user)
    nata_receipt = BubbleContainer(
                direction='ltr',
                header=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text='Keranjang',
                            size='xl',
                            align='start',
                            weight='bold',
                            color='#aaaaaa'
                        )    
                    ]
                ),
                body= BoxComponent(
                    layout='vertical',
                    spacing='md',
                    contents=tmp_main[0]
                    ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='md',
                    contents=[
                        SeparatorComponent(),
                        BoxComponent(
                            layout='horizontal',
                            contents=[
                                TextComponent(
                                    text='Total'
                                ),
                                 TextComponent(
                                    text='Rp ' + parse_value(tmp_main[1]),
                                    align='end'
                                )
                            ]
                        ),
                        SeparatorComponent(),
                        FillerComponent(),
                        FillerComponent(),
                        FillerComponent(),
                        ButtonComponent(
                            action=PostbackAction(label='Batalkan', data='batalkan', text='batalkan pesanan'),
                            style='primary',
                            color='#B0B0B0'
                            ),
                        ButtonComponent(
                            action=PostbackAction(label='Bayar', data='bayar', text='bayar pesanan'),
                            style='primary',
                            color='#8E8D8D'
                            ),         
                        ]
                    )
            )

    return nata_receipt

def generate_main_arr(tmp_user):
    main_arr = []
    total_amount = 0
    events_arr = tmp_user.user_events
    for i in events_arr:
        tmp_event = Event.query.filter_by(id=i[0]).first()
        tmp_price = tmp_event.event_price*int(i[1])
        total_amount += tmp_price
        tmp_box = BoxComponent(
            layout='vertical',
            contents=[
                BoxComponent(
                    layout='baseline',
                    contents=[
                        TextComponent(
                            text='Barang',
                            align='start'
                        ),
                        TextComponent(
                            text='Harga',
                            align='end'
                        )
                    ]
                ),
                BoxComponent(
                    layout='horizontal',
                    contents=[
                        BoxComponent(
                            layout='vertical',
                            contents=[
                                TextComponent(
                                    text='- ' + tmp_event.event_name,
                                    size='xs'
                                    ),
                                TextComponent(
                                    text='- ' + tmp_event.event_pvdr,
                                    size='xs'
                                    ),
                                TextComponent(
                                    text='- Selama ' + i[1] + ' hari',
                                    size='xs'
                                    )
                                ]
                            ),
                        BoxComponent(
                            layout='vertical',
                            contents=[
                                FillerComponent(),
                                TextComponent(
                                    text= 'Rp ' + parse_value(tmp_price),
                                    align='end'
                                    ),
                                FillerComponent()
                                ]
                            )
                        ]
                    ) 
                ]
            )
        main_arr.append(tmp_box) 
    main_arr.append(SpacerComponent())   
    return [main_arr, total_amount]

def dummy_buble():
    dummy_1 = nata_flex_buble('E01')
    dummy_2 = nata_flex_buble('E02')
    dummy_3 = nata_flex_buble('E03')
    dummy_4 = nata_flex_buble('E04')
    dummy_5 = nata_flex_buble('E05')
    dummy_carousel = CarouselContainer(
        contents= [
            dummy_1,
            dummy_2,
            dummy_3,
            dummy_4,
            dummy_5
        ]
    )
    return dummy_carousel

def dummy2_buble():
    dummy_1 = nata_flex_buble('E06')
    dummy_2 = nata_flex_buble('E07')
    dummy_3 = nata_flex_buble('E08')
    dummy_carousel = CarouselContainer(
        contents= [
            dummy_1,
            dummy_2,
            dummy_3
        ]
    )
    return dummy_carousel

def dummy3_buble():
    dummy_1 = nata_flex_buble('E09')
    dummy_2 = nata_flex_buble('E10')
    dummy_3 = nata_flex_buble('E11')
    dummy_carousel = CarouselContainer(
        contents= [
            dummy_1,
            dummy_2,
            dummy_3
        ]
    )
    return dummy_carousel
def dummy4_buble():
    dummy_1 = nata_flex_buble('E12')
    dummy_2 = nata_flex_buble('E13')
    dummy_3 = nata_flex_buble('E14')
    dummy_carousel = CarouselContainer(
        contents= [
            dummy_1,
            dummy_2,
            dummy_3
        ]
    )
    return dummy_carousel
def dummy5_buble():
    dummy_1 = nata_flex_buble('E15')
    dummy_2 = nata_flex_buble('E16')
    dummy_3 = nata_flex_buble('E17')
    dummy_carousel = CarouselContainer(
        contents= [
            dummy_1,
            dummy_2,
            dummy_3
        ]
    )
    return dummy_carousel
def dummy6_buble():
    dummy_1 = nata_flex_buble('E18')
    dummy_2 = nata_flex_buble('E19')
    dummy_3 = nata_flex_buble('E20')
    dummy_carousel = CarouselContainer(
        contents= [
            dummy_1,
            dummy_2,
            dummy_3
        ]
    )
    return dummy_carousel
def dummy7_buble():
    dummy_1 = nata_flex_buble('E21')
    dummy_2 = nata_flex_buble('E22')
    dummy_3 = nata_flex_buble('E23')
    dummy_carousel = CarouselContainer(
        contents= [
            dummy_1,
            dummy_2,
            dummy_3
        ]
    )
    return dummy_carousel
def dummy8_buble():
    dummy_1 = nata_flex_buble('E24')
    dummy_2 = nata_flex_buble('E25')
    dummy_3 = nata_flex_buble('E26')
    dummy_carousel = CarouselContainer(
        contents= [
            dummy_1,
            dummy_2,
            dummy_3
        ]
    )
    return dummy_carousel
def dummy9_buble():
    dummy_1 = nata_flex_buble('E27')
    dummy_2 = nata_flex_buble('E28')
    dummy_3 = nata_flex_buble('E29')
    dummy_carousel = CarouselContainer(
        contents= [
            dummy_1,
            dummy_2,
            dummy_3
        ]
    )
    return dummy_carousel



def datetime_msg():
    tmp_max = date.today() + timedelta(days=30)
    tmp_min = date.today() + timedelta(days=2)
    tmp_max = str(tmp_max)
    tmp_min = str(tmp_min)

    datetime_template_message = TemplateSendMessage(
                                    alt_text='datetime template',
                                    template= ButtonsTemplate(
                                        text="Pesanan akan dikirim pada tanggal " +
                                        "dan waktu yang anda pilih" ,
                                        actions=[
                                            DatetimePickerAction(
                                                label="Pilih Tanggal",
                                                data="date_postback",
                                                mode="date",
                                                initial=tmp_min,
                                                max=tmp_max,
                                                min=tmp_min
                                            )
                                        ]
                                    )
                                )

    return datetime_template_message

def transfer_msg():
    transfer_msg = TemplateSendMessage(
        alt_text='transfer message',
        template= ButtonsTemplate(
                    text='Silahkan pilih metode pembayaran di bawah ini',
                    actions=[
                        PostbackAction(
                            label='Transfer Mandiri',
                            data='transfer_mandiri',
                            display_text='atm Mandiri'
                        ),
                         PostbackAction(
                            label='Transfer BCA',
                            data='transfer_bca',
                            display_text='atm BCA',
                        ),
                        PostbackAction(
                            label='Transfer BNI',
                            data='transfer_bni',
                            display_text='atm BNI'
                        )
                    ]
                ) 
        
    )
    return transfer_msg

# batas 2.0

    # danus_orders = []
    # event_orders = []
    # box_contents = []
    # for order in cart.orders:
    #     if order.danus_flag:
    #         danus_orders.append(order)
    #     else:
    #         event_orders.append(order)
    # if len(danus_orders):
    #     box_contents.append(nata_danus_receipt(danus_orders))
    # if len(event_orders):
    #     box_contents.append(nata_event_receipt(event_orders))
    # receipt = CarouselContainer(contents=box_contents)
    # return receipt

def cancel_button(indicator):
    cancel_button = ButtonComponent(
                        action=PostbackAction(label='Batalkan',
                                            data='confirm_cancel_'+indicator,
                                            text='batalkan pemesanan'),
                        style='secondary',
                        height='sm'
                    )
    return cancel_button

def confirm_button():
    confirm_button = ButtonComponent(
                        action=PostbackAction(label='Konfirmasi',
                                            data='confirm_cart',
                                            text='konfirmasi pemesanan'),
                        style='primary',
                        margin='sm',
                        height='sm'
                    )
    return confirm_button

def footer_component(indicator):
    footer_contents = [cancel_button(indicator), confirm_button()]
    footer_component = BoxComponent(
                        layout='vertical',
                        contents=footer_contents
                    )
    return footer_component

'''
Function danus_receipt_order_box_components
Function ini membentuk 'tabel' menggunakan TextComponent
Ratio tabel diatur menggunakan attribute flex
total_cart_price menjumlahkan price dari tiap order
Kemudian, total_cart_price diappend ke index terakhir danus_receipt_order_box_components
'''
def danus_receipt_order_box_components(orders):
    danus_receipt_order_box_components = []
    total_cart_price = 0
    table_attr_component = BoxComponent(
            layout='horizontal',
            contents=[
                TextComponent(
                    text='No',
                    size='sm',
                    align='start',
                    weight='bold',
                    flex=1
                ),
                TextComponent(
                    text='Nama',
                    size='sm',
                    align='start',
                    weight='bold',
                    flex=5
                ),
                TextComponent(
                    text='Jumlah',
                    size='sm',
                    align='start',
                    weight='bold',
                    flex=2,
                    wrap=True
                ),
                TextComponent(
                    text='Harga',
                    size='sm',
                    align='end',
                    weight='bold',
                    flex=2
                )
            ]
        )
    danus_receipt_order_box_components.append(table_attr_component)
    counter = 0
    for order in orders:
        total_order_price = order.price*order.amount
        str_total_order_price = divide_value_by_thousand(total_order_price)
        total_cart_price += total_order_price
        counter += 1
        box_component = BoxComponent(
            layout='horizontal',
            margin='sm',
            contents=[
                TextComponent(
                    text=str(counter),
                    size='sm',
                    align='start',
                    flex=1
                ),
                TextComponent(
                    text=order.name,
                    size='sm',
                    align='start',
                    flex=5,
                    wrap=True
                ),
                TextComponent(
                    text=str(order.amount),
                    size='sm',
                    align='start',
                    flex=2
                ),
                TextComponent(
                    text=str_total_order_price,
                    size='sm',
                    align='end', 
                    flex=2
                )
            ]
        )
        danus_receipt_order_box_components.append(box_component)
    total_cart_price = divide_value_by_thousand(total_cart_price)
    danus_receipt_order_box_components.append(total_cart_price)
    return danus_receipt_order_box_components

'''
Secara umum sama seperti method sebelumnya, bedanya di method ini
ada lama waktu peminjaman
'''
def event_receipt_order_box_components(orders):
    event_receipt_order_box_components = []
    total_cart_price = 0
    table_attr_component = BoxComponent(
            layout='horizontal',
            contents=[
                TextComponent(
                    text='No',
                    size='sm',
                    weight='bold',
                    flex=1
                ),
                TextComponent(
                    text='Nama',
                    size='sm',
                    align='start',
                    weight='bold',
                    flex=3
                ),
                TextComponent(
                    text='Jumlah',
                    size='sm',
                    align='start',
                    weight='bold',
                    flex=2
                ),
                TextComponent(
                    text='Selama',
                    size='sm',
                    align='end',
                    weight='bold',
                    flex=2,
                    wrap=True
                ),
                TextComponent(
                    text='Harga',
                    size='sm',
                    align='end',
                    weight='bold',
                    flex=2
                )                
            ]
        )
    event_receipt_order_box_components.append(table_attr_component)
    counter = 0
    for order in orders:        
        total_order_price = order.price*order.amount*order.long_lease
        str_total_order_price = divide_value_by_thousand(total_order_price)
        total_cart_price += total_order_price
        counter += 1
        box_component = BoxComponent(
            layout='horizontal',
            margin='sm',
            contents=[
                TextComponent(
                    text=str(counter),
                    size='sm',
                    flex=1
                ),
                TextComponent(
                    text=order.name,
                    size='sm',
                    align='start',
                    flex=4
                ),
                TextComponent(
                    text=str(order.amount),
                    size='sm',
                    align='start',
                    flex=1
                ),
                TextComponent(
                    text=str(order.long_lease)+' hari',
                    size='sm',
                    align='end',
                    flex=2,
                ),
                TextComponent(
                    text=str_total_order_price,
                    size='sm',
                    align='end',
                    flex=2
                )                
            ]
        )
        event_receipt_order_box_components.append(box_component)
    total_cart_price = divide_value_by_thousand(total_cart_price)
    event_receipt_order_box_components.append(total_cart_price)
    return event_receipt_order_box_components

'''
Function nata_danus_receipt
@param cart menerima cart
danus_receipt_order memanggil danus_receipt_order_box_components()
yang tujuannya membentuk BoxComponent dari order-order pada cart secara iteratif
Tiap elemen dari danus_receipt_order berisi BoxComponent, kecuali elemen terakhir
berisi total_price dari order-order para cart
'''
def nata_danus_receipt(orders):
    danus_receipt_order = danus_receipt_order_box_components(orders)
    danus_receipt_order_box = danus_receipt_order[:-1]
    danus_total_cart_price = danus_receipt_order[-1]
    danus_receipt = BubbleContainer(
                direction='ltr',
                header=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text='LIST PEMESANAN DANUS',
                            weight='bold',
                            size='md',
                            margin='md',
                            align='center'
                        ),
                        SeparatorComponent()
                    ]
                    ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        BoxComponent(
                            layout='vertical',
                            contents=danus_receipt_order_box
                        ),
                        BoxComponent(
                            layout='horizontal',
                            margin='sm',
                            contents=[
                                TextComponent(
                                    text='TOTAL',
                                    size='sm',
                                    align='start',
                                    flex=5
                                ),
                                TextComponent(
                                    text=danus_total_cart_price,
                                    size='sm',
                                    align='end',
                                    flex=5
                                )
                            ]
                        )
                    ],
                ),
                footer=footer_component('danus')
            )

    return danus_receipt

'''
Function nata_event_receipt
Secara umum sama seperti nata_danus receipt
'''
def nata_event_receipt(orders):
    event_receipt_order = event_receipt_order_box_components(orders)
    event_receipt_order_box = event_receipt_order[:-1]
    event_total_cart_price = event_receipt_order[-1]
    event_receipt = BubbleContainer(
                direction='ltr',
                header=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(
                            text='LIST PEMESANAN EVENT',
                            weight='bold',
                            size='md',
                            margin='md',
                            align='center'
                        ),
                        SeparatorComponent()
                    ]
                    ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        BoxComponent(
                            layout='vertical',
                            contents=event_receipt_order_box
                        ),
                        BoxComponent(
                            layout='horizontal',
                            margin='sm',
                            contents=[
                                TextComponent(
                                    text='TOTAL',
                                    size='sm',
                                    align='start',
                                    flex=5
                                ),
                                TextComponent(
                                    text=event_total_cart_price,
                                    size='sm',
                                    align='end',
                                    flex=5
                                )
                            ]
                        )
                    ],
                ),
                footer=footer_component('event')
            )

    return event_receipt

def nata_locationMap():
    nata_locationMap = ImagemapSendMessage(
        base_url = "https://i.ibb.co/4jK14T3/location-Map.jpg",
        alt_text = "nata_locationMap",
        base_size=BaseSize(height=700, width=700),
        actions = [
            URIImagemapAction(
                link_uri='line://nv/location',
                area=ImagemapArea(
                    x=0, y=0, width=700, height=700
                )
            )
        ]
    )
    return nata_locationMap

def atm_map(atm_name):
    if atm_name == 'BCA' or atm_name == 'BNI' or atm_name == 'Mandiri':
        atm_map=ImagemapSendMessage(
            base_url='https://i.ibb.co/8jjLt6W/bank-map.jpg',
            alt_text='rekening BCA',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='line://nv/camera/',
                    area=ImagemapArea(
                        x=20, y=753, width=500, height=270
                    )
                ),
                URIImagemapAction(
                    link_uri='line://nv/cameraRoll/single',
                    area=ImagemapArea(
                        x=529, y=753, width=500, height=270
                    )
                )
            ]
        )

    # elif atm_name == 'BNI':
    #     atm_map=ImagemapSendMessage(
    #         base_url='https://i.ibb.co/8jjLt6W/bank-map.jpg',
    #         alt_text='rekening BNI',
    #         base_size=BaseSize(height=1040, width=1040),
    #     )
    # elif atm_name == 'Mandiri':
    #     atm_map=ImagemapSendMessage(
    #         base_url='https://i.ibb.co/8jjLt6W/bank-map.jpg',
    #         alt_text='rekening Mandiri',
    #         base_size=BaseSize(height=1040, width=1040),
    #         actions=[]
    #     )

    return atm_map
