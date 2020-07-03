INSERT INTO toutiao_tb
            (
              total_data, cycle_type, cycle_num,
              account_total, account_cycle_num,
              article_total, article_cycle_num,
              article_text_total, article_text_cycle_num,
              article_micro_total,article_micro_cycle_num,
              article_video_total, article_video_cycle_num,
              update_total, update_cycle_num,
              updata_micro_total,update_micro_cycle,
              update_text_total,update_text_cycle,
              update_video_total, update_video_cycle,
              comment_total, comment_cycle,
              video_total,video_cycle
            )
VALUES (
              total_data, cycle_type, cycle_num,
              account_total, account_cycle_num,
              article_total, article_cycle_num,
              article_text_total, article_text_cycle_num,
              article_micro_total,article_micro_cycle_num,
              article_video_total, article_video_cycle_num,
              update_total, update_cycle_num,
              updata_micro_total,update_micro_cycle,
              update_text_total,update_text_cycle,
              update_video_total, update_video_cycle,
              comment_total, comment_cycle,
              video_total,video_cycle
);


def gen_sql(dict_):
    sql = 'INSERT INTO toutiao_tb (' \
          'total_data, cycle_type, cycle_num,' \
          'account_total, account_cycle_num,' \
          'article_total, article_cycle_num,' \
          'article_text_total, article_text_cycle_num,' \
          'article_micro_total,article_micro_cycle_num,' \
          'article_video_total, article_video_cycle_num,' \
          'update_total, update_cycle_num,' \
          'updata_micro_total,update_micro_cycle,' \
          'update_text_total,update_text_cycle,' \
          'update_video_total, update_video_cycle,' \
          'comment_total, comment_cycle,' \
          'video_total,video_cycle' \
          ') VALUES (' \
          'total_data, cycle_type, cycle_num,' \
          'account_total, account_cycle_num,' \
          'article_total, article_cycle_num,' \
          'article_text_total, article_text_cycle_num,' \
          'article_micro_total,article_micro_cycle_num,' \
          'article_video_total, article_video_cycle_num,' \
          'update_total, update_cycle_num,' \
          'updata_micro_total,update_micro_cycle,' \
          'update_text_total,update_text_cycle,' \
          'update_video_total, update_video_cycle,' \
          'comment_total, comment_cycle,' \
          'video_total,video_cycle' \
          ');'

INSERT INTO douyin_tb (cycle_type, article_total) VALUES ('30',90000);