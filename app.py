from pyrogram import Client, filters
import config
import logging
from rich.logging import RichHandler
import json
import requests
import datetime

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")
log.info("Hello, World!")

app = Client("my_account", api_id=config.api_id, api_hash=config.api_hash)



@app.on_message(filters.command(["get_user", "getUser"], prefixes=".") & filters.private & filters.me)
async def getUser(client, message):
	await message.delete()
	userID = message.chat.id
	userInfo = await app.get_users(userID)
	msgInfo = f"""**User**
	First name: {userInfo.first_name}
	Last name: {userInfo.last_name}
	Username: @{userInfo.username}
	Is Bot: {userInfo.is_bot}
	Is PREMIUM: {userInfo.is_premium}
	ID: `{userInfo.id}` 
	"""

	await app.send_message("me", msgInfo)


@app.on_message(filters.command(["get_chat", "getChat"], prefixes=".") & filters.group & filters.me)
async def getChat(client, message):
	await message.delete()
	chatID = message.chat.id
	chatInfo = await app.get_chat(chatID)
	msgInfo = f"""**Group**
	Title: {chatInfo.title}
	Usename: @{chatInfo.username}
	Invite Link: {chatInfo.invite_link}
	Type: {chatInfo.type}
	Members count: {chatInfo.members_count}
	ID: `{chatInfo.id}`

**Permissions**
	Can send messages: __{chatInfo.permissions.can_send_messages}__
	Can send media messages: __{chatInfo.permissions.can_send_media_messages}__
	Can send other messages: __{chatInfo.permissions.can_send_other_messages}__
	Can add web pade previews: __{chatInfo.permissions.can_add_web_page_previews}__
	Can send polls: __{chatInfo.permissions.can_send_polls}__
	Can invite users: __{chatInfo.permissions.can_invite_users}__
	Can pin messages: __{chatInfo.permissions.can_pin_messages}__
	Can change info: __{chatInfo.permissions.can_change_info}__

**Available reactions**: {chatInfo.available_reactions}
	"""

	# Can send messages: Отправка сообщений
	# Can send media messages: Отправка медияфайлов
	# Can send other messages: Отправка стикеров и GIF
	# Can add web pade previews: Предпросмотр для ссылок
	# Can send polls: Создание опросов
	# Can invite users: Добавление участников
	# Can pin messages: Закрепление сообщений
	# Can change info: Изменение профиля группы

	await app.send_message("me", msgInfo)



@app.on_message(filters.command(["get_chat_member", "getChatMember"], prefixes=".") & filters.group & filters.reply & filters.me)
async def getChatMember(client, message):
	await message.delete()
	memberID = message.reply_to_message.from_user.id
	memberInfo = await app.get_chat_member(message.chat.id, memberID)

	msgInfo_member = f"""
	<b>Group <u>{message.chat.title}</u></b>
	Member: <u>{memberInfo.user.first_name}</u>
	Username: @{memberInfo.user.username}
	Is Bot: <i>{memberInfo.user.is_bot}</i>
	Is Premium: <i>{memberInfo.user.is_premium}</i>
	ID: <code>{memberInfo.user.id}</code>
	"""
	await app.send_message("me", msgInfo_member)




@app.on_message(filters.command(["get_chat_admin", "getChatAdmin"], prefixes=".") & filters.group & filters.reply & filters.me)
async def getChatMember(client, message):
	await message.delete()
	memberID = message.reply_to_message.from_user.id
	memberInfo = await app.get_chat_member(message.chat.id, memberID)

	try:
		msgInfo_admin = f"""
		<b>Group <u>{message.chat.title}</u></b>
		Member: <u>{memberInfo.user.first_name}</u>
		Username: @{memberInfo.user.username}
		Is Bot: <i>{memberInfo.user.is_bot}</i>
		Is Premium: <i>{memberInfo.user.is_premium}</i>
		ID: <code>{memberInfo.user.id}</code>  

		<b>Privileges</b>
		Can Change Info: {memberInfo.privileges.can_change_info}
		Can Delete Messages: {memberInfo.privileges.can_delete_messages}
		Can Restrict Members: {memberInfo.privileges.can_restrict_members}
		Can Invite Users: {memberInfo.privileges.can_invite_users}
		Can Pin Messages: {memberInfo.privileges.can_pin_messages}
		Can Manage Video Chats: {memberInfo.privileges.can_manage_video_chats}
		Is Anonymous: {memberInfo.privileges.is_anonymous}
		Can Promote Members: {memberInfo.privileges.can_promote_members}
		"""
		await app.send_message("me", msgInfo_admin)
	except:
		await app.send_message("me", f"<b>{message.from_user.first_name} NOT ADMINISTRATOR</b>")




@app.on_message(filters.command(["get_weather", "getWeather"], prefixes=".") & filters.me)
async def getWeather(client, message):
	await message.delete()
	cityName = message.text.split()[1]
	weatherInfo = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={cityName}&appid={config.WEATHER_KEY}&units=metric").json()
	msgInfo = f"""<b>***{datetime.datetime.today()}***</b>
	<b>Гороп:</b> <code>{weatherInfo['name']}</code>
	<b>Страна:</b> <code>{weatherInfo['sys']['country']}</code>
	<b>Температура:</b> <code>{weatherInfo['main']['temp']}°C</code>
	<b>Облака:</b> <code>{weatherInfo['clouds']['all']}</code>
	<b>Влажность:</b> <code>{weatherInfo['main']['humidity']}</code>
	<b>Давлене:</b> <code>{weatherInfo['main']['pressure']}</code>
	<b>Направление Ветра:</b> <code>{weatherInfo['wind']['deg']}°</code>
	<b>Скорость Ветра:</b> <code>{weatherInfo['wind']['speed']} m/s</code>"""

	await app.send_message(message.chat.id, msgInfo)





app.run()