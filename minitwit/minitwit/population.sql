

INSERT INTO user(user_id, username, email, pw_hash) VALUES ('d53f5c86-002c-4184-99fc-2fa7c8a8803b', 'mark', 'mark@sample.com', 'pbkdf2:sha256:50000$ohqiElyi$252bad2e576361a8e6b030ef11118ef44cecaa73a89d6261e4c264acd77fb20b' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('b20d93ae-e08d-45e7-b7d7-e6b718588a2a', 'tom', 'tom@sample.com', 'pbkdf2:sha256:50000$MtSnA8fD$00a15a4360be3ae035f16612290bfc96badc567f4d3ebb678f3b3a1827ffcd35' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('af38af9f-bca1-4801-953e-9a45aa8aecc3', 'jack', 'jack@sample.com', 'pbkdf2:sha256:50000$0ujvulkd$c3e82bc1beaae9f8bab74b468c012f7642e36da764d2f64d332325819df3ecea' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('191509f2-6af2-463d-8f24-259ccc8dc7a8', 'john', 'john@sample.com', 'pbkdf2:sha256:50000$T4VE9mTh$a98e6153057717e6d1580614b0e4e10349d2c4fded64fd234ad7f7039cf2367e' );


INSERT INTO message(message_id, author_id, text, pub_date) VALUES
('6db04dd8-7515-4d3d-9f6a-a9e1c788dd4c','191509f2-6af2-463d-8f24-259ccc8dc7a8', 'Bored!', 1518741362);
INSERT INTO message(message_id, author_id, text, pub_date) VALUES
('b27c2da9-2a49-422c-b49e-62b6092df393','191509f2-6af2-463d-8f24-259ccc8dc7a8', 'hello world!', 1518741366);
INSERT INTO message(message_id, author_id, text, pub_date) VALUES
('0d371d2c-20dd-47b5-93db-e83247375ff8','d53f5c86-002c-4184-99fc-2fa7c8a8803b', 'hello minitwit!!', 1518739148);
INSERT INTO message(message_id, author_id, text, pub_date) VALUES
('def70c4b-8678-4d5e-9c34-c022718ef6f9','d53f5c86-002c-4184-99fc-2fa7c8a8803b', '2nd post whats up!', 1518739188);
INSERT INTO message(message_id, author_id, text, pub_date) VALUES
('0ac9b36b-de88-4f0c-9c92-78b2b7d73aed','d53f5c86-002c-4184-99fc-2fa7c8a8803b', 'hello!', 1518739976);
INSERT INTO message(message_id, author_id, text, pub_date) VALUES
('d606161c-34a3-4722-b623-030a89e4b17a','b20d93ae-e08d-45e7-b7d7-e6b718588a2a', 'semester over yet', 1518741380);
INSERT INTO message(message_id, author_id, text, pub_date) VALUES
('aca33e17-3bbe-4a30-9b47-db4772e3dcad','b20d93ae-e08d-45e7-b7d7-e6b718588a2a', 'bang bang!', 1518741382);

INSERT INTO follower(who_id, whom_id) VALUES
('d53f5c86-002c-4184-99fc-2fa7c8a8803b', '191509f2-6af2-463d-8f24-259ccc8dc7a8'),
('d53f5c86-002c-4184-99fc-2fa7c8a8803b', 'b20d93ae-e08d-45e7-b7d7-e6b718588a2a'),
('af38af9f-bca1-4801-953e-9a45aa8aecc3', 'b20d93ae-e08d-45e7-b7d7-e6b718588a2a');
