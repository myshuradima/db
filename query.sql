

--Çàïèò 1

select production_company.name
, count(film_company.film_id)as number_of_films
from production_company left join film_company on production_company.company_id = film_company.company_id
group by production_company.name, production_company.company_id
order by number_of_films DESC;

--Çàïèò 2

select genres.name
, count(film_genre.film_id) as number_of_genres
, count(film_genre.film_id)/(select count(*) from film_genre) * 100 || '%' at_all
from genres left join film_genre on genres.genre_id = film_genre.genre_id
group by genres.name, genres.genre_id
order by number_of_genres desc;


--Çàïèò 3

select sum(amount)
, 'summer' as time 
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
, 'spring' as time
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
, 'autumn' as time
, film_year
from(
select count(original_title) as amount 
,extract(month from release_date) as film_month
,extract(year from release_date) as film_year
from film
group by extract(year from release_date), extract(month from release_date))
where film_month in ('9', '10', '11')
group by film_year;
