INSERT INTO user(user_id, username, email, pw_hash) VALUES ('f0955664-6b5a-4717-9ef5-756c7f7c2b7a', 'user7', 'user7@sample.com', 'pbkdf2:sha256:50000$ohqiElyi$252bad2e576361a8e6b030ef11118ef44cecaa73a89d6261e4c264acd77fb20b' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('2561c360-a31c-4dcc-a78d-de71f31ea579', 'rufio', 'rufio@sample.com', 'pbkdf2:sha256:50000$T4VE9mTh$a98e6153057717e6d1580614b0e4e10349d2c4fded64fd234ad7f7039cf2367e' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('b66c74bf-8b2b-4ab3-bd6d-ca217d647e39', 'banksy', 'banksy@sample.com', 'pbkdf2:sha256:50000$MtSnA8fD$00a15a4360be3ae035f16612290bfc96badc567f4d3ebb678f3b3a1827ffcd35' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('71ea059c-5a56-498f-9a35-1e71cb8a5ef9', 'user10', 'use10@sample.com', 'pbkdf2:sha256:50000$0ujvulkd$c3e82bc1beaae9f8bab74b468c012f7642e36da764d2f64d332325819df3ecea' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('11db6beb-534d-42dc-a8b0-7d3dda84796e', 'user11', 'user11@sample.com', 'pbkdf2:sha256:50000$tQ3v5Fmy$77377f7f0740cc1b836332e7862d6cf0d97b54f9fc84ed01c76c483d03934a50' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('23a2169c-c768-469a-8254-deaa9d4ce761', 'user12', 'user12@sample.com', 'pbkdf2:sha256:50000$0fKZMC5m$b4c3e62978d7f75cc6c112e1937e17ce9fa28cbfed1f484e7063732dd0ad8127' );
INSERT INTO user(user_id, username, email, pw_hash) VALUES ('?', 'user13', 'user13@sample.com', 'pbkdf2:sha256:50000$FCV2OQCj$e4c87d8752b5b9ce1b5d97aa70dbd4f9cd16d0caaefcf7d3886a928229388d62' );


INSERT INTO message(message_id, author_id, text, pub_date) VALUES
(1,'2561c360-a31c-4dcc-a78d-de71f31ea579', 'rufio here', 1518739199),
(2,'b66c74bf-8b2b-4ab3-bd6d-ca217d647e39', 'banksy here 2! what  up!', 1518739192),
(3,'11db6beb-534d-42dc-a8b0-7d3dda84796e', 'this sh*t sucks!', 1518739980);


INSERT INTO follower(who_id, whom_id) VALUES
('f0955664-6b5a-4717-9ef5-756c7f7c2b7a', '2561c360-a31c-4dcc-a78d-de71f31ea579'),
('2561c360-a31c-4dcc-a78d-de71f31ea579', '11db6beb-534d-42dc-a8b0-7d3dda84796e'),
('71ea059c-5a56-498f-9a35-1e71cb8a5ef9', 'b20d93ae-e08d-45e7-b7d7-e6b718588a2a');
