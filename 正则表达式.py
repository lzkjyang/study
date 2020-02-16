'''import re
q = lambda x,y:False if len(x.split(y)[0])==len(x) else True
z= ''''''1、国家级、世界级、最高级、顶级
国家级、世界级、最高级、顶级、顶尖、高级、高档、世界领先、遥遥领先、一马当先；
国家示范、全国领先、行业顶尖、行业领先、领衔、问鼎、开创之举、填补国内空白。
第一、唯一、首个
第一、唯一、首个、先进、前卫、进步、率先；推荐首选、优选、优质、首家、独家、全力、致力、全新、第一人、首席；
独一无二、独家、绝无仅有、前无古人、100% 百分百、史上、非常一流、优异。
金牌、名牌
金牌、名牌——品牌
王牌、销量冠军、第一(NO.1\Top1)、领袖品牌、领导品牌、顶级、顶尖、泰斗、金标、金牌、驰名尖端、高端。
最，全、精、永久
最、终极、极致、 万能、决对、彻底、完全、极佳、全解决、全方位、全面；
全面改善、精确、准确、精准、优秀、优质、杰出、出色、卓越、优越；完美、永久、悠久、长期、很久、永不反弹、永久、立竿见影、承诺；
治愈率、有效率、复发、痊愈、治愈、根除、根治、无痕、无创、不留疤、不留痕；无痛、无副作用；
保证、可靠；长久、长效、特效、效果明显、效果显著、死角；当天见效、立马见效、马上起效。''''''.split('、')
print('Z is {0}'.format(z))
for k,v in enumerate(z):
     if re.match(re.compile( '(.*)。|(.*)、|(.*)\(|(.*)\)|(.*)\\\\'),v):
         a = v.split('。') if q(v, '。') else ( v.split('、') if q(v, '、') else (v.split('(') if q(v, '(') else (v.split(')') if q(v, ')') else (v.split('\\')))))
         print('add{0}'.format(a))
         a = [ value for value in a if value!= '']
         z.extend(a)
         print('remove {0}'.format(v))
         z.remove(v)
print (z)
'''

import re
#from collections import deque

class ParserTxt(object):
    ''' 清洗文本 分类 去重'''
    # __reTxt='(.*)。|(.*)、|(.*)\(|(.*)\)|(.*)\\\\|(.*)；|(.*)、|(.*) |\n|\r'
    # __sep=r'。、()\\； '

    def __init__(self,*args,**kwargs):
        #初始 正则和内部分隔符
        self._retxt = '(.*)。|(.*)、|(.*)\(|(.*)\)|(.*)\\\\|(.*)；|(.*)、|(.*) |(.*)\n|(.*)\r|(.*)，'
        self._sep = '。、，,()\\； \n\r'
        self._ReSplitFun=lambda txt,re:False if len(txt.split(re)[0])==len(txt) else True  #检测 文本是否包含re分隔符
        #self.ShowReSep()
        super(ParserTxt).__init__(*args,**kwargs)

    def ReOfList(self,txt=None,OutSep=None,encoding='utf8'):
        ''' 将文本分隔成List'''
        if type(txt)!=type('') :   #判断TXT为文本
            raise "txt is text,please retry!"
            exit(-1)
        #txt 分解最外层
        self.txt = txt.split(OutSep)
        #print('ReOfList: ',self.txt)
        #内层分解到List  优化 灵活性更强
        return self.inRe(self.txt)

    def ShowReSep(self):
        print('ReTxt:{0} \n Sep:{1}'.format(self._retxt,self._sep))

    def inRe(self,List=None):
        ''' 内部分解'''
        if type(List) != type(list('')):
            raise "List is list object,please retry!"
            exit(-1)
        self.lst = List
        #print (self.lst)
        #处理List，去掉分隔符
        for value in self.lst:
            if re.match(re.compile(self._retxt),value):
                for sep in self._sep:
                    if self._ReSplitFun(value,sep): #找到第一个分隔符，处理后，跳出第一个
                        self.lst.extend(value.split(sep))
                        break
            elif value != '':
                yield value
'''
        for value in self.lst:
            if re.match(re.compile(self._retxt),value):
                #print(eval("self._ReSplitFun('"+value+"',"+repr('\n') + ")"))
                for _sep in self._sep :
                    if self._ReSplitFun(value,_sep):
                        self.lst.extend(value.split(_sep))
                    #print(_sep)

                #[self.lst.extend(value.split(repr(_sep)) for _sep in self._sep if eval("self._ReSplitFun("+repr(value)+","+repr(_sep) + ")")]
                #self.lst.remove(value)
            else :
                print(value)

                #yield value
                #self.lst.remove(value)
'''


z= '''1、国家级、世界级、最高级、顶级
国家级、世界级、最高级、顶级、顶尖、高级、高档、世界领先、遥遥领先、一马当先；
国家示范、全国领先、行业顶尖、行业领先、领衔、问鼎、开创之举、填补国内空白。
第一、唯一、首个
第一、唯一、首个、先进、前卫、进步、率先；推荐首选、优选、优质、首家、独家、全力、致力、全新、第一人、首席；
独一无二、独家、绝无仅有、前无古人、100% 百分百、史上、非常一流、优异。
金牌、名牌
金牌、名牌——品牌
王牌、销量冠军、第一(NO.1\Top1)、领袖品牌、领导品牌、顶级、顶尖、泰斗、金标、金牌、驰名尖端、高端。
最，全、精、永久
最、终极、极致、 万能、决对、彻底、完全、极佳、全解决、全方位、全面；
全面改善、精确、准确、精准、优秀、优质、杰出、出色、卓越、优越；完美、永久、悠久、长期、很久、永不反弹、永久、立竿见影、承诺；
治愈率、有效率、复发、痊愈、治愈、根除、根治、无痕、无创、不留疤、不留痕；无痛、无副作用；
保证、可靠；长久、长效、特效、效果明显、效果显著、死角；当天见效、立马见效、马上起效。地球最强'''
if __name__ == '__main__':
    MyObj = ParserTxt()
    for k,x in enumerate(MyObj.ReOfList(txt=z)):
        print (k,x)
