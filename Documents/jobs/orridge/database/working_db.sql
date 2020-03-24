DROP DATABASE if exists orridgedb;
CREATE DATABASE orridgedb;
GRANT ALL ON orridgedb.* TO htran@localhost IDENTIFIED BY "htran";
FLUSH PRIVILEGES;
GRANT CREATE TEMPORARY TABLES ON orridgedb.* TO htran@localhost IDENTIFIED BY "htran";
FLUSH PRIVILEGES;
ALTER DATABASE orridgedb DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
USE orridgedb;

-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.0.22-community-nt


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema orridgedb
--

-- CREATE DATABASE /*!32312 IF NOT EXISTS*/ orridgedb;


--
-- Table structure for table `orridgedb`.`accounts`
--
drop table company;
CREATE TABLE company(
	id int(11) unsigned NOT NULL auto_increment,
	name varchar(250),
	registration varchar(10),
	PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert  into company (name, registration) values 
('Home', '00000000'),
('Airport', '00000001'),
('Railway Station', '00000002'),
('Underground Station', '00000003'),
('Bus Station', '00000004'),
('Bus Stop', '00000005'),
('Coach Station', '00000006'),
('Coach Stop', '00000007'),
('Taxi', '00000006'),
('Co-Op Group Limited','10653796'),
('Harvey Nichols Group Limited','72539'),
('Homebase Group Limited','1460756'),
('Paperchase Limited','3283485'),
('Poundland Limited','2495645'),
('Superdrug','807043'),
('Wilkinson Group PLC','2669929'),
('Waterstones Booksellers Limited','NF002993'),
('Evans Cycles Limited','06649810'),
('Top Shop Group Limited','10598692'),
('Space NK Limited','02773985'),
('Euro Car Parts Limited','02680212'),
('Outdoor And Cycle Concepts Limited','03382348'),
('Johnson & Johnson Vision Care (Ireland)','IE210174'),
('WH Smith Plc','05202036'),
('Savers Health & Beauty Limited','02202838'),

;

drop table addresses;
CREATE TABLE addresses(
	id int(11) unsigned NOT NULL auto_increment,    
    company_id int(11) unsigned NOT NULL,
	address varchar(250),
	postcode varchar(25),
	PRIMARY KEY (id),
	
    CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES company(id)
	
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert  into addresses (company_id, address, postcode) values 
((select id from company where instr( name, "Superdrug") > 0), 'Units 1-4, Trinity Parade High Street, Hounslow, Middlesex', 'TW3 1HG'),
((select id from company where instr( name, "Superdrug") > 0), '297-301, Station Rd, Harrow, Middlesex', 'HA1 2TA'),
((select id from company where instr( name, "Poundland") > 0), 'Limited, 163-165 Balham High Road, Balham', 'SW12 8BG'),
((select id from company where instr( name, "Poundland") > 0), '78-80 High Street, The Exchange, Putney, London', 'SW15 1RB'),
((select id from company where instr( name, "Homebase") > 0), 'Weir Road Wimbledon, London', 'SW19 8UG'),
((select id from company where instr( name, "Homebase") > 0), 'The Causeway, Staines', 'TW18 3AP'),
((select id from company where instr( name, "Homebase") > 0), '10 Beckenham Hill Road, Catford', 'SE6 3NU'),
((select id from company where instr( name, "Homebase") > 0), 'Kingston, 229-253 Kingston Road, New Malden', 'KT3 3SW'),
((select id from company where instr( name, "Paperchase") > 0), '62 Northcote Road, London', 'SW11 1PA'),
((select id from company where instr( name, "Paperchase") > 0), '346 - 348 High Road, Chiswick, London', 'W4 5TA'),
((select id from company where instr( name, "Wilkinson") > 0), '90- 94 The Broadway West, Ealing', 'W13 0SA'),
((select id from company where instr( name, "Co-Op") > 0), 'Retail, (Raynes Park), 68 - 74 Coombe Lane, Raynes Park, London', 'SW20 0AX'),
((select id from company where instr( name, "Co-Op") > 0), 'Retail, (fulham North End Road), North End Road, London', 'SW6 1NJ'),
((select id from company where instr( name, "Co-Op") > 0), 'Food, 276-288 Kingston Road, Wimbledon Chase. London', 'SW20 8LX'),
((select id from company where instr( name, "Harvey") > 0), '109 - 125 Knightsbridge, London', 'SW1X 7RJ'),
((select id from company where instr( name, "Waterstones") > 0), '82 Gower Street, London', 'WC1E 6EQ'),
((select id from company where instr( name, "Waterstones") > 0), 'Hatchards Unit 1, St Pancras Euston Road, London', 'N1C 4QP'),
((select id from company where instr( name, "Evans") > 0), '48 Richmond Road, Kingston, Surrey', 'KT2 5EE'),
((select id from company where instr( name, "Top Shop") > 0), 'Oxford Circus, 36-38 Great Castle Street, West End, Greater London', 'W1W 8LG'),
((select id from company where instr( name, "Space NK") > 0), 'Unit 6, 4 Cathedral Walk Cardinal Place, Victoria, London', 'SW1E 5JH'),
((select id from company where instr( name, "Euro Car") > 0), 'Fulton Road, Wembley Industrial Estate, Wembley, Middlesex', 'HA9 0TF'),
((select id from company where instr( registration, "00000000") > 0), '21 Fox House, Maysoule Road, Battersea, London', 'SW11 2BX'),
((select id from company where instr( name, "Railway Station") > 0), 'Clapham Junction Railway Station, St Johns Hill, Greater London', 'SW11 2QP'),
((select id from company where instr( name, "Railway Station") > 0), 'Harrow & Wealdstone Railway Station, Harrow, London', 'HA3 5AG'),
((select id from company where instr( name, "Railway Station") > 0), 'Balham Railway Station, Balham High Road, Balham, London' , 'SW12 9SG'),
((select id from company where instr( name, "Railway Station") > 0), 'Egham Railway Station,  Station Road, Egham, Surrey' , 'TW20 9LB'),
((select id from company where instr( name, "Railway Station") > 0), 'Earlsfield Railway Station, 513 Garratt Lane, Earlsfield, London' , 'SW18 4SW'),
((select id from company where instr( name, "Railway Station") > 0), 'Putney Railway Station, 165 Putney High Street, Putney; London' , 'SW15 1RT'),
((select id from company where instr( name, "Railway Station") > 0), 'Surrey Quays Railway Station, Lower Road Rotherhithe Greater London' , 'SE16 2UE'),
((select id from company where instr( name, "Railway Station") > 0), 'Brentford Railway Station, Station Road, Brentford' , 'TW8 8DT'),
((select id from company where instr( name, "Railway Station") > 0), 'Bromley South Railway Station, Station Approach, High Street, Bromley, London' , 'BR1 1LX'),
((select id from company where instr( name, "Railway Station") > 0), 'Beckenham Hill Railway Station, Beckenham Hill Road, Beckenham, London' , 'SE6 3RE'),
((select id from company where instr( name, "Railway Station") > 0), 'Victoria Railway Station, Victoria Street, London' , 'SW1E 5ND'),
((select id from company where instr( name, "Underground Station") > 0), 'Warren Street Underground Station, Tottenham Court Rd, London' , 'NW1 3AA'),
((select id from company where instr( name, "Railway Station") > 0), 'Kew Bridge Railway Station, Kew Bridge, London' , 'TW8 9QS'),
((select id from company where instr( name, "Railway Station") > 0), 'Kings Cross Railway Station, Euston Road, London' , 'N1 9AL'),
((select id from company where instr( name, "Railway Station") > 0), 'Wimbledon Chase Railway Station, Kingston Road, Wimbledon, London' , 'SW20 8JT'),
((select id from company where instr( name, "Railway Station") > 0), 'Raynes Park Railway Station, Station Approach, Coombe Lane, London' , 'SW20 0JY'),
((select id from company where instr( name, "Railway Station") > 0), 'Wembley Central Railway Station, 7AF, High Road, Wembley, London' , 'HA9 7AJ'),
((select id from company where instr( name, "Homebase") > 0), 'Wembley Park Underground Station, Bridge Road, Wembley, London' , 'HA9 9AA'),
((select id from company where instr( name, "Homebase") > 0), '241 Kidbrooke Park Road, Kidbrooke, London' , 'SE3 9PP'),
((select id from company where instr( name, "Outdoor And Cycle Concepts") > 0), 'Cotswold Outdoor, Cycle Surgery, 658-662 Fulham Road, London' , 'SW6 5RX'),
((select id from company where instr( name, "Superdrug") > 0), '2-8, Station Road, Hayes, London' , 'UB3 4DA'),
((select id from company where instr( name, "Johnson & Johnson Vision ") > 0), 'Johnson & Johnson Vision Products European Vision Centre, Summit Business Park, 8 Hanworth Road Sunbury On Thames Middlesex, 01932 733500' , 'TW16 5DB'),
((select id from company where instr( name, "Outdoor And Cycle Concepts") > 0), 'Cotswold Outdoor, 56-58 Garratt Lane, Southside Shopping Centre, Wandsworth, London' , 'SW118 4TF'),
((select id from company where instr( name, "Superdrug") > 0), '138-140 Rushey Green, Catford, London', 'SE6 4HQ'),
((select id from company where instr( name, "Co-Op") > 0), '471-487 Kings Road, Chelsea, London', 'SW10 0LU'),
((select id from company where instr( name, "WH Smith") > 0), 'Victoria Station, London', 'SW1V 1JT'),
((select id from company where instr( name, "Poundland") > 0), '530-536 High Rd, London', 'N17 9SX'),
((select id from company where instr( name, "Savers Health & Beauty") > 0), '118-120 High Street, Acton, London', 'W3 6QX'),
((select id from company where instr( name, "Waterstones") > 0), 'Unit S 9, Bentalls Shopping Centre, Wood Street, Kingston Upon Thames, Surrey', 'KT1 1TR'),
((select id from company where instr( name, "Waterstones") > 0), 'The Grand Building, Trafalgar Square, London, London', 'WC2N 5EJ'),
((select id from company where instr( name, "Superdrug") > 0), '228 Southwark Park Road, Bermondsey, London', 'SE16 3RW'),
((select id from company where instr( name, "Superdrug") > 0), '271-273 City Road, Islington, London', 'EC1V 1LA'),
((select id from company where instr( name, "Homebase") > 0), 'Swandon way, Wandsworth, London', 'SW18 1EW'),

;

drop table jobs;
CREATE TABLE jobs(
	id int(11) unsigned NOT NULL,
	start_date DATE,
	start_time TIME,
	end_date DATE,
	end_time TIME,
    location int(11) unsigned not null,    
    predicted_duration DECIMAL(7, 2),
	predicted_amount DECIMAL(7, 2),
    actual_duration DECIMAL(7, 2),
    paid_amount DECIMAL(7, 2),
    paid_date DATE,
    reference varchar(250),    
    PRIMARY KEY (id)	,
    
    CONSTRAINT fk_location_id FOREIGN KEY (location) REFERENCES addresses(id)
    ON DELETE CASCADE 
    ON UPDATE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert  into jobs (id, start_date, start_time, end_date, end_time, location) values 
(985323, '2017-08-29', '16:30', '2017-08-30', '00:50', (select id from addresses where postcode = "TW3 1HG")),
(970539, '2017-09-04', '17:30', '2017-09-05', '01:30', (select id from addresses where postcode = "SW12 8BG")),
(985276, '2017-09-05', '16:30', '2017-09-06', '03:15', (select id from addresses where postcode = "HA1 2TA")),
(966946, '2017-09-06', '17:00', '2017-09-06', '22:21', (select id from addresses where postcode = "SW11 1PA")),
(987914, '2017-09-07', '16:30', '2017-09-07', '23:20', (select id from addresses where postcode = "W13 0SA")),
(974102, '2017-09-11', '14:00', '2017-09-11', '21:30', (select id from addresses where postcode = "SW19 8UG")),
(974103, '2017-09-12', '14:00', '2017-09-12', '18:00', (select id from addresses where postcode = "TW18 3AP")),
(957597, '2017-09-14', '06:00', '2017-09-14', '15:15', (select id from addresses where postcode = "SW20 0AX")),
(961097, '2017-09-17', '13:00', '2017-09-17', '22:00', (select id from addresses where postcode = "SW1X 7RJ")),
(966957, '2017-09-19', '16:00', '2017-09-19', '22:19', (select id from addresses where postcode = "W4 5TA")),
(955181, '2017-09-27', '06:00', '2017-09-27', '15:20', (select id from addresses where postcode = "SW6 1NJ")),
(962393, '2017-09-28', '20:30', '2017-09-29', '01:45', (select id from addresses where postcode = "WC1E 6EQ")),
(974115, '2017-10-03', '13:30', '2017-10-03', '19:30', (select id from addresses where postcode = "SE6 3NU")),
(980672, '2017-10-04', '18:30', '2017-10-05', '02:10', (select id from addresses where postcode = "SW15 1RB")),
(974118, '2017-10-11', '13:30', '2017-10-11', '21:43', (select id from addresses where postcode = "KT3 3SW")),
(957621, '2017-10-16', '09:55', '2017-10-16', '15:44', (select id from addresses where postcode = "SW20 8LX")),
(962384, '2017-10-17', '21:55', '2017-10-18', '00:45', (select id from addresses where postcode = "N1C 4QP")),
(972007, '2017-10-20', '07:30', '2017-10-20', '18:00', (select id from addresses where postcode = "HA9 0TF")),
(974124, '2017-10-24', '13:30', '2017-10-24', '21:30', (select id from addresses where postcode = "SE3 9PP")),
(985236, '2017-10-25', '13:30', '2017-10-26', '00:30', (select id from addresses where postcode = "UB3 4DA")),
(501321, '2017-10-27', '07:00', '2017-10-27', '15:00', (select id from addresses where postcode = "SW6 5RX")),
(501323, '2017-10-28', '07:00', '2017-10-28', '10:45', (select id from addresses where postcode = "SW118 4TF")),
----------------
(985329, '2017-10-31', '16:00', '2017-11-01', '00:57', (select id from addresses where postcode = "SE6 4HQ")),
(975572, '2017-11-03', '12:45', '2017-11-03', '22:00', (select id from addresses where postcode = "TW16 5DB")),
(975575, '2017-11-04', '11:10', '2017-11-04', '22:00', (select id from addresses where postcode = "TW16 5DB")),
(980897, '2017-11-06', '16:00', '2017-11-06', '22:09', (select id from addresses where postcode = "TW16 5DB")),
(955190, '2017-11-07', '06:00', '2017-11-07', '14:00', (select id from addresses where postcode = "SW10 0LU")),
(981506, '2017-11-08', '18:00', '2017-11-09', '02:00', (select id from addresses where postcode = "SW1V 1JT")),

(984744, '2017-11-09', '12:30', '2017-11-09', '20:35', (select id from addresses where postcode = "W3 6QX")),
(974130, '2017-11-14', '15:07', '2017-11-14', '21:35', (select id from addresses where postcode = "SW18 1EW")),
(962398, '2017-11-15', '19:45', '2017-11-16', '03:45', (select id from addresses where postcode = "WC2N 5EJ")),
(984351, '2017-11-17', '18:00', '2017-11-18', '02:00', (select id from addresses where postcode = "SE16 3RW")),

(957648, '2017-11-13', '06:00', '2017-11-13', '11:05', (select id from addresses where postcode = "EC1V 1LA")),
;

drop table transport_method;
CREATE TABLE transport_method(
    id int(11) unsigned NOT NULL auto_increment,
    method varchar(250),
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert  into transport_method(method) values 
("Air"),
("Ship"),
("Ferry"),
("Boat"),
("Train"),
("Underground"),
("Coach"),
("Bus"),
("Taxi"),
("Bike"),
("Walk")
;

drop table expense_proof_type;
CREATE TABLE expense_proof_type(
    id int(11) unsigned NOT NULL auto_increment,
    proof_type varchar(250),    
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert  into expense_proof_type(proof_type) values 
('Ticket'),
('Receipt'),
('Oyster Card')
;

drop table trip;
CREATE TABLE trip(
    id int(11) unsigned NOT NULL auto_increment,
    job_id int(11) unsigned NOT NULL,
    from_location_id int(11) unsigned,
    to_location_id int(11) unsigned,
    travel_method int(11) unsigned ,
    start_date DATE,
    start_time TIME,    
    proof_type varchar(250),
    expense_amount DECIMAL(7, 2),
    submit_date DATE,
    paid_date DATE,
    paid_reference varchar(250),
    PRIMARY KEY (id),
    
    CONSTRAINT fk_job_id FOREIGN KEY (job_id) REFERENCES jobs(id) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE,

    CONSTRAINT fk_from_location_id FOREIGN KEY (from_location_id) REFERENCES addresses(id) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE,

    CONSTRAINT fk_to_location_id FOREIGN KEY (to_location_id) REFERENCES addresses(id) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE,

    CONSTRAINT fk_travel_method FOREIGN KEY (travel_method) REFERENCES transport_method(id) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE        
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert into trip(job_id, from_location_id, to_location_id, travel_method, start_date, proof_type, expense_amount, submit_date, paid_date, paid_reference) values 
(985323, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'TW3 1HG'), (select id from transport_method where method =  'Train'),  (select start_date from jobs where id=985323), 'Ticket, Day Travelcard', 12.3,  '2017-09-10', '2017-10-06', 'Period 14 - £67.95'),
(970539, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'SW12 8BG'), (select id from transport_method where method =  'Bus'),  (select start_date from jobs where id=970539), 'Oyster and train ticket', 06.05,  '2017-09-10', '2017-10-06', 'Period 14 - £67.95'),
(985276, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'HA1 2TA'), (select id from transport_method where method =  'Bus'),  (select start_date from jobs where id=985276), 'Oyster and train ticket', 17.55,  '2017-09-10', '2017-10-06', 'Period 14 - £67.95'),
(966946, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'SW11 1PA'), (select id from transport_method where method =  'Bus'),  (select start_date from jobs where id=966946), 'Oyster', 1.5,  '2017-09-10', '2017-10-06', 'Period 14 - £67.95'),
(987914, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'W13 0SA'), (select id from transport_method where method =  'Train'),  (select start_date from jobs where id=987914), 'Oyster', 4.5,  '2017-09-10', '2017-10-06', 'Period 14 - £67.95'),
(974102, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'SW19 8UG'), (select id from transport_method where method =  'Train'),  (select start_date from jobs where id=974102), 'Oyster', 3.6,  '2017-09-18', '2017-10-06', 'Period 14 - £67.95'),
(974103, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'TW18 3AP'), (select id from transport_method where method =  'Train'),  (select start_date from jobs where id=974103), 'Oyster', 14.8,  '2017-09-18', '2017-10-06', 'Period 14 - £67.95'),
(957597, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'SW20 0AX'), (select id from transport_method where method =  'Train'),  (select start_date from jobs where id=957597), 'Oyster', 6.1,  '2017-09-18', '2017-10-06', 'Period 14 - £67.95'),
(961097, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'SW1X 7RJ'), (select id from transport_method where method =  'Bus'),  (select start_date from jobs where id=961097), 'Oyster', 6.1,  '2017-09-18', '2017-10-06', 'Period 14 - £67.95')
;

insert into trip(job_id, from_location_id, to_location_id, travel_method, start_date, proof_type, expense_amount, submit_date) values 
(966957, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'W4 5TA'), (select id from transport_method where method =  'Bus'),  (select start_date from jobs where id=966957), 'Oyster', 4.35,  '2017-10-12'),
(955181, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'SW6 1NJ'), (select id from transport_method where method =  'Bus'),  (select start_date from jobs where id=955181), 'Oyster', 0.0,  '2017-10-12'),
(962393, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'WC1E 6EQ'), (select id from transport_method where method =  'Bus'),  (select start_date from jobs where id=962393), 'Oyster', 3.9,  '2017-10-12'),
(974115, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'SE6 3NU'), (select id from transport_method where method =  'Bus'),  (select start_date from jobs where id=974115), 'Oyster', 7.85,  '2017-10-18'),
(980672, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'SW15 1RB'), (select id from transport_method where method =  'Bus'),  (select start_date from jobs where id=980672), 'Oyster', 0.0,  '2017-10-18'),
(974118, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'KT3 3SW'), (select id from transport_method where method =  'Bus'),  (select start_date from jobs where id=974118), 'Oyster', 6.85,  '2017-10-18'),
(957621, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'SW20 8LX'), (select id from transport_method where method =  'Bus'),  (select start_date from jobs where id=957621), 'Oyster', 5.7,  '2017-10-18'),

insert into trip(job_id, from_location_id, to_location_id, travel_method, start_date, proof_type, expense_amount) values
(962384, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'N1C 4QP'), (select id from transport_method where method =  'Bus'),  (select start_date from jobs where id=962384), 'Oyster', 6.6),
(972007, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'SE3 9PP'), (select id from transport_method where method =  'Underground'),  (select start_date from jobs where id=972007), 'Oyster', 5.8),

INSERT INTO `trip` (`job_id`, `from_location_id`, `to_location_id`, `travel_method`, `start_date`, `start_time`, `proof_type`, `expense_amount`) VALUES ('974124', '22', '45', '5', DATE('2017-10-24'), TIME('12:10'), 'Oyster', '6.2');

(974124, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'HA9 0TF'), (select id from transport_method where method =  'Train'),  (select start_date from jobs where id=974124), 'Oyster', 6.2),
(985236, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'UB3 4DA'), (select id from transport_method where method =  'Train'),  (select start_date from jobs where id=985236), 'Oyster', 5.25),
(501323, (select id from addresses where postcode = 'SW11 2BX'), (select id from addresses where postcode = 'SW118 4TF'), (select id from transport_method where method =  'Bus'),  (select start_date from jobs where id=501323), 'Oyster', 3.0),
;



SELECT jobs.id, jobs.start_date, jobs.start_time, company.name, addresses.address, addresses.postcode FROM company, addresses, jobs WHERE jobs.location = '13' and addresses.id = '13' and  addresses.company_id = company.id;

DROP PROCEDURE `ListAllJobs`;
DROP PROCEDURE `ListJobByID`;
delimiter $$
create procedure ListJobByID(
    in p_job_id int(11))
begin        
    SELECT jobs.id, jobs.start_date, jobs.start_time, jobs.end_date, jobs.end_time, company.name, addresses.address, addresses.postcode FROM company, addresses, jobs WHERE jobs.id=p_job_id and jobs.location = addresses.id and addresses.company_id = company.id;    
end$$

create procedure ListAllJobs()
begin        
    SELECT jobs.id, jobs.start_date, jobs.start_time, jobs.end_date, jobs.end_time, company.name, addresses.address, addresses.postcode FROM company, addresses, jobs WHERE jobs.location = addresses.id and addresses.company_id = company.id order by jobs.start_date;
end$$

delimiter ;




DROP PROCEDURE `UpdateAllJobsPrediction`;
DROP PROCEDURE `UpdateJobRecordsPredictedDurationAndAmount`;
delimiter $$
create procedure UpdateJobRecordsPredictedDurationAndAmount(
    in p_job_id int(11) unsigned,
    in p_rate decimal(7,2))    
begin
    update jobs set jobs.predicted_duration = round(time_to_sec(timediff(    
    concat(jobs.end_date, ' ', jobs.end_time), 
    concat(jobs.start_date, ' ', jobs.start_time)
    )) /3600, 2) where jobs.id = p_job_id;
    update jobs set jobs.predicted_amount = p_rate * jobs.predicted_duration where jobs.id = p_job_id;
end$$

create procedure UpdateAllJobsPrediction(
    in p_rate decimal(7,2))    
begin
    declare current_job_id int(11) unsigned;
    declare done int default false;
    declare jobid cursor for select id from jobs;
    declare continue handler for not found set done = true;
    
    open jobid;
    read_loop: loop
        fetch jobid into current_job_id;
        if done then
            leave read_loop;
        end if;
        call UpdateJobRecordsPredictedDurationAndAmount(current_job_id, p_rate);
    end loop;
end$$
delimiter ;


SELECT 
    jobs.id, jobs.start_date, jobs.start_time, jobs.end_time, sum(jobs.predicted_duration) as total_dur,  sum(jobs.predicted_amount) as total_pay 
FROM jobs WHERE 
(jobs.start_date >= date('2017-08-29')) and 
(jobs.start_date <= date('2017-09-05')) group by jobs.start_date with rollup ;


DROP PROCEDURE `SumJobsPredicted`;
delimiter $$
create procedure SumJobsPredicted(
    in p_from_date date,
    in p_to_date date )
begin
    SELECT 
        jobs.id, jobs.start_date, jobs.start_time, jobs.end_time, 
        company.name, addresses.address, coalesce(addresses.postcode, 'total'), sum(jobs.predicted_duration) as total_dur,  sum(jobs.predicted_amount) as total_pay 
    FROM company, addresses, jobs WHERE 
    (jobs.start_date >= p_from_date) and 
    (jobs.start_date <= p_to_date) and
    jobs.location = addresses.id and 
    addresses.company_id = company.id group by jobs.start_date with rollup;
end$$
delimiter ;

DROP PROCEDURE `SumJobsPredicted`;
delimiter $$
create procedure SumJobsPredicted(
    in p_from_date date,
    in p_to_date date )
begin
    SELECT 
        jobs.id, jobs.start_date, jobs.start_time, jobs.end_time, 
        company.name, addresses.address, addresses.postcode, sum(jobs.predicted_duration) as total_dur,  sum(jobs.predicted_amount) as total_pay 
    FROM company, addresses, jobs WHERE 
    (jobs.start_date >= p_from_date) and 
    (jobs.start_date <= p_to_date) and
    jobs.location = addresses.id and 
    addresses.company_id = company.id order by jobs.start_date;
end$$
delimiter ;



drop procedure `UpdateJobsEndTime`;
delimiter $$
create procedure UpdateJobsEndTime(
    in p_job_id int(11) unsigned,
    in p_end_date date)
begin
    update jobs set end_date = p_end_date where id = p_job_id;    
    call UpdateJobRecordsPredictedDurationAndAmount(p_job_id, 7.5);
end$$
delimiter ;


drop procedure `UpdateJobsEndDateAndTime`;
delimiter $$
create procedure UpdateJobsEndDateAndTime(
    in p_job_id int(11) unsigned,
    in p_end_date date,
    in p_end_time time)
begin
    update jobs set end_date = p_end_date, end_time = p_end_time where id = p_job_id;
    call UpdateJobRecordsPredictedDurationAndAmount(p_job_id, 7.5);
end$$
delimiter ;

drop procedure `UpdateJobsEndDate`;
delimiter $$
create procedure UpdateJobsEndDate(
    in p_job_id int(11) unsigned,
    in p_end_date date)
begin
    update jobs set end_date = p_end_date where id = p_job_id;
    call UpdateJobRecordsPredictedDurationAndAmount(p_job_id, 7.5);
end$$
delimiter ;


drop procedure `ListJobs`;
delimiter $$
create procedure ListJobs()
begin
    select * from jobs order by start_date;
end$$
delimiter ;

drop procedure `ListJobsByDates`;
delimiter $$
create procedure ListJobsByDates(
    in p_start_date Date,
    in p_end_date Date)
begin
    select * from jobs where start_date >= p_start_date and start_date <= p_end_date and predicted_duration > 0.0 order by start_date;
end$$
delimiter ;



drop procedure `ListJobsByDates`;
delimiter $$
create procedure ListJobsByDates(
    in p_start_date Date,
    in p_end_date Date)
begin
    select * from jobs.id, jobs.start_date,  where start_date >= p_start_date and start_date <= p_end_date and predicted_duration > 0.0 order by start_date;
end$$
delimiter ;

start transaction;
call UpdateAllJobsPrediction(7.5);

commit;



delimiter $$
create trigger jobs_table_update after update on jobs
for each row
begin
    declare startTime varchar(50) default '';
    declare endTime varchar(50) default '';
    
    select concat(jobs.start_date, ' ', jobs.start_time) into startTime from jobs where jobs.id = p_job_id;
    select concat(jobs.end_date, ' ', jobs.end_time) into endTime from jobs where jobs.id = p_job_id;
    update jobs set jobs.predicted_duration = round(time_to_sec(timediff(endTime, startTime))/3600, 2);    
    
    set jobs.predicted_amount = 7.5 * jobs.jobs.predicted_duration;
    
end$$
delimiter ;



DROP PROCEDURE `UpdateJobEndTime`;
delimiter $$
create procedure UpdateJobEndTime(
    in p_job_id int(11),
    in p_job_end_time TIME)
begin
    declare diff_time TIME default Time('00:00');
    select timediff(end_time, start_time) into diff_time from jobs where id = p_job_id;
    
    update jobs
    set end_time 
    SELECT jobs.id, jobs.start_date, jobs.start_time, jobs.end_date, jobs.end_time, company.name, addresses.address, addresses.postcode FROM company, addresses, jobs WHERE jobs.id=p_job_id and jobs.location = addresses.id and addresses.company_id = company.id;    
end$$

create procedure ListAllJobs()
begin        
    SELECT jobs.id, jobs.start_date, jobs.start_time, jobs.end_date, jobs.end_time, company.name, addresses.address, addresses.postcode FROM company, addresses, jobs WHERE jobs.location = addresses.id and addresses.company_id = company.id order by jobs.start_date;
end$$

delimiter ;


DROP PROCEDURE `UpdateJobEndDate`;
delimiter $$
create procedure UpdateJobEndDate(
    in p_job_id int(11),
    in p_job_end_date DATE)
begin
    declare diff_time TIME default Time('00:00');
    select timediff(end_time, start_time) into diff_time from jobs where id = p_job_id;
    
    update jobs
    set end_time 
    SELECT jobs.id, jobs.start_date, jobs.start_time, jobs.end_date, jobs.end_time, company.name, addresses.address, addresses.postcode FROM company, addresses, jobs WHERE jobs.id=p_job_id and jobs.location = addresses.id and addresses.company_id = company.id;    
end$$




drop table expense_proof;
CREATE TABLE expense_proof(
    id int(11) unsigned NOT NULL auto_increment,
    trip_id int(11) unsigned, 
    proof_type int(11) unsigned,
    expense_amount DECIMAL(7, 2),
    reference varchar(250), 
    PRIMARY KEY (id),

    CONSTRAINT fk_trip_id FOREIGN KEY (trip_id) REFERENCES trip(id) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE,

    CONSTRAINT fk_proof_type FOREIGN KEY (proof_type) REFERENCES expense_proof_type(id) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table expenses;
CREATE TABLE expenses(
    id int(11) unsigned NOT NULL auto_increment,
    expense_proof_id int(11) unsigned NOT NULL,
    submit_date DATE,
    paid_date DATE,
    paid_amount DECIMAL(7, 2),
    reference varchar(250),
    PRIMARY KEY (id),
    
    CONSTRAINT fk_expense_proof_id FOREIGN KEY (expense_proof_id) REFERENCES expense_proof(id) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



drop table payment;
CREATE TABLE payment(
    id int(11) unsigned NOT NULL auto_increment,
	job_id int(11) unsigned NOT NULL,
    predicted_duration DECIMAL(7, 2),
	predicted_amount DECIMAL(7, 2),
    actual_duration DECIMAL(7, 2),
    paid_amount DECIMAL(7, 2),
    paid_date DATE,
    reference varchar(250),
	PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert  into payment (job_id, predicted_duration, predicted_amount) values 
(985323, (select timediff(SECOND, (select concat(start_date,' ', start_time) from jobs where id='985323'), (select concat(end_date,' ',end_time) from jobs where id='985323') ))),
(970539, ),
(985276, ),
(966946, ),
(987941, ),
(974102, ),
(974103, ),
(957597, ),
(961097, ),
(966957, ),
(955181, ),
(962393, ),
(974115, ),
(980672, ),
(974118, ),
(957621, ),
(962384, ),
(972007, )
;


