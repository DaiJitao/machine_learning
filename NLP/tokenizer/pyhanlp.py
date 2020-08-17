from pyhanlp import HanLP

texts = [u"LAC是个优秀的分词工具", u"百度是一家高科技公司"]
print(HanLP.segment(texts))