-- source user_douyin_tb.sql

CREATE TABLE user_toutiao_tb
(
  user_id               VARCHAR(50)                        NOT NULL,
  name                  VARCHAR(100)                       NULL,
  first_classification  VARCHAR(10) DEFAULT '1'            NULL,
  county                VARCHAR(6) DEFAULT '0'             NULL,
  city                  VARCHAR(10) DEFAULT '0'            NULL,
  second_classification VARCHAR(6) DEFAULT '2'             NULL,
  province              VARCHAR(6) DEFAULT '48'            NULL,
  url                   VARCHAR(300)                       NULL,
  insert_time           DATETIME DEFAULT CURRENT_TIMESTAMP NULL,
  update_time           DATETIME DEFAULT CURRENT_TIMESTAMP NULL
)
  COMMENT '头条用户信息表'
  DEFAULT CHARSET=utf8
  ENGINE = InnoDB;