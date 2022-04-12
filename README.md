# Social Network

___

#### Simple Django REST API based social network, with scripts to demonstrate API functionalities.

___

## The project features:

#### ● user signup

#### ● user login

#### ● post creation

#### ● post list

#### ● post update

#### ● post delete

#### ● post like

#### ● post unlike

#### ● get info all users who liked this post

#### ● analytics about how many likes was made. Example url /api/analitics/?date_from=2022-04-10&date_to=2022-04-15 . API should return analytics aggregated by day.

#### ● JWT token authentication
___

## Testing API:

In order to test API functionality, you should use functions provided in "bot_functions.py" file. I recommend opening a python instance in same folder, and run demostration like following:


import above mentioned file


`import bot_functions as bf
`

First you need to edit the file, you can do it manually or using the function:

`bf.bot_configuration()
`

After that you can run the first function to register new users and create posts:

`bf.first_bot_activity()
`

And now you can run the second function for ask of liking like so:

`bf.second_bot_activity()`