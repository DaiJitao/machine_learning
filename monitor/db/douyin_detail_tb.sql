-- source user_douyin_tb.sql
-- 具体某一账号统计
-- DROP TABLE IF EXISTS douyin_detail_tb;

CREATE TABLE douyin_detail_tb
(
  user_id        VARCHAR(100)                       NOT NULL,
  total BIGINT(20) unsigned DEFAULT 0,
  total_cycle   INT(10) UNSIGNED DEFAULT 0 COMMENT '总量的周期量',
  article_total BIGINT(20) unsigned DEFAULT 0,
  article_cycle INT(10)          DEFAULT 0   COMMENT '文章信息量',
  account_total BIGINT(20) UNSIGNED DEFAULT 0,
  account_cycle INT(10)          DEFAULT 0,
  time_insert   DATETIME DEFAULT CURRENT_TIMESTAMP NULL,
  time_update   DATETIME DEFAULT CURRENT_TIMESTAMP NULL
)
  COMMENT '抖音用户采集信息表'
  DEFAULT CHARSET = utf8
  ENGINE = InnoDB;