# 更新时间
ALTER TABLE douyin_tb ADD time_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '更新时间';
ALTER TABLE toutiao_tb ADD time_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '更新时间';
# 插入时间
ALTER TABLE douyin_tb ADD time_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL COMMENT '插入时间';
ALTER TABLE toutiao_tb ADD time_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL COMMENT '插入时间';

# 获取最新一条数据：
SELECT * FROM toutiao_tb ORDER BY time_update DESC LIMIT 1;

#---------------------------------------------
            time_update: 2020-03-13 13:22:18
             total_data: 110
             cycle_type: 1
              cycle_num: 110
          account_total: 0
      account_cycle_num: 0
          article_total: 0
      article_cycle_num: 0
     article_text_total: 0
 article_text_cycle_num: 0
    article_micro_total: 0
article_micro_cycle_num: 0
    article_video_total: 0
article_video_cycle_num: 0
           update_total: 0
       update_cycle_num: 0
     updata_micro_total: 0
     update_micro_cycle: 0
      update_text_total: 0
      update_text_cycle: 0
     update_video_total: 0
     update_video_cycle: 0
          comment_total: 0
          comment_cycle: 0
            video_total: 0
            video_cycle: 0
            time_insert: 2020-03-13 13:22:18
#-----------------------------------------------------------------------------










