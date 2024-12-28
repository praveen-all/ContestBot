# import neccessary packages
import time as t
import telegram.ext
from datetime import datetime,time,timedelta
import requests as req
import json
import pytz



today_data=[]
hosts=["codingninjas.com/codestudio","atcoder.jp","codechef.com","codeforces.com","leetcode.com","geeksforgeeks.org"]


def start(update,context):
    update.message.reply_text("Hii , Namaste , Hola...\n Have good a Day \n how can i help(/help) you?")


def today(update,context):
    if len(today_data)==0:
        update.message.reply_text("There is no any contest Today ,*keep practicing*!!☺️☺️",parse_mode='Markdown')
    else:
        for el in today_data:
            date_time_obj = datetime.strptime(el["start"], "%Y-%m-%dT%H:%M:%S")
            ist_time_obj = date_time_obj + timedelta(hours=5, minutes=30)
            ist_time_str = ist_time_obj.strftime("%Y-%m-%dT%H:%M:%S")
            date_time_obj1 = datetime.strptime(el["end"], "%Y-%m-%dT%H:%M:%S")

            ist_time_obj2 = date_time_obj1+ timedelta(hours=5, minutes=30)
            ist_time_str3 = ist_time_obj2.strftime("%Y-%m-%dT%H:%M:%S")

            update.message.reply_text(f"""*{el["event"]}* hosted by *{el["host"].split(".")[0]}*\n\n *date*:{el["start"].split("T")[0]} from *{ist_time_str.split("T")[1]}* to *{ist_time_str3.split("T")[1]}* \n {el["href"]}""",parse_mode='Markdown')


def help(update,context):
    update.message.reply_text(
    """
    Here are the available commands:

    */help*    -> Get information about available commands
    */python*  -> Link to the first video of the Python playlist
    */java*    -> Link to the first video of the Java playlist
    */cpp*     -> Link to the first video of the C++ playlist
    */about*   -> Information about us
    */today*   -> Get information about today's contest
    */chatInfo*-> Get information about this chat

    Feel free to use these commands to interact with the bot!
    """,
    parse_mode='Markdown'
)


def python(update,context):
    update.message.reply_text("https://youtu.be/7wnove7K-ZQ?si=OP4ZSqNkHkGpS6B5")


def java(update,context):
    update.message.reply_text("https://youtu.be/yRpLlJmRo2w?si=RArnnGNQJx8Rp0JS")


def cpp(update,context):
    update.message.reply_text("https://youtu.be/z9bZufPHFLU?si=MBQPy50RojJHGbUF")


def about(update,context):
    update.message.reply_text("*Praveen Kumar G* from *3rd year ISE UVCE*",parse_mode='Markdown')


def chatInfo(update, context):
    chat_id = update.message.chat_id
    chat_type = update.message.chat.type
    chat_title = update.message.chat.title if chat_type == "group" else None
    chat_username = update.message.chat.username if chat_type == "channel" else None
    response = f"Chat ID: {chat_id}\nChat Type: {chat_type}"
    if chat_title:
        response += f"\nChat Title: {chat_title}"
    if chat_username:
        response += f"\nChat Username: {chat_username}"
    update.message.reply_text(response)


# autocatical chat sender
def send_contest_info(context):
    chat_id = context.job.context
    hey=True
    print("hi man ")
    today_data.clear()
    for host in hosts:
        data=req.get(f"https://clist.by/api/v4/json/contest/?upcoming=true&username=pvnkmrg85&api_key=fc16b16f5e2396edcd59f8c5c7b8e787e38a8f1e&host={host}")
        if data.status_code == 200:
            if data.content is not None:
                try:
                    x=json.loads(data.content)
                    utc_now = datetime.utcnow()
                    india_timezone = pytz.timezone('Asia/Kolkata')
                   # Convert the UTC time to India time zone
                    india_now = utc_now.replace(tzinfo=pytz.utc).astimezone(india_timezone)
                    formatted_now = india_now.strftime('%Y-%m-%dT%H:%M:%S')
                    # print(formatted_now)
                    hey1=datetime.strptime(formatted_now,"%Y-%m-%dT%H:%M:%S")
                    y=x["objects"]
                    li=[]
                    for el in y:
                        hey2=datetime.strptime(el["start"],"%Y-%m-%dT%H:%M:%S")
                        # print(hey1,hey2)
                        if hey1.date()==hey2.date():
                            li.append(el)
                            today_data.append(el)
                            # print(el)
                    for el in li:
                        date_time_obj = datetime.strptime(el["start"], "%Y-%m-%dT%H:%M:%S")
                        ist_time_obj = date_time_obj + timedelta(hours=5, minutes=30)
                        ist_time_str = ist_time_obj.strftime("%Y-%m-%dT%H:%M:%S")
                        date_time_obj1 = datetime.strptime(el["end"], "%Y-%m-%dT%H:%M:%S")
                        ist_time_obj2 = date_time_obj1+ timedelta(hours=5, minutes=30)
                        ist_time_str3 = ist_time_obj2.strftime("%Y-%m-%dT%H:%M:%S")
                        context.bot.send_message(chat_id=chat_id, text=f"""*{el["event"]}* hosted by *{el["host"].split(".")[0]}*\n\n *date*:{el["start"].split("T")[0]} from *{ist_time_str.split("T")[1]}* to *{ist_time_str3.split("T")[1]}* \n {el["href"]}""",parse_mode='Markdown' )
                        hey=False

                except json.JSONDecodeError:
                     print("JSON error")

    if(hey):
        context.bot.send_message(chat_id=chat_id, text="There is no any contest Today ,*keep practicing*!!☺️☺️",parse_mode='Markdown')


# scheduling daily message when time is 11:40
def schedule_daily_message(updater):
    job_context =-879820948
    job_queue = updater.job_queue
    job_queue.run_daily(send_contest_info, time=time(19,30, 0), context=job_context)



updater = telegram.ext.Updater("6830274323:AAHoLrjsf5r8ULEs_kiVN9OzEZdZ30rDwYY",use_context=True)
schedule_daily_message(updater)
dispatcher = updater.dispatcher

print("started....")

# all commonds
dispatcher.add_handler(telegram.ext.CommandHandler("start",start))
dispatcher.add_handler(telegram.ext.CommandHandler("help",help))
dispatcher.add_handler(telegram.ext.CommandHandler("python",python))
dispatcher.add_handler(telegram.ext.CommandHandler("java",java))
dispatcher.add_handler(telegram.ext.CommandHandler("cpp",cpp))
dispatcher.add_handler(telegram.ext.CommandHandler("about",about))
dispatcher.add_handler(telegram.ext.CommandHandler("today",today))
dispatcher.add_handler(telegram.ext.CommandHandler("chatInfo",chatInfo))


updater.start_polling()
updater.idle()



