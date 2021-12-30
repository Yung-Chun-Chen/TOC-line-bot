# Usage
# 輸入start開始
![start](https://user-images.githubusercontent.com/79755310/147723358-ef612368-304d-48a8-990e-cf85167c5b4d.jpg)

# 設定身高、體重、預算、年齡
![function_list](https://user-images.githubusercontent.com/79755310/147723437-809ebd81-5d72-4bbf-9ecb-b83e33b58638.jpg)

# 出現「功能選單」
![function_list2](https://user-images.githubusercontent.com/79755310/147723463-e653b69c-31e4-476c-9a71-003cb309b800.jpg)

# 點選 show FSM
![show_fsm](https://user-images.githubusercontent.com/79755310/147723481-396ab84e-a711-441e-89f2-b1d4b491d882.jpg)

# FSM圖
![fsm](https://user-images.githubusercontent.com/79755310/147723494-0f2496d7-bb0a-4f96-a0db-5dbf0942f24d.jpg)

# 點選 建議營養比例
![showsuggestion](https://user-images.githubusercontent.com/79755310/147723520-6351e0d1-0692-4a31-b057-e9ab21c6ea56.jpg)

# 點選 設定個人資訊 更新身高、體重、預算、年齡
![modified_information](https://user-images.githubusercontent.com/79755310/147723870-0f99d5f0-4df0-4826-9794-2e9d09fb0e99.jpg)

# 點選 分析早/午/晚餐營養指標 進入「選擇餐點」
![checknutrition](https://user-images.githubusercontent.com/79755310/147723580-e049c130-001b-4dab-9067-fd9bdd0dbb67.jpg)

# 點選 早餐
![breakfast](https://user-images.githubusercontent.com/79755310/147723601-51745287-dfd4-40e6-bc5e-25edfdf6541a.jpg)

# 點選餐點後回到「選擇餐點」，點選 顯示您的攝取資訊
![shownutrition](https://user-images.githubusercontent.com/79755310/147723746-b4415e57-06dd-4914-af32-d933a459c27f.jpg)

![shownutrition2](https://user-images.githubusercontent.com/79755310/147723762-d66658d7-3d60-4bbc-ae9b-a37a9dcf942f.jpg)

# 輸入return繼續選擇午餐、晚餐
![backtochecknutrition](https://user-images.githubusercontent.com/79755310/147724446-125f7aa8-220a-48c2-8d0c-be2339b9a8f3.png)

![lunch](https://user-images.githubusercontent.com/79755310/147723782-6613d5a5-62fd-44e0-9d79-b124e4e90ed7.jpg)

![dinner](https://user-images.githubusercontent.com/79755310/147723787-5bccd246-0b6b-4b2c-a7f5-92bf6d30d007.jpg)

# 輸入完 早/午/晚餐 後的完整攝取資訊
![show_all_nutrition](https://user-images.githubusercontent.com/79755310/147723986-f7eb2c12-04bb-4ca2-95a6-f2a14fccf285.jpg)


# Deny states : 4 deny states
1.餘額不足
![money_deny](https://user-images.githubusercontent.com/79755310/147723889-46140f91-18c1-4821-9af2-9590d9674094.jpg)

2.熱量太高
![calorie_deny](https://user-images.githubusercontent.com/79755310/147723908-6b38641c-e650-41f7-a621-a6daf66c25a1.jpg)

3.澱粉太多
![starch_deny](https://user-images.githubusercontent.com/79755310/147723917-6476ee6d-40b9-4a57-913f-c8dc68e01431.jpg)

4.蛋白質太多
![protein_deny](https://user-images.githubusercontent.com/79755310/147723932-2691d98e-3ccc-4b33-b86e-9d3c14cb296d.jpg)


# TOC Project 2020

[![Maintainability](https://api.codeclimate.com/v1/badges/dc7fa47fcd809b99d087/maintainability)](https://codeclimate.com/github/NCKU-CCS/TOC-Project-2020/maintainability)

[![Known Vulnerabilities](https://snyk.io/test/github/NCKU-CCS/TOC-Project-2020/badge.svg)](https://snyk.io/test/github/NCKU-CCS/TOC-Project-2020)


Template Code for TOC Project 2020

A Line bot based on a finite state machine

More details in the [Slides](https://hackmd.io/@TTW/ToC-2019-Project#) and [FAQ](https://hackmd.io/s/B1Xw7E8kN)

## Setup

### Prerequisite
* Python 3.6
* Pipenv
* Facebook Page and App
* HTTPS Server

#### Install Dependency
```sh
pip3 install pipenv

pipenv --three

pipenv install

pipenv shell
```

* pygraphviz (For visualizing Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)
	* [Note: macOS Install error](https://github.com/pygraphviz/pygraphviz/issues/100)


#### Secret Data
You should generate a `.env` file to set Environment Variables refer to our `.env.sample`.
`LINE_CHANNEL_SECRET` and `LINE_CHANNEL_ACCESS_TOKEN` **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

#### Run Locally
You can either setup https server or using `ngrok` as a proxy.

#### a. Ngrok installation
* [ macOS, Windows, Linux](https://ngrok.com/download)

or you can use Homebrew (MAC)
```sh
brew cask install ngrok
```

**`ngrok` would be used in the following instruction**

```sh
ngrok http 8000
```

After that, `ngrok` would generate a https URL.

#### Run the sever

```sh
python3 app.py
```

#### b. Servo

Or You can use [servo](http://serveo.net/) to expose local servers to the internet.


## Finite State Machine
![fsm](./img/show-fsm.png)

## Usage
The initial state is set to `user`.

Every time `user` state is triggered to `advance` to another state, it will `go_back` to `user` state after the bot replies corresponding message.

* user
	* Input: "go to state1"
		* Reply: "I'm entering state1"

	* Input: "go to state2"
		* Reply: "I'm entering state2"

## Deploy
Setting to deploy webhooks on Heroku.

### Heroku CLI installation

* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)

or you can use Homebrew (MAC)
```sh
brew tap heroku/brew && brew install heroku
```

or you can use Snap (Ubuntu 16+)
```sh
sudo snap install --classic heroku
```

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```

	refference: https://hackmd.io/@ccw/B1Xw7E8kN?type=view#Q2-如何在-Heroku-使用-pygraphviz

## Reference
[Pipenv](https://medium.com/@chihsuan/pipenv-更簡單-更快速的-python-套件管理工具-135a47e504f4) ❤️ [@chihsuan](https://github.com/chihsuan)

[TOC-Project-2019](https://github.com/winonecheng/TOC-Project-2019) ❤️ [@winonecheng](https://github.com/winonecheng)

Flask Architecture ❤️ [@Sirius207](https://github.com/Sirius207)

[Line line-bot-sdk-python](https://github.com/line/line-bot-sdk-python/tree/master/examples/flask-echo)
