from pprint import pprint
import requests
import time
import random
import json


class PetChain(object):
    """
    定义一个类，莱茨狗
    """

    def __init__(self):
        # 初始化函数
        self.headers = self.get_headers()  # 获取最新请求头
        self.data = {
            'requestId': int(time.time() * 1000),
            'appId': '1',
            'tpl': "",
            'phoneType': "android"
        }  # 初始化post参数

    def get_headers(self):
        # 定义请求头，特别是cookie
        # 该函数用于将txt的请求头格式化
        headers = {}
        with open("./data/headers.txt") as f:
            lines = f.readlines()
        for line in lines:
            line_split = line.strip().split(":")
            key = line_split[0].strip()
            value = ":".join(line_split[1:]).strip()
            headers[key] = value
        return headers
        # pprint(self.headers)  # 打印请求头

    def get_post1(self, url):
        """
        :param url:请求的链接
        获取常规数据的post请求
        :return: response,返回请求结果，json数据返回
        """
        data = self.data.copy()  # 复制初始化的请求头
        data['requestId'] = int(time.time() * 1000)  # 更新请求的时间戳
        response = requests.post(url, headers=self.headers, data=json.dumps(data))  # 请求数据
        json_data = json.loads(response.text)
        return json_data

    def get_notice(self):
        """
        用于提取最新公告
        :return: 数据刷新时间，公告内容（list类型）
        """
        url = 'https://pet-chain.duxiaoman.com/data/notice/getVigorNotice'
        data = self.get_post1(url)  # 请求数据
        response_type = data['errorMsg']  # 获取返回状态
        if response_type == 'success':  # 如果返回成功
            response_time = data['timestamp']  # 获取更新时间
            response_contents = data['data']['contents']
            print(response_time)
            for response_content in response_contents:
                print(response_content)
            return response_contents  # 返回数据更新时间，公告内容
        else:
            return None

    def get_vigor_info(self):
        """
        获取我的狗窝数据
        :return:
        """
        url = 'https://pet-chain.duxiaoman.com/data/user/getVigorInfoByUser'
        data = self.get_post1(url)  # 请求数据
        print(data)
        response_type = data['errorMsg']  # 返回状态
        if response_type == 'success':  # 如果返回状态为成功
            response_time = data['timestamp']
            print('数据更新时间：', response_time)
            amount = data['data']['amount']  # 微积分值
            vigor = data['data']['vigor']  # 元气值
            pet_count = data['data']['petCount']  # 宠物狗数量
            print('微积分：{},元气值：{}，宠物狗数量：{}'.format(amount, vigor, pet_count))
            return amount, vigor, pet_count

    def get_task_info(self):
        """
        此函数用于获取任务完成情况
        :return:
        """
        url = 'https://pet-chain.duxiaoman.com/data/vigor/taskInfo'
        data = self.get_post1(url)  # 获取请求数据
        response_type = data['errorMsg']  # 返回状态
        if response_type == 'success':  # 如果返回状态为成功
            response_time = data['timestamp']
            print('数据更新时间：', response_time)
            data1 = data['data'][0]  # 每日登录奖励
            task_sign_in_type = data1['finished']  # 每日登录任务完成状态
            task_sign_in_reward = data1['reward']  # 单日登录奖励
            task_sign_in_total_reward = data1['totalReward']  # 累计登录奖励
            task_sign_in_num = data1['taskNum']  # 可完成数量
            task_sign_in_finished_num = data1['finishedNum']  # 已完成数量
            data2 = data['data'][1]  # 邀请奖励
            task_invited_type = data2['finished']  # 今日是否拉人
            task_invited_reward = data2['reward']  # 单次拉人奖励
            task_invited_total_reward = data2['totalReward']  # 累计邀请奖励
            task_invited_num = data2['taskNum']  # 可完成数量
            task_invited_finished_num = data2['finishedNum']  # 已完成数量
            data3 = data['data'][2]  # 实名认证
            task_real_auth_type = data3['finished']  # 实名认证完成情况
            task_real_auth_reward = data3['reward']  # 单次完成奖励
            task_real_auth_total_reward = data3['totalReward']  # 累计完成奖励
            task_real_auth_num = data3['taskNum']  # 可完成数量
            task_real_auth_finished_num = data3['finishedNum']  # 已完成数量
            print('今日登录奖励：{}'.format(task_sign_in_reward))
            print('累计登录奖励：{}，累计邀请奖励：{}，实名认证奖励{}'.format(task_sign_in_total_reward,
                  task_invited_total_reward,
                  task_real_auth_total_reward))
            print('已经邀请人数/可邀请人数：{}/{}'.format(task_invited_finished_num, task_invited_num,))
        else:
            time.sleep(random.random() + 1)
            self.get_task_info()  # 重新请求数据

    def query_pets_on_sale(self, sort_type: str = 'CREATETIME_ASC'):
        """
        用于对狗狗集市场的查询
        :param sort_type:排序方式，按价格，按时间，按稀有度
        查询狗狗集市中狗的销售情况
        :return:
        """

        url = 'https://pet-chain.duxiaoman.com/data/market/queryPetsOnSale'
        data = self.data.copy()  # 复制请求头
        data['pageNo'] = '1'  # 当前所在页数，默认第一页
        data['pageSize'] = '10'  # 请求数量，默认10个
        '''
        查询排序方式：
        AMOUNT_ASC：按微积分价格进行排序,降序
        CREATETIME_ASC:按出生时间进行排序，降序
        '''
        data['querySortType'] = sort_type
        data['petIds'] = []  # 狗狗id,这里默认留空
        data['lastAmount'] = ""
        data['lastRareDegree'] = ""
        data['filterCondition'] = "{}"
        # pprint(data)
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        data1 = json.loads(response.text)
        response_type = data1['errorMsg']  # 返回状态
        if response_type == 'success':
            data2 = data1['data']['petsOnSale']  # 在售的狗列表
            pprint(data2)
            amount_list = [x['amount'] for x in data2]  # 狗的价格列表
            bg_color_list = [x['bgColor'] for x in data2]  # 狗的背景颜色
            pet_nick = [x['desc'] for x in data2]  # 狗的昵称
            pet_generation = [x['generation'] for x in data2]  # 狗的代数
            pet_id_list1 = [x['id'] for x in data2]  # 狗狗显示的id
            pet_id_list2 = [x['petId'] for x in data2]  # 狗狗真实的id
            birth_type_list = [x['petType'] for x in data2]  # 狗的类型
            pet_url_list = [x['petUrl'] for x in data2]  # 狗的照片地址
            rare_degree_list = [x['rareDegree'] for x in data2]  # 狗的稀罕程度
            valid_code_list = [x['validCode'] for x in data2]  # 定价合理程度
            return data2
        else:
            print('请求参数错误')
            print(response.json())

    def query_pet_by_id(self, pet_id: str = '3929242894338361961'):
        """
        用于查询交易单个宠物狗的信息
        需要提供真实id号
        """
        url = 'https://pet-chain.duxiaoman.com/data/pet/queryPetById'
        data = self.data.copy()  # 拷贝请求参数
        data['petId'] = pet_id  # 宠物真实id,20位数
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        data1 = response.json()
        response_type = data1['errorMsg']
        if response_type == 'success':  # 如果返回成功
            data2 = data1['data']
            pprint(data2)
            amount = data2['amount']  # 价格
            attributes = data2['attributes']  # 特征
            bg_color = data2['bgColor']  # 背景颜色
            can_breed = data2['canBreed']  # 能否繁育
            pet_age = data2['coolingInterval']  # 狗龄
            pet_nick = data2['desc']  # 狗的昵称
            pet_father = data2['father']  # 狗父
            pet_mother = data2['mother']  # 狗母
            generation = data2['generation']  # 狗的代数
            head_icon = data2['headIcon']  # 持有人头像
            pet_id1 = data2['id']  # 狗的显示id
            is_cooling = data2['isCooling']  # 是否休息中
            is_on_chain = data2['isOnChain']  # 是否上链
            last_breed_time = data2['lastBreedTime']  # 最近更新时间
            lock_status = data2['lockStatus']  # 锁定状态
            pet_name = data2['name']  # 狗的名称
            pet_id2 = data2['petId']  # 狗的真实id
            pet_url = data2['petUrl']  # 狗的图片链接
            rare_degree = data2['rareDegree']  # 狗的稀罕程度
            shelf_status = data2['shelfStatus']  # 单身状态
            pet_master = data2['userName']  # 狗的主人
        else:
            print('请求参数错误')
            print(response.json())

    def one_key_collection(self):
        """
        用于微积分的一键收取
        """
        url = 'https://pet-chain.duxiaoman.com/data/vigor/getall'
        data = self.get_post1(url)
        print(data)
        response_type = data['errorMsg']
        if response_type == '微积分聚集中,请耐心等待微积分生成':
            return '收取失败，请耐心等待'
        else:
            amount_list = data['data']['amount']
            amount_sum = 0
            for amount in amount_list:
                amount_sum += float(amount)  # 累计求和
            return '收取成功，本次共收取微积分：{}'.format(amount_sum)

    def get_purchase(self, pet_id2, pet_valid_code: str = None):
        """
        此函数用于模拟点击购买
        点击购买后将会触发验证码
        输入完验证码后才可能可以购买
        :params pet_id2:宠物狗的真实id
        :params pet_valid_code:宠物狗的价格合理代码，一般都是空
        """
        url = 'https://pet-chain.duxiaoman.com/data/user/pwdHint'
        data = self.data.copy()  # 复制请求信息
        headers = self.headers.copy()  # 复制请求头
        headers['Referer'] = "https://pet-chain.duxiaoman.com/chain/detail?\
        channel=market&petId={}&validCode={}&appId=1&tpl=".format(pet_id2, pet_valid_code)
        response = requests.post(url, data=json.dumps(data), headers=headers)  # 提交购买请求
        pass
        # 没有微积分测试，暂时不写

    def get_captcha(self, pet_id2, pet_valid_code: str = None):
        """
        此函数用于获取验证码
        """
        url = 'https://pet-chain.duxiaoman.com/data/newCaptcha/getCaptchaUrl'
        data = self.data.copy()  # 复制请求信息
        headers = self.headers.copy()  # 复制请求头
        headers['Referer'] = "https://pet-chain.duxiaoman.com/chain/detail?\
                channel=market&petId={}&validCode={}&appId=1&tpl=".format(pet_id2, pet_valid_code)
        response = requests.post(url, data=json.dumps(data), headers=headers)  # 提交,获取验证码
        data1 = response.json()
        response_type = data1['errorMsg']  # 返回状态
        if response_type == 'success':
            captcha_url = data1['data']  # 验证码地址
            response2 = requests.get(url=captcha_url, headers=headers)
            img_data = response2.text  # 图片二进制
            pass
            # 后面考虑AI识别，暂停编写






if __name__ == '__main__':
    pet = PetChain()
    # pc.get_notice()
    # pc.get_vigor_info()
    # pc.get_task_info()
    # pet.query_pets_on_sale()
    # pet.one_key_collection()
    pet.query_pet_by_id()
