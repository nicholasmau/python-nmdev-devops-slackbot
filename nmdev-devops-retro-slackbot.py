import os
import time
import re
from slackclient import SlackClient
from PIL import Image, ImageDraw, ImageFont
import datetime
import logging
import textwrap

# Built from tutorial from https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
# NMDEV 04/28/2018
# Just messing around with python + Slack API
# Set logging information
logging.basicConfig(filename='./log.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)


# instantiate Slack client
#slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_client = SlackClient('ENTER-SLACK-API-ID')
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "retro"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

# Text positioning and info
text_y = 100
text_pad = 45
#text_color = (33,47,61)
#text_color_footer = (93,109,126)
text_length_large_w_offset = 450
text_length_large_h_offset = 80
text_length_w_offset = 420
text_length_h_offset = 80
#text_length_normal = 33
#text_length_max = 39

# Define fonts for text, heading and footer
data_font = ImageFont.truetype("fonts/Roboto/Roboto-Italic.ttf", 32)
data_font_large = ImageFont.truetype("fonts/Roboto/Roboto-Italic.ttf", 30)
header_font = ImageFont.truetype("fonts/Roboto/Roboto-Bold.ttf", 50)
footer_font = ImageFont.truetype("fonts/Roboto/Roboto-Regular.ttf", 10)

# create datestamp
createdTimeStamp = datetime.datetime.now()


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    #if command.startswith(EXAMPLE_COMMAND):
    #    response = "Sure...write some more code then I can do that!"

    words_in_command = command.split()
    text_color = (33,47,61)
    text_color_footer = (93,109,126)
    # Used to limit length, but disabled for now
    #text_length_normal = 33
    #text_length_max = 39
    response = ""
    
    if words_in_command[0] == EXAMPLE_COMMAND:
        #response = "Sure...write some more code then I can do that!"

        # Used to limit length, but disabled for now
        #if len(command)<=text_length_normal:
        #    text_length = 'default'
        #elif len(command)>0 and len(command)<=text_length_max:
        #    text_length = 'large'
        
            if words_in_command[1].lower() == 'happy':
                mood = words_in_command[1].capitalize()
                for word in words_in_command[2:]:
                    response += word + " "

                # Set 'happy' color
                text_color = (33,47,61)
                # Load background image and get dimensions for positioning
                try:
                    bg_img = Image.open("images/happy_bg_img.png")

                except:
                    print("Error - Loading background")
                    logger.error("Error - Loading background")

            elif words_in_command[1].lower() == 'confused':
                mood = words_in_command[1].capitalize()
                #response = mood + ": "
                for word in words_in_command[2:]:
                    response += word + " "

                # Set 'confused' color
                text_color = (33,47,61)
                # Load background image and get dimensions for positioning
                try:
                    bg_img = Image.open("images/confused_bg_img.png")
            
                except:
                    print("Error - Loading background")
                    logger.error("Error - Loading background")

            elif words_in_command[1].lower() == 'sad':
                mood = words_in_command[1].capitalize()
                #response = mood + ": "
                for word in words_in_command[2:]:
                    response += word + " "
                # Set 'sad' color to red
                text_color = (255,0,0,255)
                # Load background image and get dimensions for positioning
                try:
                    bg_img = Image.open("images/sad_bg_img.png")
            
                except:
                    print("Error - Loading background")
                    logger.error("Error - Loading background")
            
            # Use API to attach image to slack channel, disabled for now
            #elif words_in_command[1].lower() == 'showpic':
            #    try:
            #        # Testing with 1 known image
            #        image_name = "output/retrospective_note_happy.png"
            #        attachments = attachments = [{"title": "Restrospective", "image_url": image_name}]
            #        slack_client.api_call("chat.postMessage", channel=channel, text='Last Retrospective Image', attachments=attachments)
            #    except:
            #        print("Error - Can't showing image")
            #        logger.error("Error - Can't show image")

            else:
                response = "Not sure what mood that is..."

            # Print out to console what we'll write to the image
            print(mood + ": " + response)

            try:
                surface = ImageDraw.Draw(bg_img)
                w, h = bg_img.size
        
            except:
                print("Error with initializing image info")
                logger.error("Error with initializing image info")

            # Write heading
            try:
                surface.text((w - 450, h-150), "Retrospective Note", font=header_font, fill=text_color)
        
            except:
                print("Error - Writing heading")
                logger.error("Error - Writing heading")

            # Write comment from command line arguement
            try:
                # Used to limit length, but disabled for now
                # Uses the textwrap modulue to format long text strings <30 characters
                #if text_length == 'large':
                #    text_length_w_offset = 150
                #    text_length_h_offset = 65
                #    for line in textwrap.wrap("'" + response + "'", width=100):
                #        surface.text((text_length_w_offset,text_length_h_offset), line, font=data_font_large, fill=text_color)
                #        text_length_w_offset += data_font_large.getsize(line)[1]
                
                #elif text_length == 'default':
                #    surface.text((w - text_length_w_offset, h - text_length_h_offset), "'" + response + "'", font=data_font, fill=text_color)

                # Without text limit
                surface.text((w - text_length_w_offset, h - text_length_h_offset), "'" + response + "'", font=data_font, fill=text_color)

                # Write timestamp in footer (w - 120 == width of img minus 20 px)
                surface.text((w - 120, h-20),"Created: " + createdTimeStamp.strftime('%m/%d/%y %H:%M'), font=footer_font, fill=text_color_footer)

                # Save file
                try:
                    bg_img.save(open("output/retrospective_note_" + mood + ".png", "wb"), "PNG")

                except IOError:
                    print("Error - Saving file")
                    logger.error("Error - Saving file")

                # open image after saving
                #try:
                #    image_name = "output/retrospective_note_Happy.png"
                #    #attachments = '[{"title": "Restrospective", "image_url": ' + image_name + '}]'
                #    slack_client.api_call("chat.postMessage", channel=channel, text='Retrospective', attachments='[{"title": "Retrospective","image_url":"./output/retrospective_note_Happy.png"}]')
                    
                #except:
                #    print("Error - Can't showing image")
                #    logger.error("Error - Can't show image")

            except:
                print("Error - Writing text")
                logger.error("Error - Writing text")

            # Completion message
            print("Process completed.")

        # Used to limit length, but disabled for now
        # Stops if the comment is > 30 characters to keep it clean.
        #elif len(command)>text_length_max:
        #    print("Error - Please keep the comment less than " + str(text_length_max) + " characters.\n Your comment is " + str(len(response)) + " characters.")
        #    logger.error("Error")

    else:
        response = "Not sure"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("NMDev DevOps Retro Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")