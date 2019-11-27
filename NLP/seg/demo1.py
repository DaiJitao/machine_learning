import pkuseg
import jieba_fast as jieba
model = pkuseg.pkuseg()
s = "我爱北京天安门，代继涛你好"
text = model.cut(s)
print(text)

print(" ".join(jieba.cut(s)))

model = pkuseg.pkuseg(model_name='medicine')
print(model.cut(s))