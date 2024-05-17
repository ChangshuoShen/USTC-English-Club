# USTCEnglishClub

Hey Guys, this is a repo for USTC English Club's Websites. Hope it well-known around USTC, even the whole city, province, nation, world!!! 

<h1 align='center'>需求分析文档</h1>
<p align='right'>by: 申长硕 滕润喆

## 预期功能：

* 关于我们(主页)：
  
  * 关于EC
  
* 登陆模块：
  * 使用邮箱注册
  
* 活动相关：
  * 往期活动回顾
  * 活动预览
  
* 英语学习：
  * 英语学习资源分享模块
  
* 讨论板块
  * 留言板，comment，likes
  * 表白墙投稿功能
  
* 交友模块：
  * parter-finder：找口语/各种学习伙伴
  
* puzzle特别板块：
  * 往期puzzle
  * puzzle发帖，允许水友们发riddles
  
* 抽奖模块Raffle
  
  * 英语社活动为user做抽奖
  

（终极：英语学习大模型chat-en-learn（这个先把page建起来，之后慢慢训练部署





## 表：



### User

> **uid**  PK
>
> name
>
> email
>
> password
>
> register_date

### User_Profile

> **upid** PK
>
> uid R From User
>
> avatar(用户头像)
>
> birth_date
>
> gender
>
> bio
>
> education
>
> department

follow_table
> follow_id
> follower_id reference from user.uid
> be_followed_id reference from user.uid

实现的需求，正常显示数量，点击的话进行一些相关查询

> liked
>
> likes
>
> commented
>
> followed_num
>
> follow_num

### forum

post

> id PK
>
> post/riddle
>
> ans
>
> published_time
>
> likes

2 riddle_attribute
> r_id
> f_id reference from forum.id
> main_category
> answer_text
> difficulty

3 post_likes:

> id PK
>
> liker
>
> liked_id
>
> post_id references post. id

4 comments

> id PK
>
> comments/ans
>
> q_id references riddles. id
>
> commenter
>
> likes

5 comment_likes

> id PK
>
> liker
>
> liked
>
> on_ ques
>
> comment_id references comments. id

### activities

> id PK
>
> href
>
> img
>
> outline
>
> time

> id
>
> comment_text
>
> commenter references use. id
>
> act_id references activities. id 

### Raffle抽奖(grant 使用)

prizes

> id PK
>
> prize_name
>
> num
>
> rank难度等级