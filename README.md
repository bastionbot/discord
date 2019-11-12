# Bastion Bot

Official SRSOC community bot.

Intended to provide general utility commands for users, and some fun stuff as well.

**Installation**
1) clone into `/opt/discord`
2) Create `/opt/discord/config.ini` with the two lines,`[client]` and `token = <bot token goes here>`
3) `ln -s /etc/systemd/system/bastion.service /opt/discord/bastion.service`
4) `systemctl daemon-reload`
5) `systemctl start bastion`

## Features

    * Self-service role management
        * list
        * join/add
        * leave/remove
    * Fun commands
        * `decide` - Make the bot make decisions for you!
        * `roll` - Roll all kinds of dice and nerd dice.
        * `8ball` - It's an 8ball.
        * `track` - Tracks GoFundMe progress!
