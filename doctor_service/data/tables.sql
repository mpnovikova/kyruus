CREATE TABLE IF NOT EXISTS doctors(
  docid INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  updated_at INTEGER ,
  deleted_at INTEGER);
insert into doctors(first_name, last_name, created_at) values ('Richard', 'Smith', strftime('%s','now'));
insert into doctors(first_name, last_name, created_at) values ('Mary', 'Brown', strftime('%s','now'));
insert into doctors(first_name, last_name, created_at) values ('Brian', 'Sullivan', strftime('%s','now'));
insert into doctors(first_name, last_name, created_at) values ('Megan', 'Welsh', strftime('%s','now'));


CREATE TABLE IF NOT EXISTS locations(locid INTEGER PRIMARY KEY AUTOINCREMENT, address TEXT NOT NULL);
INSERT INTO locations(address) VALUES ('123 Maple st, Salem MA 01970');
INSERT INTO locations(address) VALUES ('45 Oak ln, Peabody MA 01960');
INSERT INTO locations(address) VALUES ('71 Willow rd, Melrose MA 02176');

CREATE TABLE IF NOT EXISTS slots(slotid INTEGER PRIMARY KEY AUTOINCREMENT, slot_start TEXT NOT NULL);
INSERT INTO slots(slot_start) VALUES('0000');
INSERT INTO slots(slot_start) VALUES('0100');
INSERT INTO slots(slot_start) VALUES('0200');
INSERT INTO slots(slot_start) VALUES('0300');
INSERT INTO slots(slot_start) VALUES('0400');
INSERT INTO slots(slot_start) VALUES('0500');
INSERT INTO slots(slot_start) VALUES('0600');
INSERT INTO slots(slot_start) VALUES('0700');
INSERT INTO slots(slot_start) VALUES('0800');
INSERT INTO slots(slot_start) VALUES('0900');
INSERT INTO slots(slot_start) VALUES('1000');
INSERT INTO slots(slot_start) VALUES('1100');
INSERT INTO slots(slot_start) VALUES('1200');
INSERT INTO slots(slot_start) VALUES('1300');
INSERT INTO slots(slot_start) VALUES('1400');
INSERT INTO slots(slot_start) VALUES('1500');
INSERT INTO slots(slot_start) VALUES('1600');
INSERT INTO slots(slot_start) VALUES('1700');
INSERT INTO slots(slot_start) VALUES('1800');
INSERT INTO slots(slot_start) VALUES('1900');
INSERT INTO slots(slot_start) VALUES('2000');
INSERT INTO slots(slot_start) VALUES('2100');
INSERT INTO slots(slot_start) VALUES('2200');
INSERT INTO slots(slot_start) VALUES('2300');

CREATE TABLE IF NOT EXISTS schedule(
  app_date TEXT NOT NULL,
  docid INTEGER,
  locid INTEGER,
  slotid INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER,
  deleted_at INTEGER,
  FOREIGN KEY(docid) REFERENCES doctors(docid),
  FOREIGN KEY(locid) REFERENCES locations(locid),
  FOREIGN KEY(slotid) REFERENCES slots(slotid)
);

INSERT INTO schedule(app_date, docid, locid, slotid, created_at) VALUES(strftime('%s','now', '+2 month'), 1, 1, 9, strftime('%s','now'));

SELECT schedule.app_date, slots.slot_start, doctors.first_name, doctors.last_name, locations.address FROM schedule
INNER JOIN doctors ON doctors.docid = schedule.docid
INNER JOIN locations ON locations.locid = schedule.locid
INNER JOIN slots ON slots.slotid = schedule.slotid;

