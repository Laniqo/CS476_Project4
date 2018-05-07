

INSERT INTO user(user_id, username, email, pw_hash) VALUES ('d53f5c86-002c-4184-99fc-2fa7c8a8803b', 'mark', 'mark@sample.com', 'pbkdf2:sha256:50000$ohqiElyi$252bad2e576361a8e6b030ef11118ef44cecaa73a89d6261e4c264acd77fb20b' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('191509f2-6af2-463d-8f24-259ccc8dc7a8', 'john', 'john@sample.com', 'pbkdf2:sha256:50000$T4VE9mTh$a98e6153057717e6d1580614b0e4e10349d2c4fded64fd234ad7f7039cf2367e' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('b20d93ae-e08d-45e7-b7d7-e6b718588a2a', 'tom', 'tom@sample.com', 'pbkdf2:sha256:50000$MtSnA8fD$00a15a4360be3ae035f16612290bfc96badc567f4d3ebb678f3b3a1827ffcd35' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('af38af9f-bca1-4801-953e-9a45aa8aecc3', 'jack', 'jack@sample.com', 'pbkdf2:sha256:50000$0ujvulkd$c3e82bc1beaae9f8bab74b468c012f7642e36da764d2f64d332325819df3ecea' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('?', 'craig', 'craig@sample.com', 'pbkdf2:sha256:50000$tQ3v5Fmy$77377f7f0740cc1b836332e7862d6cf0d97b54f9fc84ed01c76c483d03934a50' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('?', 'josh', 'josh@sample.com', 'pbkdf2:sha256:50000$0fKZMC5m$b4c3e62978d7f75cc6c112e1937e17ce9fa28cbfed1f484e7063732dd0ad8127' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('?', 'bilbo', 'bilbo@sample.com', 'pbkdf2:sha256:50000$FCV2OQCj$e4c87d8752b5b9ce1b5d97aa70dbd4f9cd16d0caaefcf7d3886a928229388d62' );


INSERT INTO message(message_id, author_id, text, pub_date) VALUES
(1,'d53f5c86-002c-4184-99fc-2fa7c8a8803b', 'hello minitwit!!', 1518739148),
(2,'d53f5c86-002c-4184-99fc-2fa7c8a8803b', '2nd post whats up!', 1518739188),
(3,'d53f5c86-002c-4184-99fc-2fa7c8a8803b', 'hello!', 1518739976),
(4,'191509f2-6af2-463d-8f24-259ccc8dc7a8', 'Bored!', 1518741362),
(5,'191509f2-6af2-463d-8f24-259ccc8dc7a8', 'hello world!', 1518741366),
(6,'b20d93ae-e08d-45e7-b7d7-e6b718588a2a', 'semester over yet', 1518741380),
(7,'b20d93ae-e08d-45e7-b7d7-e6b718588a2a', 'bang bang!', 1518741382);

INSERT INTO follower(who_id, whom_id) VALUES
('d53f5c86-002c-4184-99fc-2fa7c8a8803b', '191509f2-6af2-463d-8f24-259ccc8dc7a8'),
('d53f5c86-002c-4184-99fc-2fa7c8a8803b', 'b20d93ae-e08d-45e7-b7d7-e6b718588a2a'),
('af38af9f-bca1-4801-953e-9a45aa8aecc3', 'b20d93ae-e08d-45e7-b7d7-e6b718588a2a');
