from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self,row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text,[row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		#伊利斯听说有一个很酷的在线待办事项应用
		#她去看了这个应用的首页
		self.browser.get(self.live_server_url)

		#她注意到网页的标题和头部都包含“To-Do”这个词
		self.assertIn('To-Do',self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do',header_text)
		
		#应用邀请她输入一个待办事项
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		#她在一个文本框内输入了“Buy peacock feathers”
		#伊利斯的爱好是使用家蝇做饵钓鱼
		inputbox.send_keys('Buy peacock feathers')

		#她按回车建后，页面更新了
		#待办事项表格中显示了“1：Buy peacock feathers”
		inputbox.send_keys(Keys.ENTER)
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url,'/lists/.+')		
		self.check_for_row_in_list_table('1:Buy peacock feathers')

		#页面中有显示了一个文本框，可以输入其他的待办事项
		#她输入了‘Use peacork feathers to make a fly“（使用孔雀羽毛做家蝇）
		#伊利斯做事很有条理
	
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		#import time
		#time.sleep(2)
		#页面再次更新，她的清单中显示了这两个待办事项
		self.check_for_row_in_list_table('1:Buy peacock feathers')
		self.check_for_row_in_list_table('2:Use peacock feathers to make a fly')
		
		#现在一个叫弗兰西斯的新用户访问了网站

		##我们使用一个新的浏览器会话
		##确保伊利斯的信息不会从cookie中泄露出来
		self.browser.quit()
		self.borwser = webdriver.Firefox()
		
		#弗兰西斯访问首页
		#页面中看不到伊利斯的清单
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').test
		self.assertNotIn('Buy peacock feathers',page_text)
	
		#弗兰西斯输入一个新的待办事项，新建一个清单
		#他不像伊利斯那么兴致盎然
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		#弗兰西斯获得了他的唯一Url
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url,'/lists/.+')
		self.assertNotEqual(francis_list_url,edith_list_url)

		#这个页面还是没有伊利斯的清单
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers',page_text)
		self.assertIn('Buy milk',page_text)

		#两个人都很满意，去睡觉了
