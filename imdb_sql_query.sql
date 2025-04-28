use imdb;
select * from scarb_imdb;

# 1.Top 10 movies by rating and voting count
select Titile, Ratings, Voting_count from scarb_imdb order by Ratings desc, Voting_count desc limit 10;

#2.Genre Distribution
select Genre,count(*) as movies_genre_distribution from scarb_imdb group by Genre;

#3.Average duration by genre
select Genre,Avg(Timings) as average_duration from scarb_imdb group by Genre;

#4.Voting Trends by Genre
select Genre,Avg(Voting_count) as Voting_trends from scarb_imdb group by Genre;

#5.Rating Distribution
select Genre,avg(Ratings) as Rating_distribution  from scarb_imdb group by Genre;

#6.top-rated movie for each genre
select Titile, Genre, Ratings from scarb_imdb s
where (Genre, Ratings) in (select Genre, MAX(Ratings) from scarb_imdb group by Genre)
order by Ratings desc;

#7.Most Popular Genres by Voting
select Genre,avg(Voting_count) as popular_genre from scarb_imdb group by Genre;

#8.shortest and longest movies
select Titile, Timings, case 
when Timings = (select max(Timings) from scarb_imdb) then 'Highest Timing'
when Timings = (select min(Timings) from  scarb_imdb) then 'Lowest Timing' end as Timing_Type
from  scarb_imdb where Timings = (select max(Timings) from  scarb_imdb) or Timings = (select MIN(Timings) from  scarb_imdb);

#9. Ratings by genre
select Genre,avg(Ratings) as Rating_genre  from scarb_imdb group by Genre;