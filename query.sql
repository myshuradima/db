
--Запит 1

select production_company.name
, count(film_company.film_id)as number_of_films
from production_company left join film_company on production_company.company_id = film_company.company_id
group by production_company.name, production_company.company_id
order by number_of_films DESC;

--Запит 2

select genres.name
, count(film_genre.film_id) as number_of_genres
, count(film_genre.film_id)/(select count(*) from film_genre) * 100 || '%' at_all
from genres left join film_genre on genres.genre_id = film_genre.genre_id
group by genres.name, genres.genre_id
order by number_of_genres desc;


--Запит 3

set serveroutput on
declare 
cursor film_cursor is (select original_title, release_date from film);
v_month VARCHAR2(30);
begin
    for record in film_cursor
        loop
            v_month := extract(month from record.release_date);
            if v_month in ('12', '1', '2')
            then
                DBMS_OUTPUT.PUT_LINE (record.original_title || ': Winter ' || EXTRACT(year from record.release_date));
            ELSIF v_month in ('3', '4', '5')
            then 
                DBMS_OUTPUT.PUT_LINE (record.original_title || ': Spring ' || EXTRACT(year from record.release_date));
            ELSIF v_month in ('6', '7', '8')
            then 
                DBMS_OUTPUT.PUT_LINE (record.original_title || ': Summer ' || EXTRACT(year from record.release_date));
            ELSE 
                DBMS_OUTPUT.PUT_LINE (record.original_title || ': Autumn ' || EXTRACT(year from record.release_date));
            END IF;
        end loop;
end;
