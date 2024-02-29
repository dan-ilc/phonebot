# Phone Bot

This repo contains a bot to call people and read out messages.

Architecture diagram: https://miro.com/app/board/o9J_l0HycFU=/?moveToWidget=3458764580554678026&cot=14

# Getting started (ubuntu)
Pro tip: on windows, run `wsl --install` to get a list of distros. I went for `Ubuntu-22.04`. Then get the VSCode plugin and start coding in the linux env.


> NOTE: Need to add the node source before you install, otherwise you'll get hit by a VERY old node
> NOTE2: I had to 
```
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get update && sudo apt-get install -y python3-venv nodejs npm 
``

set up your venv (ubuntu)
```bash
python3 -m venv testenv
source venv/bin/activate
pip install -r requirements.txt
```

and run the tests
```bash
pytest
```
### node
```
npx create-react-app phone-bot-app
```


## To do list
1. DONE Do twilio python tutorial DONE
2. DONE update python to actually send the correct message
3. DONE send requirements clarifications
4. do react app and host it

## questions
- where to host the app?

## design
write a build script for the react app that produces a set of static files. Static files are then loaded into the 
docker image and served by fastapi. Host with cloud run or heroku. 

## work log
Got a phone number `+447723427639`

wow windows env vars are annoying

oh wow WSL is a thing - cool

ok nice we are back in linux baby

let's run NPM in a container itself- that way we can directly deploy it. (ideally in a single container)

Nope actually because we're just putting the static files in the container so we don't need NPM/node in there per se

Oop getting hit by CORS. Fastapi can handle that

Ok now need a bit better error handling for the 400 validations

trying to make more stylish, adding bootstrap. Not sure how to add to package list, a `sudo npm install bootstrap` sorta worked.

ok so the answer is to cd into the dir and run `sudo npm install` to update the package list

tested with the full end to end. Now to deploy to cloud run.

