import time
from slackclient import SlackClient

with open("id.txt") as file:
    BOT_ID = file.read()

AT_BOT = f"<@{BOT_ID}>"

with open("token.txt") as file:
    slack_client = SlackClient(file.read())

firstname = {
    'a': "Long",
    'b': "Hard",
    'c': "Big",
    'd': "Girthy",
    'e': "Pleasure",
    'f': "Fun",
    'g': "Monster",
    'h': "Power",
    'i': "Bear",
    'j': "Man",
    'k': "Love",
    'l': "Sex",
    'm': "Purple",
    'n': "Mister",
    'o': "Fuck",
    'p': "Pussy",
    'q': "Ugly",
    'r': "Darling",
    's': "Giant",
    't': "Skin",
    'u': "Explosive",
    'v': "Hulk",
    'w': "Beast",
    'x': "Massive",
    'y': "Iron",
    'z': "Hairy"
}

lastname = {
    'a': "Want",
    'b': "Sword",
    'c': "Destroyer",
    'd': "Injector",
    'e': "Snake",
    'f': "Killer",
    'g': "Punch",
    'h': "Stick",
    'i': "Knob",
    'j': "Sausage",
    'k': "Flute",
    'l': "Gun",
    'm': "Pole",
    'n': "Tube",
    'o': "Machine",
    'p': "Beef",
    'q': "Schlong",
    'r': "Tool",
    's': "Meat",
    't': "Unit",
    'u': "Hammer",
    'v': "Salami",
    'w': "Steak",
    'x': "Pecker",
    'y': "Shaft",
    'z': "Rod"
}


def get_real_name(user_id):
    api_call = slack_client.api_call("users.list")
    if api_call.get("ok"):
        users = api_call.get('members')
        for user in users:
            if user.get("id").upper() == user_id:
                return user.get("real_name")


def handle_command(user_id, command, channel):
    args = command.split()

    # activate on the "name" command
    if args[0] == "name":

        # initial basic format check
        if len(args) not in (1, 2, 3):
            response = f"<@{user_id}>: Incorrect number of arguments!"
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        else:
            if len(args) == 3:
                initials = [args[1][0].lower(), args[2][0].lower()]  # get initials from arguments
                response = " ".join((map(lambda n: n[0].upper() + n[1:], args[1:])))  # capitalize name

                # properly use apostrophe (i.e. Charles' instead of Charles's)
                if response[-1] == 's':
                    response += "'"
                else:
                    response += "'s"

            elif len(args) == 2:
                lookup_id = args[1][2:-1].upper()  # parse out ID to look up

                # check if user wants the name of the bot
                if lookup_id == BOT_ID:
                    response = f"<@{user_id}>: My name is Penis Bot!"
                    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
                    return

                real_name = get_real_name(lookup_id)
                split_name = real_name.split()

                # check if user has set real name
                if not real_name:
                    response = f"<@{user_id}>: <@{lookup_id}> hasn't set their real name yet!"
                    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
                    return

                # check if name is valid
                if not len(split_name) == 2:
                    response = f"<@{user_id}>: <@{lookup_id}> does not have a valid name!"
                    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
                    return

                initials = [split_name[0][0].lower(), split_name[1][0].lower()]
                response = f"<@{user_id}: <@{lookup_id}>"
                if response[-1] == 's':
                    response += "'"
                else:
                    response += "'s"

            elif len(args) == 1:
                real_name = get_real_name(user_id)
                split_name = real_name.split()
                if not real_name:
                    response = f"<@{user_id}>: You haven't set your real name yet!"
                    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
                    return

                elif not len(split_name) == 2:
                    response = f"<@{user_id}>: Your name is invalid!"
                    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
                    return

                initials = [split_name[0][0].lower(), split_name[1][0].lower()]
                response = f"<@{user_id}>: Your"

            response += f" penis name is {firstname[initials[0]]} {lastname[initials[1]]}."
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    # show original image
    elif args[0] == "image":
        response = [
            {
                "fallback": "Penis name source image",
                "image_url": "http://i.imgur.com/MZEDlNI.png",
                "text": "This bot is based off of this image:"
            }
        ]
        slack_client.api_call("chat.postMessage", channel=channel, attachments=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and output["text"].startswith(AT_BOT):
                return output["user"], output['text'][12:].strip().lower(), output["channel"]
    return None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("penis-bot connected and running!")
        while True:
            uid, cmd, ch = parse_slack_output(slack_client.rtm_read())
            if cmd and ch:
                handle_command(uid, cmd, ch)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
