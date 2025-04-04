from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Yangi token
TOKEN = '7596912191:AAGTup9GbxIe0m8Ex6pJqKZhfnvRK2L1WAY'
MUHAMMAD_ISKANDAROV_ID = 7807493773

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    if user.id == MUHAMMAD_ISKANDAROV_ID:
        await update.message.reply_text("Salom, nma gap boshliq?")
        return
    
    # "Adminga Savol berish" inline knopka sifatida matn tagida
    keyboard = [[InlineKeyboardButton("Adminga Savol berish", callback_data='ask_question')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # "Narxlar" va "Isbot uchun" knopkalari pastdan chiqadi
    keyboard_bottom = [["Narxlar", "Isbot uchun"]]
    reply_markup_bottom = ReplyKeyboardMarkup(keyboard_bottom, resize_keyboard=True, one_time_keyboard=False)
    
    # Xabar va inline knopka birgalikda, pastdagi knopkalar esa alohida qo‘shiladi
    await update.message.reply_text(
        f"Salom, {user.first_name}! 😊\n"
        "Adminga savol berish uchun quyidagi knopkani bosing:",
        reply_markup=reply_markup  # Inline knopka
    )
    
    # Pastdagi knopkalarni qo‘shish uchun xabarni reply_markup_bottom bilan yuboramiz
    await update.message.reply_text(
        "Quyidagi knopkalardan birini tanlang:",
        reply_markup=reply_markup_bottom  # Pastdagi doimiy knopkalar
    )

# "Narxlar" knopkasi bosilganda
async def show_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Narxlar❕\n\n"
        "1000 ta 50 ming (aralash)👥\n"
        "1000 ta 55 ming (faqat ayollar)👩\n\n"
        "ESLATMA📌\n"
        "BITTA GURUHGA 24 SOAT ICHIDA 5 MINGTA ODAM QO'SHSA BO'LADI\n\n"
        "5MINGTA QUSHTIRGANLAR UCHUN SKITKA BOR✅\n\n"
        "ADMIN 👤@Muhammad_iskandarov"
    )

# "Isbot uchun" knopkasi bosilganda
async def show_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ISBOT GURUHI! 🤖\n"
        "@Odamqushishhizmatil\n"
        "@Odam_QUSHlSH\n\n"
        "SHAXSIY AKKAUNTIM👇🏻\n"
        "@Muhammad_iskandarov\n\n"
        "TELEFON RAQAMIM\n"
        "+998 93 311 15 29 📱\n\n"
        "BUNDAN BOSHQA AKKAUNT VA NOMERIM YUQ ALDANIB QOLMANG‼️"
    )

# "Adminga Savol berish" knopkasi bosilganda
async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Savolingizni yozing:")
    context.user_data['waiting_for_question'] = True
    print("Knopka bosildi va 'Savolingizni yozing' xabari yuborildi")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    message_text = update.message.text
    
    # Admin xabarlari uchun alohida funksiyaga o‘tadi
    if user.id == MUHAMMAD_ISKANDAROV_ID:
        await handle_admin_reply(update, context)
        return
    
    # "Narxlar" knopkasi bosilganda
    if message_text == "Narxlar":
        await show_prices(update, context)
        return
    
    # "Isbot uchun" knopkasi bosilganda
    if message_text == "Isbot uchun":
        await show_proof(update, context)
        return
    
    # Agar foydalanuvchi savol yozayotgan bo‘lsa
    if context.user_data.get('waiting_for_question', False):
        user_message = update.message.text
        if len(user_message.strip()) < 5:
            await update.message.reply_text("Savolingizni to‘liq va aniq yozing!")
            return
        
        try:
            keyboard = [[InlineKeyboardButton("Foydalanuvchiga javob yozish", callback_data=f'reply_to_{user.id}')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            # Username bo‘lsa ko‘rsatamiz, bo‘lmasa lichkaga havola qo‘shamiz
            if user.username:
                username_display = f"@{user.username}"
            else:
                user_link = f'<a href="tg://user?id={user.id}">Foydalanuvchi lichkasi</a>'
                username_display = user_link
            # Hamma narsani bitta xabarda yuboramiz, HTML formatida
            await context.bot.send_message(
                chat_id=MUHAMMAD_ISKANDAROV_ID,
                text=f"Yangi savol!\n\nFoydalanuvchi: {user.first_name} (ID: {user.id})\nUsername: {username_display}\n\nXabar:\n{user_message}",
                reply_markup=reply_markup,
                parse_mode="HTML"  # Havolani bosiladigan qilish uchun HTML ishlatamiz
            )
            await update.message.reply_text("Savolingiz adminga yuborildi, javobni kuting!")
            context.user_data['waiting_for_question'] = False
        except Exception as e:
            await update.message.reply_text(f"Xatolik: {str(e)}")
            print(f"Foydalanuvchi savolini adminga yuborishda xatolik: {str(e)}")
    else:
        await update.message.reply_text("Iltimos, adminga savol berish uchun matndagi 'Adminga Savol berish' knopkasini bosing yoki pastdagi knopkalardan birini tanlang!")

async def handle_reply_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    if query.from_user.id != MUHAMMAD_ISKANDAROV_ID:
        await query.answer(f"Bu funksiya faqat admin uchun! Sizning ID'ingiz: {query.from_user.id}")
        return
    
    user_id = int(query.data.split('_')[-1])
    context.user_data['reply_to_user_id'] = user_id
    
    await query.answer()
    await query.message.reply_text(f"Foydalanuvchi (ID: {user_id}) ga yuboriladigan javobingizni yozing:")
    print(f"Admin javob yozish uchun tayyorlandi. Foydalanuvchi ID: {user_id}")

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != MUHAMMAD_ISKANDAROV_ID:
        return
    
    if 'reply_to_user_id' not in context.user_data:
        await update.message.reply_text("Javob yuborish uchun foydalanuvchi tanlanmagan.")
        return
    
    reply_message = update.message.text
    user_chat_id = context.user_data['reply_to_user_id']
    
    print(f"Admin javobi yuborilmoqda. Foydalanuvchi ID: {user_chat_id}, Xabar: {reply_message}")
    
    try:
        # Foydalanuvchiga javob yuborish
        await context.bot.send_message(
            chat_id=user_chat_id,
            text=f"Admin javobi:\n\n{reply_message}"
        )
        # Adminga tasdiq xabari
        await context.bot.send_message(
            chat_id=MUHAMMAD_ISKANDAROV_ID,
            text=f"Javob foydalanuvchiga (ID: {user_chat_id}) yuborildi!"
        )
        print(f"Javob muvaffaqiyatli yuborildi. Foydalanuvchi ID: {user_chat_id}")
    except Exception as e:
        await update.message.reply_text(f"Xatolik: {str(e)}")
        print(f"Javob yuborishda xatolik: {str(e)}")
        return
    
    del context.user_data['reply_to_user_id']

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(ask_question, pattern='ask_question'))
    app.add_handler(CallbackQueryHandler(handle_reply_button, pattern=r'reply_to_\d+'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()