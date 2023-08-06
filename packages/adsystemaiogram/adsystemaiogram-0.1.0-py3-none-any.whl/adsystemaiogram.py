from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import json 
from aiogram import types

interests_keyboard = InlineKeyboardMarkup(row_width=4)
ik1 = InlineKeyboardButton("Юмор & Развлечения", callback_data="adsystemparameters_2_1")
ik2 = InlineKeyboardButton("Новости", callback_data="adsystemparameters_2_2")
ik3 = InlineKeyboardButton("IT-сфера", callback_data="adsystemparameters_2_3")
ik4 = InlineKeyboardButton("Мода & Красота", callback_data="adsystemparameters_2_4")
ik5 = InlineKeyboardButton("Еда & Кулинария", callback_data="adsystemparameters_2_5")
ik6 = InlineKeyboardButton("Бизнес & Финансы", callback_data="adsystemparameters_2_6")
ik7 = InlineKeyboardButton("Политика", callback_data="adsystemparameters_2_7")
ik8 = InlineKeyboardButton("Образование", callback_data="adsystemparameters_2_8")
ik9 = InlineKeyboardButton("Криптовалюты", callback_data="adsystemparameters_2_9")
ik10 = InlineKeyboardButton("Искусство & Дизайн", callback_data="adsystemparameters_2_10")
ik11 = InlineKeyboardButton("Спорт", callback_data="adsystemparameters_2_11")
ik12 = InlineKeyboardButton("Путешествия", callback_data="adsystemparameters_2_12")
ik13 = InlineKeyboardButton("Видеоигры", callback_data="adsystemparameters_2_13")
ik14 = InlineKeyboardButton("Дети & Воспитание", callback_data="adsystemparameters_2_14")

nx = InlineKeyboardButton("Далее >", callback_data="adsystemparameters_2_next")
interests_keyboard.add(ik1, ik2)
interests_keyboard.add(ik3, ik4)
interests_keyboard.add(ik5, ik6)
interests_keyboard.add(ik7, ik8)
interests_keyboard.add(ik9, ik10)
interests_keyboard.add(ik11, ik12)
interests_keyboard.add(ik13, ik14)
interests_keyboard.add(nx)

genders_keyboard = InlineKeyboardMarkup()
genders_keyboard.add(InlineKeyboardButton("Мужчина", callback_data="adsystemparameters_0_-1"))
genders_keyboard.add(InlineKeyboardButton("Женщина", callback_data="adsystemparameters_0_1"))

ages_keyboard = InlineKeyboardMarkup()
ages_keyboard.add(InlineKeyboardButton(" <12 ", callback_data="adsystemparameters_1_1"), \
            InlineKeyboardButton(" 12-18 ", callback_data="adsystemparameters_1_2"), \
                InlineKeyboardButton(" 18-21 ", callback_data="adsystemparameters_1_3") )
ages_keyboard.add(InlineKeyboardButton(" 21-25 ", callback_data="adsystemparameters_1_4"), \
            InlineKeyboardButton(" 25-30 ", callback_data="adsystemparameters_1_5"), \
                InlineKeyboardButton(" 30-36 ", callback_data="adsystemparameters_1_6"))
ages_keyboard.add(InlineKeyboardButton(" 36-42 ", callback_data="adsystemparameters_1_7"), \
            InlineKeyboardButton(" 42-50 ", callback_data="adsystemparameters_1_8"), \
                InlineKeyboardButton(" 50-60 ", callback_data="adsystemparameters_1_9"))
ages_keyboard.add(InlineKeyboardButton(" >60 ", callback_data="adsystemparameters_1_10"))

try_again_keyboard = InlineKeyboardMarkup()
try_again_keyboard.add(InlineKeyboardButton("Попробовать ещё раз", callback_data="adsystemparameters_5"))

# temporary data storage
class UserAnswers(StatesGroup):
    interests_keyboard = State()
    captcha = State()
    bot = None
            
class MessageToAdSystem(BoundFilter):
    def __init__(self, bot):
        self.bot = bot
        
    async def check(self, message: types.Message):    
        bot = self.bot
            
        adsystem_host = 1089311758      # AdSystem id in Telegram
        survey = {
            0: "🆕 Теперь контент будет подбираться специально для Вас! \nДля этого, пожалуйста, ответьте на несколько вопросов.\n\nВы: ",
            1: "Ваш возраст:",
            2: "Чем Вы увлекаетесь?"
        }    
        keyboards = {
            0: genders_keyboard,
            1: ages_keyboard,
            2: interests_keyboard
        }   
        user = int(message.from_user.id)  # The user who wrote
        
        if user!=adsystem_host:
            await bot.send_message(chat_id=adsystem_host, text=f"message:{user}")       # request an ad for the user
            return False
        
        else:   
            if "survey" in message.text:
                data = message.text.replace("survey:", "").split(":")
                user = int(data[0])
                stage = int(data[1])

                if stage < 3:
                    await bot.send_message(chat_id=user, text=survey[stage], reply_markup=keyboards[stage])       # send question to the user
                                    
                return True 
                
            elif "ad" in message.text:
                data = json.loads(message.text.replace("ad:", "").replace("'", '"'))
                title = data['title']
                ad_text = data['ad_text']
                link = data['link']
                user = data['user']
                
                text = f"{title}\n{ad_text}"
                ad_keyboard = InlineKeyboardMarkup()
                ad_keyboard.add(InlineKeyboardButton("Перейти", url=link))
                
                await bot.send_message(chat_id=user, text=text, reply_markup=ad_keyboard)       # send question to the user
                
                return True 

                
class CallbackToAdSystem(BoundFilter):
    def __init__(self, bot):
        self.bot = bot
        
    async def check(self, callback_query: types.CallbackQuery):
        bot = self.bot
        adsystem_host = 1089311758      # AdSystem id in Telegram
        
        if callback_query.data.startswith("adsystemparameters") and int(callback_query.data.split("_")[1]) != 2 and int(callback_query.data.split("_")[1]) != 5:
            data = callback_query.data.split("_")
            
            user_id = callback_query.from_user.id
            parameter = data[1]
            value = data[2]
            
            await bot.send_message(chat_id=adsystem_host, text=f"survey:{user_id}:{parameter}:{value}")
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
            
            return True
        
        elif callback_query.data.startswith("adsystemparameters") and int(callback_query.data.split("_")[1]) == 5:  # request captcha again
            await bot.send_message(chat_id=adsystem_host, text=f"survey:{callback_query.from_user.id}:3:0")
            return True 
        
        else:
            return False 
        
class IsFromAdSystem(BoundFilter):
    async def check(self, message: types.Message ):
        adsystem_host = 1089311758      # AdSystem id in Telegram
        if message.from_user.id == adsystem_host:
            return True 
        else:
            return False     

class SaveBot(BoundFilter):
    def __init__(self, bot):
        self.bot = bot
        
    async def check(self, message):
        UserAnswers.bot = self.bot 
        return True 
    
class Me: me = None      

class IAmTheOwner(BoundFilter):
    def __init__(self, me):
        Me.me = me 
        
    async def check(self, message):
        return True

async def AdSystemConnectBot(message: types.Message):
    adsystem_host = 1089311758      # AdSystem id in Telegram
    if message.from_user.id == adsystem_host: await message.reply(Me.me)

# forward message
#@dp.message_handler(MessageToAdSystem() )
async def AdSystemMessage(message: types.Message): pass

# forward answer (1 and 2)
#@dp.callback_query_handler(CallbackToAdSystem(), state="*")
async def AdSystemCallback(callback_query: types.CallbackQuery, state: FSMContext):    
    if int(callback_query.data.split("_")[1]) == 1: 
        await UserAnswers.interests_keyboard.set()
        await state.update_data(interests_buttons=[ik1, ik2, ik3, ik4, ik5, ik6, ik7, ik8, ik9, ik10, ik11, ik12, ik13, ik14, nx])
        await state.update_data(interests={})
        
    elif int(callback_query.data.split("_")[1]) == 5:       # get captcha again
        await UserAnswers.captcha.set()
        
#@dp.callback_query_handler(state=UserAnswers.interests_keyboard)
async def AdSystemGetInterests(callback_query: types.CallbackQuery, state: FSMContext):   
    adsystem_host = 1089311758      # AdSystem id in Telegram
    data = callback_query.data.split("_")   # get data
    
    bot = UserAnswers.bot 
    
    user_id = callback_query.from_user.id
    parameter = data[1]
    value = data[2]
                    
    # получаем данные
    tmpData = await state.get_data()
        
    if value == "next" and tmpData['interests'].keys():
        await bot.send_message(chat_id=adsystem_host, text=f"survey:{user_id}:{parameter}:0:{list(tmpData['interests'].keys())}")
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await UserAnswers.captcha.set()
    elif value == "next" and not tmpData['interests'].keys():
        await bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=True, text='Выберете Ваши интересы, потом нажмите кнопку "Далее"')
    else:
        value = int(value)
        # обновляем кнопки
        if value not in tmpData['interests']:       # если пользователь выбрал данную категорию
            tmpData['interests_buttons'][value-1].text += " ✅"       # помечаем как выбранную
            tmpData['interests'][value] = None      # сохраняем интерес
        else:       # если пользователь передумал 
            tmpData['interests_buttons'][value-1].text = tmpData['interests_buttons'][value-1].text[:-2]
            del tmpData['interests'][value]      # удаляем интерес
            
        # сохраняем кнопки 
        await state.update_data(interests_buttons=tmpData['interests_buttons'])
        await state.update_data(interests=tmpData['interests'])
        
        # пересобираем клавиатуру
        new_keyboard = InlineKeyboardMarkup(row_width=4)
        new_keyboard.add(tmpData['interests_buttons'][0], tmpData['interests_buttons'][1])
        new_keyboard.add(tmpData['interests_buttons'][2], tmpData['interests_buttons'][3])
        new_keyboard.add(tmpData['interests_buttons'][4], tmpData['interests_buttons'][5])
        new_keyboard.add(tmpData['interests_buttons'][6], tmpData['interests_buttons'][7])
        new_keyboard.add(tmpData['interests_buttons'][8], tmpData['interests_buttons'][9])
        new_keyboard.add(tmpData['interests_buttons'][10], tmpData['interests_buttons'][11])
        new_keyboard.add(tmpData['interests_buttons'][12], tmpData['interests_buttons'][13])
        new_keyboard.add(tmpData['interests_buttons'][14])
        
        await callback_query.message.edit_reply_markup(reply_markup=new_keyboard)

#@dp.message_handler(state=UserAnswers.captcha )
async def AdSystemCaptcha(message: types.Message, state: FSMContext, *args):
    adsystem_host = 1089311758       # AdSystem id in Telegram
    bot = UserAnswers.bot 
    
    await state.finish()
    await bot.send_message(chat_id=adsystem_host, text=f"survey:{message.from_user.id}:4:{message.text}")
        

#@dp.message_handler(IsFromAdSystem(), content_types=['photo', 'text'])
async def AdSystemPhoto(message: types.Message, *args):
    bot = UserAnswers.bot 
    print(message)
    if "caption" in message:
        if "ad:" in message.caption:    # send ad
            image = message['photo'][0]['file_id']
            data = json.loads(message.caption.replace("ad:", "").replace("'", '"'))
            title = data['title']
            ad_text = data['ad_text']
            link = data['link']
            user = data['user']
            
            text = f"{title}\n{ad_text}"
            ad_keyboard = InlineKeyboardMarkup()
            ad_keyboard.add(InlineKeyboardButton("Перейти", url=link))
                    
            await bot.send_photo(chat_id=user, photo=image, caption=text, reply_markup=ad_keyboard)
            
        else:   # send captcha
            image = message['photo'][0]['file_id']
            data = message.caption.split("=")
            user_id = data[0]
            caption = data[1]
                
            await bot.send_photo(chat_id=user_id, photo=image, caption=caption)
            
    elif "text" in message:
        data = message.text.split(":")
        if data[1] == "end":      # success
            await bot.send_message(chat_id=data[0], text="Успешно! Можете продолжать пользоваться ботом!")
        else:
            await bot.send_message(chat_id=data[0], text=data[1], reply_markup=try_again_keyboard)
            