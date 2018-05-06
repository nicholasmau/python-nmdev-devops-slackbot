# python-nmdev-devops-slackbot
Weekend project of messing around with python and slack API

Credit:
This tutorial was built using the tutorials below (Thanks!):
- https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
- https://hackaday.com/2018/03/21/making-pictures-worth-1000-words-in-python/

Description of project:
A weekend project to practice Python and utilize Slack APIs. The use-case:
Part 1 - To have Python create an image from user input
Part 2 - Serve a slackbot to listen and respond to command from slack
Part 3 - Attach the newly created image to the slack channel (not completed)

How to Use:
1. Get your Slack API key and enter it int the code (or create an environment
variable and call your variable)

2. Create a slackbot on Slack.

3. Add a slackbot user to access your slackbot.

4. Go to your Slacl channel and use "/invite" to add the slackbot user.

5. Run the Python file to start the slackbot and begin listening.

6. Go to your slack channel and invoke your slackbot (@slackbot user) + command:

7. The slackbot requires 3 arguments
    a. retro (or specified key word)
    b. -m for mood (Options: "happy", "confused" or "sad")
    c. -c for comment (free-form text)

8. Optional - run Python script as a service