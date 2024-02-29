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

apparently WSL doesnt bundle docker natively. Oh boy here we go.

ok so you can't "just" install docker on WSL. Have to install for windows and link thru.

Ok docker now on windows. Narrowly dodged an update and restart. 

ok while docker is building... how do i run a container, host it, and inject secrets

created a project
```
gcloud projects create phonebot-123 --name=phonebot
gcloud config set project phonebot-123
```
had to set billing acc in console
now can set apis to run
```
gcloud services enable container.googleapis.com secretmanager.googleapis.com containerregistry.googleapis.com
```
great now how do we create secrets
export our env
```
set -o allexport
source .env
set +o allexport
```
create the secrets. Should probs use more descriptive names
```
gcloud secrets create AUTH_TOKEN --data-file <(echo -n "${AUTH_TOKEN}")
gcloud secrets create ACCOUNT_SID --data-file <(echo -n "${ACCOUNT_SID}")
```
and check
```
 gcloud secrets versions access latest --secret=AUTH_TOKEN
```
great now we need cloud run working. Container still not built. Restarted docker in windows. seems to have fixed things.

uggh i hate cors so much 

ok using an npm dev server is too much pain. Building

ok switching track to do the docker push. Need to configure docker.

Set up cloud run but the service account needs access to the secret. Weird - i am the service account.

Ok closing up shop here.