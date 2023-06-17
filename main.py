import pyrogram,string
import requests
from pyrogram import Client,filters,enums,types
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from asSQL import Client as cl
import telegraph,random
from telegraph import upload_file
from pyrogram.types import InputMediaPhoto, InputMediaVideo
dbs = cl("reback")
db = dbs['users']
db.create_table()
app = Client("i2",api_id=3895828,api_hash='5229902a14b2512c35688aa152bd9f29',workers=20,bot_token='6086656535:AAFj-pUNTTZK5Cvi5cBw7W-AJMvkhXj_UtY',parse_mode=enums.ParseMode.DEFAULT)

@app.on_message(filters.private & filters.command(['start']))
def start_command(app,message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if db.key_exists(f"user_{user_id}_email"):
        data = db.get(f"user_{user_id}")
        bio = data['bio']
        ids = data['id']
        photos = len(data['data']['photos'])
        texts = len(data['data']['texts'])
        videos = len(data['data']['videos'])
        followers,following =len( data['followers']),len(data['following'])
        p = "عام" if data['private'] == None or data['private'] == False else "خاص"
        info = [
                [InlineKeyboardButton(text=f"رفع فيديو",callback_data=f'up_video-{user_id}'),InlineKeyboardButton(text="رفع نص",callback_data=f'up_text-{user_id}')],
                [InlineKeyboardButton(text="رفع صور",callback_data=f'up_photo-{user_id}')],
                [InlineKeyboardButton(text="تصفح المنشورات ",callback_data="explore"),InlineKeyboardButton(text="بحث عن حساب",callback_data="search")],
                [InlineKeyboardButton(text='الاعدادات',callback_data=f'settings-{user_id}')]
                
                ]
        btns = InlineKeyboardMarkup(info)
        return message.reply(f"<strong>حساب: <code>{ids}</code> ،\n نوع : {p} ،\n المتابعين : {followers} ،\n المُتابعون : {following} ،\n الصور المرفوعة : {photos} ،\n الفيديوهات المرفوعه : {videos} ،\n النصوص : {texts} ، \n البايو : {bio} .</strong>",reply_markup=btns)
    else:
        db.set(f"ask_email_{user_id}",True)
        return message.reply(f"أهلا، الي واضح انو مامعك حساب، هسة ارسل ايميلك علمود نسوي لك حساب (ايميل حقيقي) ..")

@app.on_message(filters.private & filters.video)
def r_vid(app,m):
    btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
    if (m.video) and db.get(f"pending_upload_vid_{m.from_user.id}"):
        if m.video.duration >119:
            return m.reply(f"الفيديو اكبر من دقيقتين !",reply_markup=btns)
        if m.video.ttl_seconds:
            return 
        if db.key_exists(f"user_{m.from_user.id}"):
            caption = None
            inf = db.get(f"user_{m.from_user.id}")
            if m.caption:
                caption = m.caption
                m.download(file_name="videos/1.mp4")
                m.reply("جارِ رفع الفيديو ....")
                link = "https://telegra.ph"+upload_file(f"videos/1.mp4")[0]
                ids = f"{m.from_user.id}_{random.randint(1920,2324)}"
                f_info = {
                    "caption":caption,
                    "id":ids,
                    "type": "video",
                    "by":{
                        "id":m.from_user.id,
                        "name":m.from_user.first_name,
                        "date":str(m.video.date),
                    },
                    "video_info":{
                        "duration":m.video.duration,
                        "likes":[],
                    },
                    "file":{
                        'unique':str(m.video.file_id),
                        "url":link,
                        "id":ids,
                        "size":m.video.file_size,
                    }
                }
                
                inf['data']['videos'].append(f_info)
                db.set(f"user_{m.from_user.id}",inf)
                db.delete(f"pending_upload_vid_{m.from_user.id}")
                m.delete()
                return m.reply(f"تم رفع الفيديو !\n ارسل <code>/video {ids}</code>, لرؤية الفيديو .",reply_markup=btns)
            else:
                caption = m.caption
                m.download(file_name="videos/1.mp4")
                m.reply("جارِ رفع الفيديو ....")
                link = "https://telegra.ph"+upload_file(f"videos/1.mp4")[0]
                ids = f"{m.from_user.id}_{random.randint(1920,2324)}"
                f_info = {
                    "caption":caption,
                    "id":ids,
                    "type": "video",
                    "by":{
                        "id":m.from_user.id,
                        "name":m.from_user.first_name,
                        "date":str(m.video.date),
                    },
                    "video_info":{
                        "duration":m.video.duration,
                        "likes":[],
                    },
                    "file":{
                        'unique':str(m.video.file_id),
                        "url":link,
                        "id":ids,
                        "size":m.video.file_size,
                    }
                }
                
                inf['data']['videos'].append(f_info)
                db.set(f"user_{m.from_user.id}",inf)
                db.delete(f"pending_upload_vid_{m.from_user.id}")
                m.delete()
                return m.reply(f"تم رفع الفيديو !\n ارسل <code>/video {ids}</code>, لرؤية الفيديو .",reply_markup=btns)
@app.on_message(filters.private & filters.photo)
def r_photo(app,m):
    user_id = m.from_user.id
    btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
    if (m.photo) and db.get(f"pending_upload_photo_{user_id}"):
        if m.photo.ttl_seconds:
            return 
        if db.key_exists(f"user_{m.from_user.id}"):
            caption = None
            inf = db.get(f"user_{m.from_user.id}")
            
            if m.caption:
                caption = m.caption
                m.download(file_name="photos/1.jpg")
                m.reply("جارِ رفع الصور....")
                link = "https://telegra.ph"+upload_file(f"photos/1.jpg")[0]
                ids = f"{m.from_user.id}_{random.randint(1920,2324)}"
                f_infoo = {
                    "caption":caption,
                    "id":ids,
                    "type":'photo',
                    "by":{
                        "id":m.from_user.id,
                        "name":m.from_user.first_name,
                        "date":str(m.photo.date),
                    },
                    "photo_info":{
                        "likes":[],
                },
                    "file":{
                            'unique':str(m.photo.file_id),
                            "url":link,
                            "id":ids,
                            "size":m.photo.file_size,
                    }
            }
                
                inf['data']['photos'].append(f_infoo)
                db.set(f"user_{m.from_user.id}",inf)
                db.delete(f"pending_upload_photo_{m.from_user.id}")
                return m.reply(f"تم رفع لصورة!\n ارسل : <code>/photo {ids}</code> ، لرؤية الصورة .",reply_markup=btns)
            else:
                caption = m.caption
                m.download(file_name="photos/1.jpg")
                m.reply("جارِ رفع الصور....")
                link = "https://telegra.ph"+upload_file(f"photos/1.jpg")[0]
                ids = f"{m.from_user.id}_{random.randint(1920,2324)}"
                f_infoo = {
                    "caption":caption,
                    "id":ids,
                    "type":'photo',
                    "by":{
                        "id":m.from_user.id,
                        "name":m.from_user.first_name,
                        "date":str(m.photo.date),
                    },
                    "photo_info":{
                        "likes":[],
                },
                    "file":{
                            'unique':str(m.photo.file_id),
                            "url":link,
                            "id":ids,
                            "size":m.photo.file_size,
                    }
            }
                
                inf['data']['photos'].append(f_infoo)
                db.set(f"user_{m.from_user.id}",inf)
                db.delete(f"pending_upload_photo_{m.from_user.id}")
                return m.reply(f"تم رفع لصورة!\n ارسل : <code>/photo {ids}</code> ، لرؤية الصورة .",reply_markup=btns)
    
                        
@app.on_callback_query()
def rc(app,call):
    
    data = call.data
    if data == "back_main":
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        if db.key_exists(f"user_{user_id}_email"):
            app.delete_messages(call.message.chat.id, call.message.id)
            data = db.get(f"user_{user_id}")
            bio = data['bio']
            ids = data['id']
            photos = len(data['data']['photos'])
            texts = len(data['data']['texts'])
            videos = len(data['data']['videos'])
            followers,following =len( data['followers']),len(data['following'])
            p = "عام" if data['private'] == None or data['private'] == False else "خاص"
            info = [
                [InlineKeyboardButton(text=f"رفع فيديو",callback_data=f'up_video-{user_id}'),InlineKeyboardButton(text="رفع نص",callback_data=f'up_text-{user_id}')],
                [InlineKeyboardButton(text="رفع صور",callback_data=f'up_photo-{user_id}')],
                [InlineKeyboardButton(text="تصفح المنشورات ",callback_data="explore"),InlineKeyboardButton(text="بحث عن حساب",callback_data="search")],
                [InlineKeyboardButton(text='الاعدادات',callback_data=f'settings-{user_id}')]
                
                ]
            btns = InlineKeyboardMarkup(info)
            return app.send_message(chat_id=call.message.chat.id,text=f"<strong>حساب: <code>{ids}</code ،\n نوع : {p} ،\n المتابعين : {followers} ،\n المُتابعون : {following} ،\n الصور المرفوعة : {photos} ،\n الفيديوهات المرفوعه : {videos} ،\n النصوص : {texts} ، \n البايو : {bio} .</strong>",reply_markup=btns)
        else:
            db.set(f"ask_email_{user_id}",True)
            call.edit_message_text(f"أهلا، الي واضح انو مامعك حساب، هسة ارسل ايميلك علمود نسوي لك حساب (ايميل حقيقي) ..")
    if data.startswith("saves-"):
        user_id = data.split("-")[1]
        d = db.get(f"user_{call.from_user.id}_savelist")
        ax = "المحفوظات:\n"
        btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
        if d == None:
            return call.edit_message_text(f"لايوجد شيء",reply_markup=btns)
        else:
            for i in d['data']:
                if i['media']:
                    ax+=f"- <code>/get {i['id']}</code> . | ميديا\n"
                else:
                    ax+=f"- <code>/get {i['id']}</code>. | نص\n"
            call.edit_message_text(ax,reply_markup=btns)
    if data.startswith("settings-"):
        user_id = data.split("-")[1]
        if int(user_id) == int(call.from_user.id):
            n = db.get(f"user_{user_id}")
            btns  = InlineKeyboardMarkup([[InlineKeyboardButton(text="تغيير حالة الحساب",callback_data=f'changet-{user_id}')],[InlineKeyboardButton(text="المحفوظات .",callback_data=f"saves-{user_id}"),InlineKeyboardButton(text="تعيين بايو",callback_data=f"bio-{user_id}")],[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
    
            return app.edit_message_text(chat_id=call.message.chat.id,text=' اعدادات حسابك..',message_id=call.message.id,reply_markup=btns)
    if data.startswith('changet-'):
            user_id = data.split("-")[1]
            n = db.get(f"user_{user_id}")
            if n['private'] == False or n['private'] == None:
                n['private'] = True
                db.set(f"user_{user_id}",n)
                return call.answer(f"تم تغيير حالة حسابك لـ خاص")
            else:
                n['private'] = False
                db.set(f"user_{user_id}",n)
                return call.answer(f"تم تغيير حاله حسابك لـ عام")
    if data.startswith('bio-'):
        btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
        user_id = data.split("-")[1]
        bio = db.get(f"user_{user_id}")['bio']
        db.set(f"pending_bio_{user_id}",True)
        return call.edit_message_text(f"البايو هسة : {bio} \n ارسل البايو الجديد ..",reply_markup=btns)
    if data.startswith("up_video-"):
        user_id = data.split("-")[1]
        btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
        if int(user_id) == int(call.from_user.id):
            db.set(f"pending_upload_vid_{user_id}",True)
            return app.edit_message_text(text="الحين أرسل الفيديو (الوصف مقبول)",chat_id=call.message.chat.id,message_id=call.message.id,reply_markup=btns)
    if data.startswith("up_text-"):
        user_id = data.split("-")[1]
        btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
        if int(user_id) == int(call.from_user.id):
            db.set(f"pending_upload_text_{user_id}",True)
            return app.edit_message_text(text="الحين أرسل النص ",chat_id=call.message.chat.id,message_id=call.message.id,reply_markup=btns)
    if data.startswith("up_photo-"):
        user_id = data.split("-")[1]
        btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
        if int(user_id) == int(call.from_user.id):
            db.set(f"pending_upload_photo_{user_id}",True)
            return app.edit_message_text(text="الحين أرسل لصورة (الوصف مقبول)",chat_id=call.message.chat.id,message_id=call.message.id,reply_markup=btns)
    if call.data == "search":
        db.set(f"search_{call.from_user.id}",True)
        btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
        return call.edit_message_text("الحين أرسل ايدي الشخص ؟",reply_markup=btns)
    if call.data == "explore":
        from random import choice
        next_button = InlineKeyboardMarkup([[InlineKeyboardButton(text="التالي",callback_data="explore")]])
        all_keys = db.keys(list=True) 

        users = [] 
        
        
        for key in all_keys:
            if ("user" not in key):
                continue
            if ("_email" in key):
                continue
            else:
                user = db.get(key)  
                
                if isinstance(user["data"], dict) and (user["data"].get("photos") or user["data"].get("videos") or user["data"].get("texts")):
                    users.append(user)
 



        if not users:
            call.answer("مافي فيديوهات")
            return
        while True:
            current_user = choice(users)
            media = choice([
                (media_type, media)
                for media_type, media_list in current_user["data"].items()
                for media in media_list
            ])
            post_id = media[1]["id"]
            
            if db.key_exists(f"seen_{post_id}_{call.from_user.id}"):
                continue
            
            # Mark the post as seen
            db.set(f"seen_{post_id}_{call.from_user.id}", True)
            app.delete_messages(call.message.chat.id, call.message.id)
            
            if media[0] == "photos":
                photo = media[1]
                url = photo["file"]['url']
                next_button = InlineKeyboardMarkup([[InlineKeyboardButton(text="التالي",callback_data="explore")],[InlineKeyboardButton(text="حفظ المنشور",callback_data=f"save_{url}")]])

                by_info = media[1]['by']
                name = by_info['name']
                date = by_info['date']
                call.answer("جار ارسال صورة...")
                app.send_photo(
                    chat_id=call.from_user.id,
                    photo=photo["file"]['url'],
                    caption=f'<code>{media[1]["caption"]}</code>\n\nبواسطة: {name[:10]} \n في: {date}',
                    reply_markup=next_button
                )
                break
            elif media[0] == "videos":
                video = media[1]
                url = video["file"]['url']
                next_button = InlineKeyboardMarkup([[InlineKeyboardButton(text="التالي",callback_data="explore")],[InlineKeyboardButton(text="حفظ المنشور",callback_data=f"save_{url}")]])

                by_info = media[1]['by']
                name = by_info['name']
                date = by_info['date']
                call.answer("جار ارسال فيديو...")
                app.send_video(
                    chat_id=call.from_user.id,
                    video=video["file"]['url'],
                    caption=f'<code>{media[1]["caption"]}</code>\n\nبواسطة: {name[:10]} \n في: {date}',
                    reply_markup=next_button
                )
                break
            elif media[0] == "texts":
                
                text = media[1]["info"]['text']
                
                id3 = media[1]['id']
                
                url = f"{id3}"
                next_button = InlineKeyboardMarkup([[InlineKeyboardButton(text="التالي",callback_data="explore")],[InlineKeyboardButton(text="حفظ المنشور",callback_data=f"save_{url}")]])

                by_info = media[1]['by']
                name = by_info['name']
                date = by_info['date']
                likes = media[1]['info']['likes']
                call.answer("جار ارسال نص ...")
                app.send_message(
                    chat_id=call.from_user.id,
                    text=f"المنشور:\n <code>{text}</code>\n\nبواسطة: {name[:10]} \n في: {date}",
                    reply_markup=next_button
                )
                break
    if call.data.startswith("scrap_"):
        user_id = call.data.split("scrap_")[1]
        user = db.get(f"user_{user_id}")  
        users = []
        from random import choice
        if isinstance(user["data"], dict) and (user["data"].get("photos") or user["data"].get("videos") or user["data"].get("texts")):
            users.append(user)
        user1 = users[-1]
        vid = len(user1['data']['videos'])
        pho = len(user1['data']['photos'])
        texts = len(user1['data']['texts'])
        v1 = []
        ph = []
        tx = "النصوص:\n"
        pts = []
        vts = []
        for photo in range((pho)):
            id = user1['data']['photos'][photo]['file']['unique']
            caption = user1['data']['photos'][photo]['caption']
            ph.append({"id":id,"c":caption})
        for video in range((vid)):
            id = user1['data']['videos'][video]['file']['url']
            caption = user1['data']['videos'][video]['caption']
            v1.append({"id":id,"c":caption})
        
        for photo in range(len(ph)):
            app.download_media(f"{ph[photo]['id']}",file_name=f"temp/{photo}.jpg")
            pts.append(InputMediaPhoto(f"temp/{photo}.jpg", caption=f"{ph[photo]['c']}"))
        for vv in range(len(v1)):
            vts.append(InputMediaVideo(f"{v1[vv]['id']}", caption=f"{v1[vv]['c']}"))
        
        c =  app.send_media_group(chat_id=call.message.chat.id,media=pts)
        app.send_message(call.message.chat.id,f"الصور:",reply_to_message_id=call.message.id)
        b = app.send_media_group(chat_id=call.message.chat.id,media=vts)
        app.send_message(call.message.chat.id,f"الفيديوهات:",reply_to_message_id=call.message.id)
        for t in range(texts):
            text = user1['data']['texts'][t]['info']['text']
            tx += f"<code>{text}</code>\n\n"
        app.send_message(chat_id=call.message.chat.id,text=f"<code>{tx}</code>")
        app.send_message(call.message.chat.id,f"المنشورات:",reply_to_message_id=call.message.id)
    if call.data.startswith("save_"):
        datas = data.split("_")
        url = datas[1]
        if db.key_exists(f"user_{call.from_user.id}_savelist") == 1:
            if "telegra.ph" in str(url):
                
                rn = "".join(random.choice(string.digits) for _ in range(5))
                fid = f"{call.from_user.id}_{rn}"
                d = {"url":url,"id":fid,'rid':url,"media":True}
                info = db.get(f"user_{call.from_user.id}_savelist")
                info['data'].append(d)
                db.set(f"user_{call.from_user.id}_savelist",info)
                call.answer(f"تم الحفظ!")
                return
            else:
                id = datas
                
                
                rid = id[1]
                z = db.get(f"user_{rid}")
                found=False
                for t in z['data']['texts']:
                    
                    if str(t['id']).split("_")[1] == str(id[2]):
                        found = True
                        rn = "".join(random.choice(string.digits) for _ in range(5))
                        fid = f"{call.from_user.id}_{rn}"
                        d = {"text":t['info']['text'],'rid':str(id[2]),"id":fid,"media":False}
                        info = db.get(f"user_{call.from_user.id}_savelist")
                        info['data'].append(d)
                        db.set(f"user_{call.from_user.id}_savelist",info)
                        call.answer("تم الحفظ!")
                        return
                    else:continue
                
                
        else:
            db.set(f"user_{call.from_user.id}_savelist",{"data":[]})
            if "telegra.ph" in str(url):
                rn = "".join(random.choice(string.digits) for _ in range(5))
                fid = f"{call.from_user.id}_{rn}"
                d = {"url":url,"id":fid,'rid':url,"media":True}
                info = db.get(f"user_{call.from_user.id}_savelist")
                info['data'].append(d)
                db.set(f"user_{call.from_user.id}_savelist",info)
                call.answer(f"تم الحفظ!")
                return
            else:
                id = datas
                rid = id[1]
                found  = False
                z = db.get(f"user_{rid}")
                rn = "".join(random.choice(string.digits) for _ in range(5))
                for t in z['data']['texts']:
                    print(str(t['id']).split("_")[1])
                    if str(t['id']).split("_")[1] == str(id[2]):
                        found = True
                        fid = f"{call.from_user.id}_{rn}"
                        d = {"text":t['info']['text'],'rid':str(id[2]),"id":fid,"media":False}
                        info = db.get(f"user_{call.from_user.id}_savelist")
                        info['data'].append(d)
                        db.set(f"user_{call.from_user.id}_savelist",info)
                        call.answer("تم الحفظ!")
                        return
                    else:continue
                
                
                    
@app.on_message(filters.private & filters.text)
def ask_email(app,message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    m  = message
    if db.get(f"ask_email_{user_id}"):
        if ("@"  in message.text) and not message.text.isdigit():
            email = message.text 
            from datetime import datetime
            inf = {
                "id":user_id,
                "bio":"",
                'private':None,
                'followers':[],
                'following':[],
                "data":{
                    "photos":[],
                    "texts":[],
                    "videos":[],
                },
                "date_of_join":str(datetime.now()),
            }
            
            db.delete(f"ask_email_{user_id}")
            
            db.set(f"user_{user_id}_email",email)
            db.set(f"user_{user_id}",inf)
            btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
            
            return message.reply(f"الايميل : {email} تم تعيينه .",reply_markup=btns)
        else:
            return message.reply("الايميل غير صالح .\nأعد ارساله ")
    if db.get(f"search_{message.from_user.id}"):
        btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
        ids = None
        try:
            ids = int(message.text)
        except:
            db.delete(f"search_{message.from_user.id}")
            return message.reply("الايدي لازم ارقام !",reply_markup=btns)
        if (ids) <6:
            db.delete(f"search_{message.from_user.id}")
            return message.reply("الايدي مره قصير!",reply_markup=btns)
        else:
            if db.key_exists(f"user_{ids}")==1:
                info = db.get(f"user_{ids}")
                db.delete(f"search_{message.from_user.id}")
                followers,following = len(info['followers']),len(info['following'])
                btns2 = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"جلب محتوى الشخص (منشوراته)",callback_data=f"scrap_{ids}")]])
                bio,private = info['bio'],"عام" if info['private'] == None or info['private'] == False else "خاص"
                if info['private'] == True:
                    return message.reply(f"معلومات الحساب:\n- ايدية : {ids} .\n- نوع لحساب : {private} .\n- المتابعين : {followers} .\n- المُتابعهم : {following} .\n- البايو : {bio}",reply_markup=btns)
                else:
                    return message.reply(f"معلومات الحساب:\n- ايدية : {ids} .\n- نوع لحساب : {private} .\n- المتابعين : {followers} .\n- المُتابعهم : {following} .\n- البايو : {bio}",reply_markup=btns2)

            else:
                return message.reply("مالقيت اي حساب .",reply_markup=btns)
    if db.get(f"pending_bio_{user_id}"):
        new_bio = message.text
        btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
        if len(new_bio) > 400:
            return message.reply("البايو لازم 400 حرف او اقل، ارسله من جديد .",reply_markup=btns)
        else:
            db.delete(f"pending_bio_{user_id}")
            info = db.get(f"user_{user_id}")
            info['bio'] = new_bio
            db.set(f"user_{user_id}",info)
            return message.reply("تم تعيين البايو الجديد .",reply_markup=btns)
    sp = ['كس','خول','عير','زب','طيز','نيج','قضيب','pussy','dick','boobs','tits','ديوس','ديوث']
    if db.get(f"pending_upload_text_{user_id}"):
        if db.key_exists(f"user_{m.from_user.id}"):
            btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
            inf = db.get(f"user_{m.from_user.id}")
            if m.text:
                if m.text in sp:
                    return m.reply("لايمكن إن يحتوي النص على كلمات مسيئة .",reply_markup=btns)
                if len(m.text) > 2000:
                    return m.reply("اقصى حد للرسالة هو 2000 حرف .",reply_markup=btns)
                else:
                    ids = f"{m.from_user.id}_{random.randint(1920,2324)}"
                    f_info = {
                        "id":ids,
                        "type":'text',
                        "by":{
                            "id":m.from_user.id,
                            "name":m.from_user.first_name,
                            "date":str(m.date),
                        },
                        "info":{
                            "text":m.text,
                            'date':str(m.date),
                            "likes":[],
                            "size":len(m.text),
                        },
                    }
                    inf['data']['texts'].append(f_info)
                    db.set(f"user_{m.from_user.id}",inf)
                
                    db.delete(f"pending_upload_text_{m.from_user.id}")
                    return m.reply(f"تم رفع النص !\n ارسل : <code>/text {ids}</code> ، لرؤية النص .",reply_markup=btns)
    if "/photo" in message.text:
        ids = None
        btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
        try:
            ids = message.text.split("/photo ")[1]
        except:
            return message.reply("الطريقة غير صالحة ..",reply_markup=btns)
        info = db.get(f"user_{user_id}")
        for i in info['data']['photos']:
            if i['id'] == ids:
                return message.reply_photo(i['file']['url'],caption=i['caption'],reply_markup=btns)
            else:
                continue
        pass
    if "/video" in message.text:
        ids = None
        btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
        try:
            
            ids = message.text.split("/video ")[1]
        except:
            return message.reply("الطريقة غير صالحة ..",reply_markup=btns)
        info = db.get(f"user_{user_id}")
        for i in info['data']['videos']:
            if i['id'] == ids:
                return message.reply_photo(i['file']['url'],caption=i['caption'],reply_markup=btns)
            else:
                continue
        pass
    if "/text" in message.text:
        btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
        ids = None
        try:
            ids = message.text.split("/text ")[1]
        except:
            return message.reply("الطريقة غير صالحة .",reply_markup=btns)
        info = db.get(f"user_{user_id}")
        for i in info['data']['texts']:
            
            if i['id'] == str(ids):
                return message.reply_text(i['info']['text'],reply_markup=btns)
            else:
                continue
        pass
    if "/get" in message.text:
        btns = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"رجوع",callback_data="back_main")]])
        ids = None
        try:
            ids = message.text.split("/get ")[1]
        except:
            return message.reply("الطريقة غير صالحة .",reply_markup=btns)
        info = db.get(f"user_{user_id}_savelist")
        for i in info['data']:
            
            if i['id'] == str(ids):
                if i['media'] == True:
                    if ".mp4" in str(i['url']):
                        return message.reply_video(i['url'],reply_markup=btns)
                    if ".jpg" in str(i['url']):
                        return message.reply_photo(i['url'],reply_markup=btns)
                if i['media'] == False:
                    return message.reply_text(i['text'],reply_markup=btns)
            else:
                continue
        pass
    
app.run()