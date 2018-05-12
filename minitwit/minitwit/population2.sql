INSERT INTO user(user_id, username, email, pw_hash) VALUES ('fa99f9af-541c-4a4f-b1e0-f844eff78fec', 'craig', 'craig@sample.com', 'pbkdf2:sha256:50000$tQ3v5Fmy$77377f7f0740cc1b836332e7862d6cf0d97b54f9fc84ed01c76c483d03934a50' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('1502ebfe-433f-4756-ba42-06ca1e896c39', 'user1', 'user1@sample.com', 'pbkdf2:sha256:50000$ohqiElyi$252bad2e576361a8e6b030ef11118ef44cecaa73a89d6261e4c264acd77fb20b' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('ce701bfb-ca81-4227-bb97-fdeed2ac4376', 'user2', 'user2@sample.com', 'pbkdf2:sha256:50000$T4VE9mTh$a98e6153057717e6d1580614b0e4e10349d2c4fded64fd234ad7f7039cf2367e' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('47e8d685-ccee-4c7d-8029-9a11d5cc9e55', 'user3', 'user3@sample.com', 'pbkdf2:sha256:50000$MtSnA8fD$00a15a4360be3ae035f16612290bfc96badc567f4d3ebb678f3b3a1827ffcd35' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('d2acec16-a4bb-4215-b9ea-8dc4119af70e', 'user4', 'user4@sample.com', 'pbkdf2:sha256:50000$0ujvulkd$c3e82bc1beaae9f8bab74b468c012f7642e36da764d2f64d332325819df3ecea' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('e6607a8e-70a3-4a89-bcb9-b84a4e915499', 'user5', 'user5@sample.com', 'pbkdf2:sha256:50000$tQ3v5Fmy$77377f7f0740cc1b836332e7862d6cf0d97b54f9fc84ed01c76c483d03934a50' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('90417063-b425-4f10-b161-28234534c8b4', 'user6', 'user6@sample.com', 'pbkdf2:sha256:50000$0fKZMC5m$b4c3e62978d7f75cc6c112e1937e17ce9fa28cbfed1f484e7063732dd0ad8127' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('b4dc988a-4059-4c72-8457-e9537de7f4c5', 'user13', 'user13@sample.com', 'pbkdf2:sha256:50000$FCV2OQCj$e4c87d8752b5b9ce1b5d97aa70dbd4f9cd16d0caaefcf7d3886a928229388d62' );

INSERT INTO message(message_id, author_id, text, pub_date) VALUES
('8ae7a49c-7f8c-4226-b0e6-ac63cc650c99','1502ebfe-433f-4756-ba42-06ca1e896c39', 'user1 here', 1518739155);
INSERT INTO message(message_id, author_id, text, pub_date) VALUES
('f2afcc50-c110-4a78-94c9-b8853494204b','ce701bfb-ca81-4227-bb97-fdeed2ac4376', 'user 2! post  up!', 1518739190);
INSERT INTO message(message_id, author_id, text, pub_date) VALUES
('62477f5b-87a1-4978-b171-4729c62403ca','47e8d685-ccee-4c7d-8029-9a11d5cc9e55', 'whack!', 1518739978);
INSERT INTO message(message_id, author_id, text, pub_date) VALUES
('8e5b512a-8359-4226-ac4b-2e7eae48628c','e6607a8e-70a3-4a89-bcb9-b84a4e915499', 'used up so much time on this!!', 1518741365);
INSERT INTO message(message_id, author_id, text, pub_date) VALUES
('c6168841-7893-4cc4-942d-74b7b21163c4','90417063-b425-4f10-b161-28234534c8b4', 'I could be doing better things and getting paid!', 1518741369);



INSERT INTO follower(who_id, whom_id) VALUES
('1502ebfe-433f-4756-ba42-06ca1e896c39', 'ce701bfb-ca81-4227-bb97-fdeed2ac4376'),
('47e8d685-ccee-4c7d-8029-9a11d5cc9e55', '90417063-b425-4f10-b161-28234534c8b4'),
('90417063-b425-4f10-b161-28234534c8b4', 'b20d93ae-e08d-45e7-b7d7-e6b718588a2a');
