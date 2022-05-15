/*
* source: https://github.com/plkpiotr/soccer-league
* Modified and extended by Filip Kovacevic on 12.05.2022
*/ 

create table stadium (
	id_stadium smallint primary key, -- missing
	full_name varchar(32) not null, -- missing
	capacity integer not null -- missing
);

create table team (
	id_team smallint primary key, -- auto incr
	id_stadium smallint references stadium(id_stadium), -- missing
	club varchar(50) not null, --df_full_premierleague.home_team, --df_full_premierleague.away_team
	shorthand varchar(3) --unique not null check(length(shorthand) = 3)
);

create table player (
	id_player smallint primary key, --auro incr
	name varchar(50), --player_name
	kit smallint, --not null check(kit between 1 and 99), --missing
	country varchar(32) -- not null --missing
); 

create table contract (
    id_player smallint not null references player(id_player),
	id_team smallint not null references team(id_team),
    transfer_period varchar(15) not null check (transfer_period = 'Summer' or transfer_period = 'Winter'), --english_premiere_league.transfer_period
    season varchar(15) not null, --english_premiere_league.season
	position varchar(30) not null check(position='Centre-Forward' --english_premiere_league.position
                                        OR position='Goalkeeper'
                                        OR position='Central Midfield'
                                        OR position='Defensive Midfield'
                                        OR position='Left-Back'
                                        OR position='Right Winger'
                                        OR position='Attacking Midfield'
                                        OR position='Centre-Back'
                                        OR position='Second Striker'
                                        OR position='Right-Back'
                                        OR position='Right Midfield'
                                        OR position='Left Midfield'
                                        OR position='Left Winger'
                                        OR position='attack'),
    year numeric(4) --english_premiere_league.year

);

create table match (
	id_match smallint primary key, --auto incr
	id_home smallint not null references team(id_team), --df_full_premierleague.home_team
	id_away smallint not null references team(id_team), --df_full_premierleague.away_team
	id_stadium smallint references stadium(id_stadium), --missing 
	date_time timestamp not null, --df_full_premierleague.date
	attendance integer --missing
);

create table result (
	id_match smallint primary key references match(id_match),
	home smallint not null check(home >= 0),--EO.FTHG
	away smallint not null check(away >= 0) --EO.FTAG
);

/*create table score (
	id_score smallint primary key, --auto incr
	id_match smallint not null references match(id_match),
	id_team smallint not null references team(id_team),
	id_player smallint not null references player(id_player),
	goals smallint not null check(goals >= 0) --df_full_premierleague.goal_home_ft + df_full_premierleague.goal_away_ft
	assists smallint not null check(assists >= 0) --missing
);*/

create table platformUser (
    id_user smallint primary key, --auto incr
    name varchar(50) not null -- synthetic
);

create table bet (
    id_bet smallint primary key, --auto incr
    id_match smallint not null references match(id_match),
    bet_offered timestamp not null, -- E0.Date, E0.Time
    home_win_odds decimal not null, --E0.B365H		
    draw_odds decimal not null, --E0.B365D
    away_win_odds decimal not null, --E0.B365A
    betting_provider varchar(50) not null -- E0.B365H column name substring
);

create table user_bet (
    id_user smallint not null references platformUser(id_user),
    id_bet smallint not null references bet(id_bet),
    tip varchar(1) not null check(tip='H' OR tip='D' OR tip ='A'), --synthetic
    tip_timestamp timestamp not null, --synthetic
    primary key(id_user, id_bet, tip_timestamp)
);


