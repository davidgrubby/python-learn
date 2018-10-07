
from scrapy.selector import Selector

def test():
    response = '''
    <div class="day7">
				<ul class="week">
											<li><b>10月05日</b><span>星期五</span><img src="//static.tianqistatic.com/static/wap2018/ico1/b2.png"></li>
											<li><b>10月06日</b><span>星期六</span><img src="//static.tianqistatic.com/static/wap2018/ico1/b1.png"></li>
											<li><b>10月07日</b><span>星期日</span><img src="//static.tianqistatic.com/static/wap2018/ico1/b1.png"></li>
											<li><b>10月08日</b><span>星期一</span><img src="//static.tianqistatic.com/static/wap2018/ico1/b0.png"></li>
											<li><b>10月09日</b><span>星期二</span><img src="//static.tianqistatic.com/static/wap2018/ico1/b1.png"></li>
											<li><b>10月10日</b><span>星期三</span><img src="//static.tianqistatic.com/static/wap2018/ico1/b8.png"></li>
											<li><b>10月11日</b><span>星期四</span><img src="//static.tianqistatic.com/static/wap2018/ico1/b7.png"></li>
									</ul>
				<ul class="txt txt2">
											<li>阴转小雨</li>
											<li>阴转多云</li>
											<li>多云</li>
											<li>晴</li>
											<li>多云</li>
											<li>中雨到大雨</li>
											<li>小雨</li>
									</ul>
				<div class="zxt_shuju" style="display: none;">
				<ul>
											<li><span>22</span><b>19</b></li>
											<li><span>25</span><b>19</b></li>
											<li><span>25</span><b>20</b></li>
											<li><span>25</span><b>19</b></li>
											<li><span>24</span><b>19</b></li>
											<li><span>23</span><b>18</b></li>
											<li><span>23</span><b>18</b></li>
									</ul>
				</div>
				<canvas id="canvas" width="600" height="140"></canvas>
				<script type="text/javascript" src="//static.tianqistatic.com/static/js/canvas.js"></script>
				<ul class="txt">
											<li>北风</li>
											<li>西北风</li>
											<li>东北风</li>
											<li>东风</li>
											<li>东风</li>
											<li>东北风</li>
											<li>东北风</li>
									</ul>			
			</div>
    
    '''

    items = Selector(text=response).xpath('//div[@class="day7"]').extract()
    print (items )

    weeks = Selector(text=response).xpath('//ul[@class="week"]').extract()
    print(weeks)

    for week in weeks:
        print(week)


    # a = Selector(text=response).xpath('/html/body/class[last()]').extract()
    # a = Selector(text=response).xpath('/html/body/class[last()]/name').extract()
    # a = Selector(text=response).xpath('/class[last()]/name/text()').extract()
    # print( response )



if __name__ == '__main__':
    test()
