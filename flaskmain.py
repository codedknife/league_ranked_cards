from flask import Flask, render_template, request
import requests, re, math

#functions
def get_champion_name(champion_pool_url, champion_key):
    response = requests.get(champion_pool_url)
    champions_data = response.json()
    champions_dict = champions_data['data']

    for champion in champions_dict.values():
        if int(champion.get("key")) == champion_key:
            return champion.get("name")
    return None


#####################


app = Flask(__name__)

@app.route('/')
#render_template displays the html file at hand
def display_homepage():
    return render_template('home.html')

@app.route('/username', methods=['GET', 'POST'])
def check_username():
    #recieve the shortcode (username) from home.html
    shortcode = request.form['shortcode']
    #recieve the server (returns server) from home.html
    server = request.form['server']
    
    #api_keys: create the api_url based on username
    api_key = "RGAPI-c417f988-6b74-45a5-ad94-06e138271140"
    api_url = "https://" + server + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    api_url = api_url + shortcode + '?api_key=' + api_key
    
    #returns a dictionary if found
    get_playerinfo = requests.get(api_url)
    if get_playerinfo.status_code == 404:
        return render_template('doesnotexist.html', error=
                               "The Summoner ID does not exist.")
    else:
        #returns a dictionary
        get_playerinfo = requests.get(api_url)
        player_info = get_playerinfo.json()
    
        #extracts first api
        player_name = player_info["name"]
        player_level = player_info["summonerLevel"]
        player_pic = str(player_info["profileIconId"])
    
        #returns the url for profile pic
        player_pic_url = "http://ddragon.leagueoflegends.com/cdn/13.7.1/img/profileicon/"
        player_pic_url += player_pic + ".png"
    
        #new api for ranked info
        player_id = player_info["id"]
        api_url_2 = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/"
        api_url_2 = api_url_2 + player_id + '?api_key=' + api_key
        get_playerinfo2 = requests.get(api_url_2)
        player_info2 = get_playerinfo2.json()
    
        #extracts second api
        player_tier = player_info2[0]["tier"]
        player_rank = player_info2[0]["rank"]
        
        player_wins = str(player_info2[0]["wins"])    
        player_losses = str(player_info2[0]["losses"])
        player_wr = str(math.trunc((player_info2[0]["wins"])/ ((player_info2[0]["losses"]) + (player_info2[0]["wins"]))*100))
    
        #gets top 3 champions mastery
        api_url_3 = "https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"
        api_url_3 += player_id + "/top" + '?api_key=' + api_key
        get_mastery_info = requests.get(api_url_3)
        mastery_info = get_mastery_info.json()
    
        # get champion id in str   
        ch_id1 = mastery_info[0]["championId"]
        ch_id2 = mastery_info[1]["championId"]
        ch_id3 = mastery_info[2]["championId"]
    
        #get champion level convert to string
        ch_lvl1 = str(mastery_info[0]["championLevel"])
        ch_lvl2 = str(mastery_info[1]["championLevel"])
        ch_lvl3 = str(mastery_info[2]["championLevel"])
    
        #get champion points convert to string
        ch_mp1 = str(mastery_info[0]["championPoints"])
        ch_mp2 = str(mastery_info[1]["championPoints"])
        ch_mp3 = str(mastery_info[2]["championPoints"])
    
        #search in api the key to find character name
        champion_pool = "http://ddragon.leagueoflegends.com/cdn/13.7.1/data/en_US/champion.json"
        ch1 = get_champion_name(champion_pool, ch_id1)
        ch2 = get_champion_name(champion_pool, ch_id2)
        ch3 = get_champion_name(champion_pool, ch_id3)
    
        ch1name = re.sub(r'\W+', '', ch1)
        ch2name = re.sub(r'\W+', '', ch2)
        ch3name = re.sub(r'\W+', '', ch3)
    
        api_ch_img = "http://ddragon.leagueoflegends.com/cdn/13.7.1/img/champion/"
        ch1_img = api_ch_img + ch1name + ".png"
        ch2_img = api_ch_img + ch2name + ".png"
        ch3_img = api_ch_img + ch3name + ".png"
    
        return render_template('afterinputid.html',
                           server=server,
                           player_pic_url=player_pic_url,
                           player_name=player_name,
                           player_level=player_level,
                           player_tier=player_tier,
                           player_rank=player_rank,
                           player_wins=player_wins,
                           player_losses=player_losses,
                           player_wr=player_wr,
                           ch1=ch1,
                           ch2=ch2,
                           ch3=ch3,
                           ch_lvl1=ch_lvl1,
                           ch_lvl2 = ch_lvl2,
                           ch_lvl3 = ch_lvl3,
                           ch_mp1 = ch_mp1,
                           ch_mp2 = ch_mp2,
                           ch_mp3 = ch_mp3,
                           ch1_img = ch1_img,
                           ch2_img = ch2_img,
                           ch3_img = ch3_img)
