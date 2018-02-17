

INSERT INTO user(user_id, username, email, pw_hash) VALUES ('1', 'mark', 'mark@sample.com', 'pbkdf2:sha256:50000$ohqiElyi$252bad2e576361a8e6b030ef11118ef44cecaa73a89d6261e4c264acd77fb20b' );

INSERT INTO user(user_id, username, email, pw_hash) VALUES ('2', 'john', 'john@sample.com', 'pbkdf2:sha256:50000$T4VE9mTh$a98e6153057717e6d1580614b0e4e10349d2c4fded64fd234ad7f7039cf2367e' );

INSERT INTO user(user_id, username, email, pw_hash) VALUES ('3', 'tom', 'tom@sample.com', 'pbkdf2:sha256:50000$MtSnA8fD$00a15a4360be3ae035f16612290bfc96badc567f4d3ebb678f3b3a1827ffcd35' );



INSERT INTO message(message_id, author_id, text, pub_date) VALUES
(1, 1, 'hello minitwit!', 1518739148),
(2, 2, 'new user', 1518739188),
(3, 3, 'whats up', 1518739976),
(4, 3, 'bangarang!', 1518741362),
(5, 2, 'bang bang', 1518741366),
(6, 1, 'new app, who dis?', 1518741380);


INSERT INTO follower(who_id, whom_id) VALUES
(2, 1),
(3, 2),
(3, 1);
