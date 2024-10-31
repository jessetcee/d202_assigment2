-- SQLite
-- select * from TemperatureReadings

-- delete from sensors where id BETWEEN 3 and 12
-- go
update sensors 
set sensor_name = "Palmerston North"
where id ="2"
go
select * from sensors
go