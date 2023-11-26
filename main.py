# David Barton (theDavidBarton@AOL.com) © 2023
# Test Automation Engineer coding challenge - Formula One
import json
import os
import re
import platform
import subprocess
import urllib.request
from bs4 import BeautifulSoup
import requests

resp = requests.get('https://hu.wikipedia.org/wiki/Formula%E2%80%931')
soup = BeautifulSoup(resp.text, 'html.parser')

# identify required soups from tables based on content specific to them.
# note: later this can be refactored to more robust identification
tables = soup.css.select('.wikitable')
for table in tables:
    if re.search('Pilóta.Név', str(table)):
        drivers_table = table.tbody
        break

for table in tables:        
    if re.search('Zászló', str(table)):
        flag_rules_table = table.tbody
        break

# init list to filter images later to 'identified' folder
# it will be populated with: teams, engines and driver names
filter_for_identified_images = []

# 👪 teams/constructors and engines
def teams_function():
    # collect all team/engine names from the infobox, e.g.:
    # infobox row contains: "Csapatok 10 (Mercedes, Red Bull, Ferrari..." --> team
    # infobox row contains: "Motorok 4 (Ferrari, Mercedes, Renault..." --> engine
    teams = [{ 'teams' : [], 'engines' : [] }]
    team_info_rows = soup.css.select('.infobox tr')
    for t_row in team_info_rows:
        if re.search('Csapatok', str(t_row)):
            team_links = t_row.find_all('a')
            for team in team_links:
                filter_for_identified_images.append(team.text)
                teams[0]['teams'].append(team.text)

        elif re.search('Motorok', str(t_row)):
            engine_links = t_row.find_all('a')
            for engine in engine_links:
                filter_for_identified_images.append(engine.text)
                teams[0]['engines'].append(engine.text)

    return teams


# 🏎️ drivers
def drivers_function():
    # collect the driver numbers, names & teams for active drivers about the current year
    drivers = []
    def scrape_driver_team(url_path):
        # visit the page of the driver & scrape team, e.g.:
        # 'https://hu.wikipedia.org' + '/wiki/Pierre_Gasly'
        # infobox row contains: "Csapata FRA Alpine (2023–)" --> Alpine
        resp = requests.get('https://hu.wikipedia.org' + url_path)
        soup = BeautifulSoup(resp.text, 'html.parser')
        driver_info_rows = soup.css.select('.infobox tr')
        for dr_row in driver_info_rows:
            if re.search('Csapata', str(dr_row)):
                return dr_row.find_all('a')[1].text.strip()

    def check_inactive_period(last_column):
        # last character should be a '–' if the number is currently active, e.g.:
        # 1. Sebastian Vettel 2011–2014 [inactive]
        # 1. Max Verstappen 2022– [active]
        if last_column[-1] != '–': return True
        else: return False

    for driver_row in drivers_table.find_all('tr'):
        columns = driver_row.find_all('td')
        if len(columns) == 4:
            driver_number = columns[0].text.strip()
            driver_name = columns[2].text.strip()
            driver_team = scrape_driver_team(columns[2].a.get('href'))
            if check_inactive_period(columns[-1].text.strip()):
                continue
            filter_for_identified_images.append(driver_name)
            drivers.append({ 'driver_name' : driver_name , 'driver_number' : driver_number,'driver_team' : driver_team })
        elif len(columns) == 3:
            # driver_number remains the previous value to handle spanrow=2
            driver_name = columns[1].text.strip()
            driver_team = scrape_driver_team(columns[1].a.get('href'))
            if check_inactive_period(columns[-1].text.strip()):
                continue
            filter_for_identified_images.append(driver_name)
            drivers.append({ 'driver_name' : driver_name , 'driver_number' : driver_number,'driver_team' : driver_team })
        elif len(columns) == 2:
            # driver_number remains the previous value to handle spanrow=2
            driver_name = columns[0].text.strip()
            driver_team = scrape_driver_team(columns[0].a.get('href'))
            if check_inactive_period(columns[-1].text.strip()):
                continue
            filter_for_identified_images.append(driver_name)
            drivers.append({ 'driver_name' : driver_name , 'driver_number' : driver_number,'driver_team' : driver_team })
    
    return(drivers)


# 🏁 flag_rules
def flag_rules_function():
    # collect the flag rules from the responsible table
    # as an extra: a flag name is also cleaned from the image URL
    flags = []
    for flag_row in flag_rules_table.find_all('tr'):
        columns = flag_row.find_all('td')
        if len(columns) == 2:
            flag_image_url = columns[0].figure.a.img.get('src')
            flag_name = flag_image_url.split('/')[-2].replace('.svg', '').replace('_', ' ')
            flag_image = 'flags/' + flag_image_url.split('/')[-1]
            description = columns[1].text.strip()
            flags.append({ 'flag_name' : flag_name, 'flag_image' : flag_image, 'description' : description })
    
    return(flags)


# 🖼️ images
def images_function():
    # collect, sort & download images
    images = []
    def sort_images(image_url, img_description):
        # sort images into 3 folders based on their descriptions and content
        for filter_element in filter_for_identified_images:
            if filter_element in img_description: 
                return 'identified/'
        if '_flag' in image_url:
            return 'flags/'
        else:
            return 'not_identified/'

    def images_download(image_url, image_path):
        # download images to their desired folders
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        try:
            resp = urllib.request.urlopen('https:' + image_url)
            data = resp.read()
            with open(image_path, 'wb') as f:
                f.write(data)
            return len(data)
        except Exception:
            return 0

    wiki_images = soup.css.select('figure img')
    for img in wiki_images:
        image_url = img.get('src')
        img_description = img.find_parent('figure').figcaption.text.strip()
        image_name = image_url.split('/')[-1]
        image = sort_images(image_url, img_description) + image_name # 👈 image_path
        resolution = img.get('width') + 'x' + img.get('height')
        image_size = images_download(image_url, image) # 👈 download happens here
        image_extension = image_name.split('.')[-1].lower()
        images.append({ 'image' : image, 'img_description' : img_description, 'resolution' : resolution, 'image_size' : image_size, 'image_extension' : image_extension })

    return images


# 🏒 JSON file
def json_create_function():
    print('# David Barton (theDavidBarton@AOL.com) © 2023\n# Test Automation Engineer coding challenge - Formula One\n\n[init script...]')
    
    print('* teams being collected...')
    teams = teams_function()
    print('* drivers being collected (slower)...')
    drivers = drivers_function()
    print('* flag rules being collected...')
    flag_rules = flag_rules_function()
    print('* images being collected & downloaded (slower)...')
    images = images_function()
    
    data = {
        'teams' : teams,
        'drivers' : drivers,
        'flag_rules' : flag_rules,
        'images' : images,
    }

    print('* json file being created...')
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    return data


# 📈 stats
def stats_function(data):
    # statistics calculations
    # the function also executes the bash or batch script to generate stats.txt
    resolutions_calculated = []
    resolutions_list = []
    sizes = []

    number_of_identified_images = 0
    number_of_not_identified_images = 0
    for img in data['images']:
        # two same-length arrays populated with resolutions
        # so later the script can match the original resolution
        # with the calculated (multiplied) value
        resolutions_calculated.append(int(img['resolution'].split('x')[0]) * int(img['resolution'].split('x')[1]))
        resolutions_list.append(img['resolution'])
        # an array is populated with all of the image sizes
        sizes.append(int(img['image_size']))

        # count identified/not identified images
        if 'not_identified' in img['image']:
            number_of_not_identified_images += 1
        else: 
            number_of_identified_images += 1

    number_of_drivers_in_the_championship = len(data['drivers'])
    number_of_engine_suppliers = len(data['teams'][0]['engines'])
    number_of_images = len(data['images'])
    size_of_all_images = sum(sizes) * 0.001
    average_size_of_images = sum(sizes)/len(sizes) * 0.001
    # calculate resolutions
    highest_resolution_raw = max(resolutions_calculated)
    lowest_resolution_raw = min(resolutions_calculated)

    highest_resolution = resolutions_list[resolutions_calculated.index(highest_resolution_raw)]
    lowest_resolution = resolutions_list[resolutions_calculated.index(lowest_resolution_raw)]

    print('\n'.join([
        '\n#############################################',
        '1. number of drivers in the championship: ' + str(number_of_drivers_in_the_championship),
        '2. number of engine suppliers: ' + str(number_of_engine_suppliers),
        '3. number of images: ' + str(number_of_images),
        '4. number of identified images: ' + str(number_of_identified_images),
        '5. number of not identified images: ' + str(number_of_not_identified_images),
        '6. size of all images: ' + str(size_of_all_images),
        '7. average size of images: ' + str(average_size_of_images),
        '8. highest resolution: ' + str(highest_resolution),
        '9. lowest resolution: ' + str(lowest_resolution),
        '#############################################\n',
    ]))
    subprocess_parameters = [
        str(number_of_drivers_in_the_championship),
        str(number_of_engine_suppliers),
        str(number_of_images),
        str(number_of_identified_images),
        str(number_of_not_identified_images),
        str(size_of_all_images),
        str(average_size_of_images),
        str(highest_resolution),
        str(lowest_resolution)
    ]

    if platform.system() == 'Linux':
        subprocess.run(['./generate_stat.sh'] + subprocess_parameters)
    elif platform.system() == 'Windows':
        subprocess.run(['generate_stat.bat'] + subprocess_parameters)
    else:
        print('* untested operating system: stat.txt won\'t be created')


# generate data JSON and stat text file
data = json_create_function()
print('* stats & txt file being created...')
stats_function(data)
