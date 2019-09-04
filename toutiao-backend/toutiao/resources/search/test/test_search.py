import json
import unittest
# 1.自定义单元测试类 unittest.TestCase
# 2.实现默认的方法
# 3.实现自定义的测试方法

from toutiao import create_app
# 创建flask应用
test_app = create_app('test')


# 自定义测试类
class SuggestionTestCase(unittest.TestCase):
    """搜索建议测试用例类"""
    def setUp(self):
        """每个测试方法启动前会调用"""
        print('测试初始化')
        # 创建测试客户端
        self.client = test_app.test_client()

    def tearDown(self):
        """每个测试方法执行后会调用"""
        print("进行测试的资源回收")

    def test_request_normal(self):
        print("测试正常请求的情况")
        """
        测试中发请求:  1> 使用普通的网络请求的框架 urllib/request 2> 使用web应用框架提供的测试工具 优点:不是发送真实请求, 只是模拟请求, 提高测试的效率
        """
        # 发起测试请求
        resp = self.client.get('/v1_0/suggestion?q=python')
        # 对状态码进行断言
        self.assertEqual(resp.status_code, 200, '正常请求的状态码不是200')
        # 对返回的数据进行断言
        resp_json_str = resp.data
        resp_dict = json.loads(resp_json_str)
        self.assertIn('message', resp_dict, '正常请求返回的数据不包含message字段')
        self.assertIn('data', resp_dict, '正常请求返回的数据不包含data字段')
        data = resp_dict['data']
        self.assertIn('options', data, '返回数据的data字段中不包含option字段')


    def test_param_q_missing(self):
        print("测试参数q缺失的情况")
        # 发起测试请求
        resp = self.client.get('/v1_0/suggestion')
        # 对状态码进行断言
        self.assertEqual(resp.status_code, 400, '参数q缺失状态码不是400')

    def test_param_q_length_error(self):
        print("测试参数q长度错误的情况")
        # 发起测试请求
        resp = self.client.get('/v1_0/suggestion?q={}'.format('h' * 51))
        # 对状态码进行断言
        self.assertEqual(resp.status_code, 400, '参数q长度错误状态码不是400')


class SearchTestCase(unittest.TestCase):
    """文章搜索测试用例类"""
    def setUp(self):
        """每个测试方法启动前会调用"""
        print('测试初始化')

    def tearDown(self):
        """每个测试方法执行后会调用"""
        print("进行测试的资源回收")

    def test_request_normal(self):
        print("测试正常请求的情况123")


if __name__ == '__main__':
    unittest.main()  # 可以启动当前文件中的所有测试