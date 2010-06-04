CREATE TABLE IF NOT EXISTS novel_items ( /* {{{ */
	id mediumint(9) NOT NULL auto_increment,
	name varchar(128) NOT NULL,
	intro text,
	page_url varchar(256) UNIQUE NOT NULL,
	img_url varchar(1024),

	PRIMARY KEY (id)
) ENGINE MyISAM; /* }}} */
