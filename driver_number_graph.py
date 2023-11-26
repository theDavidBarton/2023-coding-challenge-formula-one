# David Barton (theDavidBarton@AOL.com) © 2023
# Test Automation Engineer coding challenge - Formula One
import re
from bs4 import BeautifulSoup
import plotly.graph_objects as go
import requests

resp = requests.get('https://hu.wikipedia.org/wiki/Formula%E2%80%931')
soup = BeautifulSoup(resp.text, 'html.parser')

# identify the required table
# note: later this can be refactored to more robust identification
tables = soup.css.select('.wikitable')
for table in tables:
    if re.search('Pilóta.Név', str(table)):
        drivers_table = table.tbody
        break


# 🏎️1️⃣ driver numbers & years
def numbers_with_years_function():
    # collect and pair numbers with years

    def retrieve_years_from_interval(interval):
        # most years are displayed as intervals like "2010, 2015–2022"
        # we want to retrieve the individual years from these as:
        # [2010, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
        individual_years = []

        current_year = 2023

        # extracting comma-separated years & intervals for iteration
        for part in interval.split(','):
            case_1 = re.match('^\\d\\d\\d\\d$', part.strip())
            case_2 = re.match('\\d\\d\\d\\d–\\d\\d\\d\\d', part.strip())
            case_3 = re.match('\\d\\d\\d\\d–$', part.strip())
            # case 1: 2009
            if case_1:
                individual_years.append([int(part)])
            # case 2: 2011–2014
            elif case_2:
                year_start = int(case_2[0].split('–')[0])
                year_end = int(case_2[0].split('–')[1])
                individual_years.append(list(range(year_start, year_end + 1)))
            # case 3: 2011–
            elif case_3:
                year_start = int(case_3[0].split('–')[0])
                individual_years.append(
                    list(range(year_start, current_year + 1))) # 7. https://sparkbyexamples.com/python/convert-a-nested-list-into-a-flat-list-in-python
        flattened_array = sum(individual_years, [])

        return flattened_array

    numbers_with_years = {}
    for driver_row in drivers_table.find_all('tr'):
        try:
            columns = driver_row.find_all('td')
            if len(columns) == 4:  # no rowspans, all four columns are available
                driver_number = int(columns[0].text.strip())
                years = retrieve_years_from_interval(columns[-1].text.strip())
                numbers_with_years[driver_number] = years
            else:
                # driver_number remains the previous value to handle rowspan=2
                # also we concat the previous year list with the new one to group by driver number
                new_years = retrieve_years_from_interval(
                    columns[-1].text.strip())
                years = years + new_years
                years.sort()
                numbers_with_years[driver_number] = years
                if len(columns) == 3:
                    # in case of two rowspans: driver_number needs to be incremented
                    # the edge cases are: #5 and #6
                    driver_number += 1

                years = []  # reset array
        except Exception:
            pass  # handling the heading row, we can swallow the exception safely

    return numbers_with_years


# 📈 draw a graph with Plotly
def draw_graph_function(data):
    # y axis: all driver numbers present in the table
    driver_numbers = list(data.keys())
    # x axis: length of years for each driver numbers
    number_of_years = [len(data[key]) for key in driver_numbers]

    fig = go.Figure(data=[go.Bar(
        x=number_of_years, y=driver_numbers, orientation='h', marker={'color': 'red'})])
    fig.update_layout(
        title='🏎️ Driver numbers & number of years in use',
        xaxis={'title': 'Number of years',
               'automargin': True, 'tickfont': {'size': 10}},
        yaxis={'title': 'Driver numbers',
               'automargin': True, 'tickfont': {'size': 10}},
        bargap=0,
        plot_bgcolor='black',
        paper_bgcolor='black',
        font={'size': 18, 'color': 'white'}
    )
    fig.write_html('tmp.html', auto_open=True)


print('# David Barton (theDavidBarton@AOL.com) © 2023\n# Test Automation Engineer coding challenge - Formula One\n\n[init script...]')

print('* data being collected...')
data = numbers_with_years_function()
for key, value in data.items(): print(key, value)

print('* graph being created...')
draw_graph_function(data)
