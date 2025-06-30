import requests
import json
import webbrowser
import time


SAMPLE_API_TOKEN = 'WwG6ytiCOhUoog4iCdPZjiGxLOqOhzoCgNWVuXhOjj1ToOH0b02yhcow6Zgl' #remember to change this later
current_params = {
    'api_token':SAMPLE_API_TOKEN,
    #'filters':'date_range:2022-01-01',
    #'include':'scores'
    }
URL = 'https://api.sportmonks.com/v3'
sportmonks_create_account = 'https://my.sportmonks.com/login'

team_ids = {
    '53':'Celtic',
    '62':'Rangers',
    '66':'Hibernian',
    '180':'Kilmarnock',
    '246':'Ross County',
    '273':'Aberdeen',
    '282':'Dundee United',
    '284':'Dundee',
    '309':'Motherwell',
    '314':'Hearts',
    '496':'St. Mirren',
    '734':'St. Johnstone'
}

def test_request(api_token):
    #this is the base api token filters verifier of sportmonks website
    #if you enter an invalid token, it returns an error message, and this function checks if the message
    #matches the error message 'Invalid token...' 
    #if it does, then the code returns 'false' so it can be checked in the 'get_api_token' function.
    test_url = f'https://api.sportmonks.com/v3/my/filters/entity?api_token={api_token}'
    r = requests.get(test_url)
    check_content = r.json()
    for value in check_content.values():
        if value == "Invalid token provided":
            print('Error: your Token is invalid, please enter a valid Token')
            return False
        else:
            return True

def get_api_token():
    #this is the get token and token verification
    while True:
        api_key_input = input('Insert your Sportmonks API key:\n')
        if len(api_key_input) > len(SAMPLE_API_TOKEN):
            print('Error: your Token is invalid, please enter a valid Token.')
            continue
        elif len(api_key_input) < len(SAMPLE_API_TOKEN):
            print('Error: your Token is invalid, please enter a valid Token.')
            continue
        elif test_request(api_key_input) == False: #this runs a test with 'test_request' to check if the token is valid
            continue #it makes a request to sportmonks 'available filters' page and if it returns a valid Token, the code flows normally.
        else: #if not, then it goes back into asking for the api_token.
            return api_key_input

def select_team_id():
    available_teams = list(team_ids.values())
    
    #for i, v in enumerate(available_teams):
        #print(f'{i+1}. {v}')

    while True:
        choose_team = input('pick a team:\n')
        if not choose_team.isdigit():
            print('Pick one of the available teams in the list.')
            continue
        
        choice_index = int(choose_team)-1
        if 0 <= choice_index < len(available_teams):
            selected_team_name = available_teams[choice_index]
            
            for k, v in team_ids.items():
                ids = k
                if selected_team_name == v:
                    return ids
        else:
            print('error')
            


#now I'll be setting up the available endpoints and information I want to retrieve
#I will have to check how to work with lists. How to add the available params in the list
#and how to 'include':';', .join(options_list)

#these are the endpoints I'll use: 
#/fixtures/head-to-head/{team_id_1}/{team_id2}
#/teams/seasons/{ID}
#/players/{ID} -> in this part I'll need to write a function to retrieve the infomation of each player
#I will have to use :api.sportmonks.com/v3/football/players/{player_id} then run a function to print
#the player's name, age, etc.
#for now this is what I'll be working with. and more functions will be added later


#this part is running the get_api_token, but I'll most likely have to replace it in the future



def head_to_head_request():
    available_teams = list(team_ids.values())
    
    for i, v in enumerate(available_teams):
        print(f'{i+1}. {v}')
    while True:
        team_id_1 = select_team_id()
        team_id_2 = select_team_id()
        if team_id_2 == team_id_1:
            print("Please pick different teams to compare")
            continue
        else:
            hth_url = f'{URL}/football/fixtures/head-to-head/{team_id_1}/{team_id_2}'
            return hth_url

def main_request(current_url, current_params):
    response = requests.get(current_url, params=current_params)
    parsed_response = response.json()
    print(response.url)
    #print(type(parsed_response))
    for date in parsed_response.get('data'):
        if '2024-01-01' < date['starting_at']:
            print('This is the data for the current request:')
            print(f'Teams: {date["name"]}')
            print(f'Match result: {date["result_info"]}')
            print(f'Match date: {date["starting_at"]}')
            print('-'*len(f'match date: {date["result_info"]}'))
        else:
            print('Nothing could be found!')
    #print(json.dumps(parsed_response, indent=2))
#&include=events shows the highlights of the match.

def main_menu():
    print('Hello, how would you like to be called?')
    name_input = input('Insert your name here: ')
    print('-'*65)
    print(f'Hi, {name_input}. Welcome to the Football Information Retriever program') 
    print('-'*65)   
    while True:
        print(f'Do you already possess an api key to use with our system?')
        yn_input = input('Y/N: ').lower()
        if yn_input in 'n':
            print('Redirecting to sportmonks website to create account and your api key\n')
            webbrowser.open(sportmonks_create_account)
            print('Once you have your api key, simply type "y" and paste it below')
            continue
        elif yn_input not in ('y', 'n'):
            print('Please write "y" or "n" to continue')
            continue
        else:
            get_key = get_api_token()
            print('Please, store your api key somewhere safe.')
            print('For security, once the program is closed, your api key is not saved in the program.')
            print('-'*70)            
            params: dict = {
                'api_token':get_key
            }
            while True:
                print('These are the current options:')
                print('1. Look for head to head information on the Scottish League.')
                print('2. Restart the program')
                print('3. Exit')
                options_input = input('Please, choose one of the available options: ')
                if options_input == '1':
                    get_hth = head_to_head_request()
                    main_request(get_hth, params)
                    continue
                elif options_input == '2':
                    print('Restarting the program')
                    time.sleep(2)
                    main_menu()
                elif options_input == '3':
                    print('Closing program.')
                    exit()
                else:
                    print('Enter a valid input.')
                    continue

main_menu()
