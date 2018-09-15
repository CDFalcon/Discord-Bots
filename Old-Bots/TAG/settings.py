BOT_TOKEN = "NDM3MzQwNTEyNDU0ODM2MjU3.Db06sg.9HaEgOkNPS5pP-JyhPyclCgLPZQ"

VERSION = "?help"
ADMIN_ROLES = ["Founders", "TAG Admin"]
HELP_MENU = "```Help Menu```\n:white_check_mark: **Index:** :white_check_mark:\n1: *General Commands*\n2: *Hub Administrator Commands*\n3: *TAG Administrator Commands*\n*Note: all commands are case and space sensitive.*\n```#```\n:white_check_mark: **1: General Commands** :white_check_mark:\nUse `?help` to request this menu.\nUse `?join \"Hub Name Here\"` to join a hub of your choice.\nUse `?join \"Hub Name Here\" \"password\"` to join a password-protected hub.\nUse `?leave \"Hub Name Here\"` to leave a hub.\n```#```\n:white_check_mark: **2: Hub Administrator Commands** :white_check_mark:\nUse `?createPassword \"Hub Name Here\"` to create a new random password for your hub (changes your old password if you already have one).\nUse `?createPassword \"Hub Name Here\" \"true\"` to remove your current password.\nUse `?ban \"Hub Member\"` to kick and ban one of your hub members from your hub.\nUse `?unban \"Member\"` to unban a member from your hub.\nUse `?mod \"Hub Member\"` to make a **current member** of your hub a moderator.\nUse `?unmod \"Hub Member\"` to remove the moderator perms from a hub member.\nUse `?hide \"Hub Name Here\" \"Channel Name\"` to hide a channel from all hub members except for staff.\nUse `?unhide \"Hub Name Here\" \"Channel Name\"` to unhide a channel.\n```#```\n:white_check_mark: **3: TAG Administrator Commands** :white_check_mark:\nUse `?addPartner \"Hub Name Here\" \"First Admin\'s Name Here\"` to add a new partner and create a hub for them. Be extra careful with the first admin\'s name.\nUse `?addPartner \"Hub Name Here\" \"First Admin\'s Name Here\" \"true\"` to create a new password protected hub.\nUse `?removePartner \"Hub Name Here\"` to erase a partner and their hub from existence."

PASSWORD_ID = 437360721198579713
RECRUIT_CAT_ID = 437361351346618369
DY_CHAN_ID = 437361765941116928
DY_CAT_ID = 437361539188654081

ERROR__WRONG_CHANNEL = ":x: **Error:** You tried to execute a command in a DM with the bot, please run this command in a text channel on the server. :x:"
ERROR__INVALID_ARGS = ":x: **Error:** You are using your arguments incorrectly. Try running ?help to see a help menu. :x:"
ERROR__INVALID_HUB = ":x: **Error:** The hub you entered does not exist. And trust us, if an item does not appear on our records, it does not exist. Check your spelling, and keep everything cap-sensitive. :x:"
ERROR__WRONG_PASSWORD = ":x: **Error:** The password you entered for the hub is either non-existent or incorrect. Please ask an administrator for the password and add it to the end of your command. :x:"
ERROR__NOT_HUB_ADMIN = ":x: **Error:** You are trying to use an administrator command. Please get your hub's administrator to execute this command for you. :x:"
ERROR__NOT_TAG_ADMIN = ":x: **Error:** You are trying to use an TAG administrator command. Please contact TAG staff if you believe this is a mistake. :x:"
ERROR__NOT_A_MEMBER = ":x: **Error:** You are not even a member of the hub you are trying to leave. :x:"

NEW_HUB_MESSAGE = "```Welcome to The Armory Gaming Community!```\n:white_check_mark: **You are the administrator for your new hub.** :white_check_mark:\n**Please use** `?help` **to view all commands you now have access to. We appreciate your support!**"
JOIN_MESSAGE_START = "```Welcome to The Armory Gaming Community!```\n:white_check_mark: **You are now a member of **`"
JOIN_MESSAGE_END = "'s hub`. :white_check_mark:"
LEAVE_MESSAGE_START = ":white_check_mark: **You have left **`"
LEAVE_MESSAGE_END = "'s hub`. :white_check_mark:"
