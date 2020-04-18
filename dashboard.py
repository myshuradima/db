import chart_studio

chart_studio.tools.set_credentials_file(username='myshuradima', api_key='igkva9kCH1mZNdXwBIKP')


import cx_Oracle
import chart_studio.plotly as py
import plotly.graph_objs as go
import re
import chart_studio.dashboard_objs as dashboard


def fileId_from_url(url):
    """Return fileId from a url."""
    raw_fileId = re.findall("~[A-z.]+/[0-9]+", url)[0][1:]
    return raw_fileId.replace('/', ':')


connection = cx_Oracle.connect("DB_KPI/DB_KPI@localhost:1521/xe")

cursor = connection.cursor()

""" create plot 1"""

query = """
SELECT PRODUCTION_COMPANY.NAME
, COUNT(FILM_COMPANY.FILM_ID) AS NUMBER_OF_FILMS
FROM PRODUCTION_COMPANY LEFT JOIN FILM_COMPANY ON PRODUCTION_COMPANY.COMPANY_ID = FILM_COMPANY.COMPANY_ID
GROUP BY PRODUCTION_COMPANY.NAME, PRODUCTION_COMPANY.COMPANY_ID
ORDER BY NUMBER_OF_FILMS DESC """


cursor.execute(query)

company = []
films_amount = []

for row in cursor:
    print("Customer name: ", row[1], " and his order sum: ", row[0])
    if int(row[1]) > 50:
        company += [row[0]]
        films_amount += [row[1]]

data = [go.Bar(
        x=company,
        y=films_amount
)]

layout = go.Layout(
    title='Companies and amount of films',
    xaxis=dict(
        title='Companies',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Amount of films',
        rangemode='nonnegative',
        autorange=True,
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)

companies_films_amount = py.plot(fig, filename='companies-films-amount')

""" create plot 2"""

query = """
select genres.name
, count(film_genre.film_id) as number_of_genres
from genres left join film_genre on genres.genre_id = film_genre.genre_id
group by genres.name, genres.genre_id
order by number_of_genres desc """


cursor.execute(query)

genre = []
films_amount = []

for row in cursor:
    print("Customer name: ", row[1], " and his order sum: ", row[0])
    genre += [row[0]]
    films_amount += [row[1]]

pie = go.Pie(
        labels=genre,
        values=films_amount
)
genres_films_amount = py.plot([pie], filename='genres-films-amount')

""" create plot 3"""

cursor.execute("""
select sum(amount)
, 'Summer' as time 
, film_year
from(
select count(original_title) as amount 
,extract(month from release_date) as film_month
,extract(year from release_date) as film_year
from film
group by extract(year from release_date), extract(month from release_date))
where film_month in ('6', '7', '8')
group by film_year

union

select sum(amount)
, 'Winter' as time
,film_year
from(
select count(original_title) as amount 
,extract(month from release_date) as film_month
,extract(year from release_date) as film_year
from film
group by extract(year from release_date), extract(month from release_date))
where film_month in ('12', '1', '2')
group by film_year

union

select sum(amount)
, 'Spring' as time
, film_year
from(
select count(original_title) as amount 
,extract(month from release_date) as film_month
,extract(year from release_date) as film_year
from film
group by extract(year from release_date), extract(month from release_date))
where film_month in ('3', '4', '5')
group by film_year

union

select sum(amount)
, 'Autumn' as time
, film_year
from(
select count(original_title) as amount 
,extract(month from release_date) as film_month
,extract(year from release_date) as film_year
from film
group by extract(year from release_date), extract(month from release_date))
where film_month in ('9', '10', '11')
group by film_year
order by film_year
""")
release_dates = []
amount_of_films = []

for row in cursor:
    if row[2] >1990:
        print("Date ", row[1] + str(row[2]), " sum: ", row[0])
        release_dates += [row[1] + " " + str(row[2])]
        amount_of_films += [row[0]]

order_date_prices = go.Scatter(
    x=release_dates,
    y=amount_of_films,
    mode='lines+markers'
)
data = [order_date_prices]
release_date_films = py.plot(data, filename='amount-of-films-by-dates')

"""--------CREATE DASHBOARD------------------ """

my_dboard = dashboard.Dashboard()

companies_films_amount_id = fileId_from_url(companies_films_amount)
genres_films_amount_id = fileId_from_url(genres_films_amount)
release_date_films_id = fileId_from_url(release_date_films)

box_1 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': companies_films_amount_id,
    'title': 'Companies and amount of their films'
}

box_2 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': genres_films_amount_id,
    'title': 'Genres and percent of films in this genres '
}

box_3 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': release_date_films_id,
    'title': 'Amount of films by date'
}

my_dboard.insert(box_1)
my_dboard.insert(box_2, 'below', 1)
my_dboard.insert(box_3, 'left', 2)

py.dashboard_ops.upload(my_dboard, 'Lab 2 Dashboard')