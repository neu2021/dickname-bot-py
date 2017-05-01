import time
from slackclient import SlackClient

with open("id.txt") as file:
    BOT_ID = file.read()

AT_BOT = "<@" + BOT_ID + ">"

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
            if user.get("id") == user_id:
                return user.get("real_name")


def get_name(user_id):
    api_call = slack_client.api_call("users.list")
    if api_call.get("ok"):
        users = api_call.get('members')
        for user in users:
            if user.get("id") == user_id:
                return user.get("name")


def handle_command(user_id, command, channel):
    args = command.split()
    if args[0] == "name":
        if len(args) not in (1, 3):
            slack_client.api_call("chat.postMessage", channel=channel,
                                  text="Incorrect number of arguments!", as_user=True)
        else:
            if len(args) == 3:
                initials = [args[1][0].lower(), args[2][0].lower()]
                response = " ".join((map(lambda n: n[0].upper() + n[1:], args[1:])))
                if response[-1] == 's':
                    response += "'"
                else:
                    response += "'s"
            elif len(args) == 1:
                name = get_name(user_id)
                real_name = get_real_name(user_id)
                names = real_name.split()
                initials = [names[0][0].lower(), names[1][0].lower()]
                response = f"<@{user_id}>: Your"

            response += f" penis name is {firstname[initials[0]]} {lastname[initials[1]]}"
            slack_client.api_call("chat.postMessage", channel=channel,
                                  text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output["text"]:
                return output["user"], output['text'].split(AT_BOT)[1].strip().lower(), output["channel"]
    return None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("test-bot connected and running!")
        while True:
            uid, cmd, ch = parse_slack_output(slack_client.rtm_read())
            if cmd and ch:
                handle_command(uid, cmd, ch)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
