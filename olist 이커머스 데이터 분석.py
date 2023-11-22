#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import math


# In[2]:


# 그래프를 출력할 때 한글 글씨체 사용
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


# # 데이터 불러오기

# In[3]:


customer_df = pd.read_csv('./olist_customers_dataset.csv')
customer_df


# In[4]:


geolocation_df = pd.read_csv('./olist_geolocation_dataset.csv')
geolocation_df


# In[5]:


order_items_df = pd.read_csv('./olist_order_items_dataset.csv')
order_items_df


# In[6]:


order_payments_df = pd.read_csv('./olist_order_payments_dataset.csv')
order_payments_df


# In[7]:


order_reviews_df = pd.read_csv('./olist_order_reviews_dataset.csv')
order_reviews_df


# In[8]:


orders_df = pd.read_csv('./olist_orders_dataset.csv')
orders_df


# In[9]:


products_df = pd.read_csv('./olist_products_dataset.csv')
products_df


# In[10]:


sellers_df = pd.read_csv('./olist_sellers_dataset.csv')
sellers_df


# In[11]:


category_name_df = pd.read_csv('./product_category_name_translation.csv')
category_name_df


# In[12]:


orders_df


# In[13]:


customer_df


# # 데이터 전처리

# In[14]:


# 데이터 합치기
olist_df = pd.merge(orders_df, order_payments_df, on = 'order_id')
olist_df = olist_df.merge(customer_df, on = 'customer_id')
olist_df = olist_df.merge(order_items_df, on = 'order_id')
olist_df = olist_df.merge(products_df, on = 'product_id')
olist_df = olist_df.merge(category_name_df, on = 'product_category_name')
olist_df = olist_df.merge(order_reviews_df, on = 'order_id')
olist_df = olist_df.merge(sellers_df, on = 'seller_id')


# In[15]:


olist_df.info()


# In[16]:


olist_df.duplicated(subset = 'order_id').value_counts()


# In[17]:


# 중복 행 제거
olist_df.duplicated(subset = 'order_id').value_counts()

olist_df = olist_df[~olist_df.duplicated(['order_id'])]

# 인덱스 초기화
olist_df = olist_df.reset_index()
olist_df = olist_df.drop(columns = {'index'})


# In[18]:


# datetime 형식으로 구매 일자 변경
date_time = olist_df['order_purchase_timestamp'].str.split()

date_list = []
time_list = []
for x in range(date_time.shape[0]) :
    date_list.append(date_time[x][0])
    time_list.append(date_time[x][1])
    
olist_df['purchase_date'], olist_df['purchase_time'] = date_list, time_list
olist_df = olist_df.drop(columns = {'order_purchase_timestamp'})

olist_df['purchase_date'] = pd.to_datetime(olist_df['purchase_date'])


# In[19]:


# 구매 일자를 연, 월, 요일별로 분해
olist_df['year'] = olist_df['purchase_date'].dt.year
olist_df['month'] = olist_df['purchase_date'].dt.month
olist_df['day_of_week'] = olist_df['purchase_date'].dt.day_name()


# In[20]:


# olist_df['purchase_time']에 시간 값만 저장
olist_df['purchase_time'] = olist_df['purchase_time'].str.slice(0, 2)


# In[21]:


olist_df.info()


# In[22]:


# 주 이름을 한글로 바꾸는 함수
def get_kor_state(state) :
    if state == 'AC' :
        state_kor_name = '아크리주'
    elif state == 'AL' :
        state_kor_name = '알라고아스주'
    elif state == 'AP' :
        state_kor_name = '아마파주'
    elif state == 'AM' :
        state_kor_name = '아마조나스주'
    elif state == 'BA' :
        state_kor_name = '바이아주'
    elif state == 'CE' :
        state_kor_name = '세아라주'
    elif state == 'DF' :
        state_kor_name = '연방구'
    elif state == 'ES' :
        state_kor_name = '이스피리투산투주'
    elif state == 'GO' :
        state_kor_name = '고이아스주'
    elif state == 'MA' :
        state_kor_name = '마라냥주'
    elif state == 'MT' :
        state_kor_name = '마투그로수주'
    elif state == 'MG' :
        state_kor_name = '미나스제라이스주'
    elif state == 'PA' :
        state_kor_name = '파라주'
    elif state == 'PB' :
        state_kor_name = '파라이바주'
    elif state == 'PR' :
        state_kor_name = '파라나주'
    elif state == 'PE' :
        state_kor_name = '페르남부쿠주'
    elif state == 'PI' :
        state_kor_name = '피아우이주'
    elif state == 'RJ' :
        state_kor_name = '리우데자네이루주'
    elif state == 'RN' :
        state_kor_name = '히우그란지두노르치주'
    elif state == 'RS' :
        state_kor_name = '히우그란지두술주'
    elif state == 'RO' :
        state_kor_name = '혼도니아주'
    elif state == 'RR' :
        state_kor_name = '호라이마주'
    elif state == 'SC' :
        state_kor_name = '산타카타리나주'
    elif state == 'SP' :
        state_kor_name = '상파울루주'
    elif state == 'SE' :
        state_kor_name = '세르지피주'
    elif state == 'MS' :
        state_kor_name = '마투그로수두술'
    else :
        state_kor_name = '토칸칭스주'
    return state_kor_name


# In[23]:


# state를 입력받으면 지역을 return하는 함수
def get_region(state) :
    if (state == 'SP' or state == 'MG' or state == 'ES' or state == 'RJ') : 
        region = '남동부'
    elif (state == 'PR' or state == 'SC' or state == 'RS') : 
        region = '남부'
    elif (state == 'BA' or state == 'PE' or state == 'CE' or state == 'RN' or state == 'PI' or state == 'MA' or state == 'SE' or state == 'AL' or state == 'PB') : 
        region = '북동부'
    elif (state == 'GO' or state == 'MT' or state == 'MS' or state == 'DF') : 
        region = '중서부'
    else : 
        region = '북부'
    return region


# In[24]:


# 판매자 거주 지역 컬럼 추가
for index, row in olist_df.iterrows():
    state = row['seller_state']
    region = get_region(state)
    olist_df.at[index,'seller_region'] = region

# 구매자 거주 지역 컬럼 추가
for index, row in olist_df.iterrows():
    state = row['customer_state']
    region = get_region(state)
    olist_df.at[index,'customer_region'] = region
    
olist_df


# In[25]:


# 주의 한글 이름 컬럼 추가
for index, row in olist_df.iterrows():
    state = row['customer_state']
    kor_name = get_kor_state(state)
    olist_df.at[index,'kor_state'] = kor_name
    
olist_df


# # EDA

# ### 거주 주별 고객 수

# In[26]:


customer_state_df = olist_df['customer_state']


# In[27]:


customer_state_df = pd.DataFrame(customer_state_df.value_counts())
customer_state_df = customer_state_df.reset_index()
customer_state_df = customer_state_df.rename(columns = {'index' : 'state'})
customer_state_df


# In[28]:


px.pie(customer_state_df, values='customer_state', names='state', 
       color_discrete_sequence=px.colors.qualitative.Pastel1 + px.colors.qualitative.Pastel2)


# 고객이 가장 많이 거주하고 있는 주로는 상파울루주로 고객의 42%가 상파울루주에 거주하고 있는 것을 알 수 있다. 다음으로는 리우데자네이루주, 미나스제라이스주, 히우그란지두술주 순으로 이어지며 이는 주별 인구수와 비슷한 결과를 나타내고 있다.

# ### 카테고리 별 주문 건수

# In[29]:


category_df = pd.DataFrame(olist_df['product_category_name_english'].value_counts())
category_df = category_df.reset_index()
category_df = category_df.rename(columns = {'index' : 'category', 'product_category_name_english' : 'count'})
category_df


# In[30]:


px.bar(category_df, x="category", y='count',
       labels={"category":"카테고리","count":"총 주문건수"}, 
       title='카테고리별 주문 건수', color = px.colors.qualitative.Pastel1 + px.colors.qualitative.Pastel2 + px.colors.qualitative.Pastel + px.colors.qualitative.Light24 + px.colors.qualitative.Safe + px.colors.qualitative.Set2, 
       color_discrete_map='identity')


# 다음 그래프에서는 카테고리별 주문 건수를 확인할 수 있다. 주문 건수가 가장 많은 상위 5개의 카테고리로는 'bed_bath_table', 'health_beauty', 'sports_leisure', 'computers_accessories', 'furniture_decor' 순이고, 주문 건수가 가장 적은 하위 5개의 카테고리는 'home_comfort_2', 'la_cuisine', 'cds_dvds_musicals', 'fashion_childrens_clothes', 'security_and_services' 이다.

# ### 매출액 추이

# In[31]:


date_purchase_df = olist_df[['payment_value', 'purchase_date', 'year', 'month', 'day_of_week']]
date_purchase_df


# In[32]:


date_purchase_df['purchase_date'].describe()


# In[33]:


date_purchase_pt = pd.pivot_table(data = date_purchase_df, 
                                   index = 'purchase_date', 
                                   values = 'payment_value', 
                                   aggfunc = 'sum').reset_index()
date_purchase_pt


# In[34]:


date_purchase_pt2 = pd.pivot_table(data = date_purchase_df, 
                                   index = 'purchase_date', 
                                   values = 'payment_value', 
                                   aggfunc = 'count').reset_index()
date_purchase_pt2


# In[35]:


date_purchase_pt = pd.merge(date_purchase_pt, date_purchase_pt2, on = 'purchase_date')
date_purchase_pt = date_purchase_pt.rename(columns = {'payment_value_x':'payment_value', 'payment_value_y':'payment_count'})
date_purchase_pt


# In[36]:


px.line(date_purchase_pt, x = 'purchase_date', y = 'payment_value',
        labels={"purchase_date":"날짜","payment_value":"매출액"},
        title='매출액 추이')


# 다음 그래프는 2016년 9월 4일부터 2018년 9월 3일 까지의 데이터로 이루어진  매출액 추이를 나타낸 그래프로, 서비스가 오픈한 후부터 2017년 초까지는 매출액이 저조하다가 2017년 2~3월 부터 매출액이 증가하기 시작하는 것을 확인할 수 있다. 다음 그래프에서 유독 매출액이 비정상적으로 상승한 날짜를 살펴볼 수 있는데 이는 2017년 11월 24일로 이 날은 블랙프라이데이라고 한다.

# ### 연도별 매출액

# In[37]:


# 연도별 매출액의 합계 피벗테이블 생성
year_purchase_pt = pd.pivot_table(data = date_purchase_df, 
                                  index = 'year',
                                  values = 'payment_value',
                                  aggfunc = 'sum').reset_index()
# 연도별 주문 건수 피벗테이블 생성
year_purchase_pt2 = pd.pivot_table(data = date_purchase_df, 
                                  index = 'year',
                                  values = 'payment_value',
                                  aggfunc = 'count').reset_index()
year_purchase_pt = pd.merge(year_purchase_pt, year_purchase_pt2, on = 'year')
year_purchase_pt = year_purchase_pt.rename(columns = {'payment_value_x' : 'value_sum', 'payment_value_y' : 'value_count'})
year_purchase_pt


# In[38]:


# 막대그래프 = 연도별 주문 건수, 선그래프 = 연도별 매출액
matplotlib.rc_file_defaults()
ax1 = sns.set_style(style=None, rc=None )

fig, ax1 = plt.subplots(figsize=(12,6))

sns.lineplot(data = year_purchase_pt['value_sum'], marker='o', sort = False, ax=ax1)
ax2 = ax1.twinx()

sns.barplot(year_purchase_pt, x='year', y='value_count', alpha=0.5, ax=ax2)


# 해당 그래프는 연도별 매출액과 주문건수를 시각화한 그래프로 2016년부터 2018년까지 시간이 지날수록 매출액과 주문건수가 증가했음을 확인할 수 있다.

# ### 월별 매출액

# In[39]:


# 월별 매출액의 합계 피벗테이블 생성
month_purchase_pt = pd.pivot_table(data = date_purchase_df,
                                   index = 'month',
                                   values = 'payment_value',
                                   aggfunc = 'sum').reset_index()
# 월별 주문 건수 피벗테이블 생성
month_purchase_pt2 = pd.pivot_table(data = date_purchase_df, 
                                  index = 'month',
                                  values = 'payment_value',
                                  aggfunc = 'count').reset_index()
month_purchase_pt = pd.merge(month_purchase_pt, month_purchase_pt2, on = 'month')
month_purchase_pt = month_purchase_pt.rename(columns = {'payment_value_x' : 'value_sum', 'payment_value_y' : 'value_count'})
month_purchase_pt


# In[40]:


# 막대그래프 = 월별 주문 건수, 선그래프 = 월별 매출액
matplotlib.rc_file_defaults()
ax1 = sns.set_style(style=None, rc=None )

fig, ax1 = plt.subplots(figsize=(12,6))

sns.lineplot(data = month_purchase_pt['value_sum'], marker='o', sort = False, ax=ax1)
ax2 = ax1.twinx()

sns.barplot(month_purchase_pt, x='month', y='value_count', alpha=0.5, ax=ax2)


# 해당 그래프는 월별 매출액과 주문 건수를 시각화한 그래프로 9 ~ 12월 데이터와 1 ~ 2월 데이터가 서비스를 오픈한지 얼마 되지않았던 2016년 데이터와 2017년 데이터 밖에 존재하지 않아 다른 달보다 매출액과 주문건수가 적게 표현된 것을 확인할 수 있다. 이를 제외하고 5월과 8월에 매출액과 주문 건수가 다른 달에 비해 높은 것을 확인할 수 있다.

# ### 요일별 매출액

# In[41]:


# 요일별 매출액의 합계 피벗테이블 생성
dayofweek_purchase_pt = pd.pivot_table(data = date_purchase_df,
                                       index = 'day_of_week',
                                       values = 'payment_value',
                                       aggfunc = 'sum').reset_index()
# 요일별 주문 건수 피벗테이블 생성
dayofweek_purchase_pt2 = pd.pivot_table(data = date_purchase_df, 
                                  index = 'day_of_week',
                                  values = 'payment_value',
                                  aggfunc = 'count').reset_index()
dayofweek_purchase_pt = pd.merge(dayofweek_purchase_pt, dayofweek_purchase_pt2, on = 'day_of_week')
dayofweek_purchase_pt = dayofweek_purchase_pt.rename(columns = {'payment_value_x' : 'value_sum', 'payment_value_y' : 'value_count'})
dayofweek_purchase_pt


# In[42]:


# 인덱스 재배열
dayofweek_purchase_pt = dayofweek_purchase_pt.reindex([3, 1, 5, 6, 4, 0, 2])
dayofweek_purchase_pt = dayofweek_purchase_pt.reset_index()
dayofweek_purchase_pt = dayofweek_purchase_pt.drop(columns = {'index'})
dayofweek_purchase_pt


# In[43]:


# 막대그래프 = 요일별 주문 건수, 선그래프 = 요일별 매출액
matplotlib.rc_file_defaults()
ax1 = sns.set_style(style=None, rc=None )

fig, ax1 = plt.subplots(figsize=(12,6))

sns.lineplot(data = dayofweek_purchase_pt['value_sum'], marker='o', sort = False, ax=ax1)
ax2 = ax1.twinx()

sns.barplot(dayofweek_purchase_pt, x='day_of_week', y='value_count', alpha=0.5, ax=ax2)


# 다음 그래프는 요일대별 매출액과 주문건수를 표현한 그래프로 월요일과 그보다 미세하게 떨어진 화요일, 수요일에 가장 매출액과 주문 건수가 높았습니다. 이는 대부분에 사람들이 주말보다는 주중에 쇼핑을 하는 것을 선호하는 것을 확인할 수 있다.

# # 시간대별 매출액

# In[44]:


time_purchase_df = olist_df[['payment_value', 'purchase_time']]
time_purchase_df


# In[45]:


# 시간별 매출액의 합계 피벗테이블 생성
time_purchase_pt = pd.pivot_table(data = time_purchase_df, 
                                   index = 'purchase_time', 
                                   values = 'payment_value', 
                                   aggfunc = 'sum').reset_index()
# 시간별 주문 건수 피벗테이블 생성
time_purchase_pt2 = pd.pivot_table(data = time_purchase_df, 
                                  index = 'purchase_time',
                                  values = 'payment_value',
                                  aggfunc = 'count').reset_index()
time_purchase_pt = pd.merge(time_purchase_pt, time_purchase_pt2, on = 'purchase_time')
time_purchase_pt = time_purchase_pt.rename(columns = {'payment_value_x' : 'value_sum', 'payment_value_y' : 'value_count'})
time_purchase_pt


# In[46]:


# 막대그래프 = 시간대별 주문 건수, 선그래프 = 시간대별 매출액
matplotlib.rc_file_defaults()
ax1 = sns.set_style(style=None, rc=None )

fig, ax1 = plt.subplots(figsize=(12,6))

sns.lineplot(data = time_purchase_pt['value_sum'], marker='o', sort = False, ax=ax1)
ax2 = ax1.twinx()

sns.barplot(time_purchase_pt, x='purchase_time', y='value_count', alpha=0.5, ax=ax2)


# 다음은 시간대별 매출액과 주문건수에 대한 그래프로 사람들이 잠에 드는 오후 11시 ~ 오전 8시까지는 매출액과 주문 건수가 적은 것을 확인할 수 있고, 오전 10시 ~ 오후 4시 시간대에 가장 쇼핑을 많이 하는 것을 확인할 수 있다.

# ### 결제 유형

# In[47]:


payment_type_df = pd.DataFrame(olist_df['payment_type'].value_counts())
payment_type_df = payment_type_df.reset_index()
payment_type_df = payment_type_df.rename(columns = {'index' : 'payment_type', 'payment_type' : 'total'})
payment_type_df


# In[48]:


px.bar(payment_type_df, x = 'payment_type', y = 'total',
       labels={"payment_type":"결제 유형","total":"총 주문 건수"},
       title='결제 유형별 총 주문 건수', 
       color=["#e6bab1", "#f2a47d", "rgb(241,235,156)", "rgb(188,209,155)"], color_discrete_map="identity")


# 다음 그래프는 결제 유형별 주문 건수에 대한 그래프로 주문의 70%정도가 신용카드로 결제하는 것을 확인할 수 있다. 뒤이어 볼레토, 바우처, 직불카드 순으로 결제를 선호한다고 볼 수 있다.

# ### 할부 개월별 주문 건수

# In[49]:


payment_installments_df = pd.DataFrame(olist_df['payment_installments'].value_counts())
payment_installments_df = payment_installments_df.reset_index()
payment_installments_df = payment_installments_df.rename(columns = {'index' : 'payment_installments', 'payment_installments' : 'total'})
payment_installments_df = payment_installments_df.sort_values(by='payment_installments' ,ascending = True)
payment_installments_df


# In[50]:


px.bar(payment_installments_df, x = 'payment_installments', y = 'total',
       labels={'payment_installments' : '할부 개월', 'total' : '주문 건수'},
       title='할부 개월별 주문 건수', 
       color=['rgb(229,225,230)','rgb(234,211,226)','rgb(229,206,219)','rgb(228,198,212)','rgb(233,205,208)','rgb(242,212,215)', 
              'rgb(245,218,223)','rgb(235,228,154)','rgb(224,192,159)','rgb(237,200,163)','rgb(220,213,154)','rgb(209,224,215)',
              'rgb(184,221,225)','rgb(164,219,232)','rgb(209,221,230)','rgb(219,226,233)','rgb(221,229,237)','rgb(209,244,215)',
              'rgb(209,244,215)','rgb(209,244,215)','rgb(209,244,215)','rgb(209,244,215)','rgb(209,244,215)','rgb(241,135,156)'], 
       color_discrete_map="identity")


# 다음 그래프는 할부 개월별 주문 건수로 할부를 1개월로 하는 주문이 가장 많고 뒤를 이어 2 ~ 5월 순으로 주문 건수가 많은 것을 확인할 수 있다. 이는 브라질에서의 할부금은 대출과 같으며 매우 높은 이자율을 가지고 있기 때문으로 볼 수 있다.  

# ### 카테고리별 평균 배송 시간

# In[51]:


category_delivery_df = olist_df[['product_category_name_english', 'purchase_date', 'order_delivered_customer_date']].dropna(axis = 0).reset_index().drop(columns = {'index'})


# In[52]:


# 배송된 날짜만 추출
delivered_date = category_delivery_df['order_delivered_customer_date'].str.split()

delivered_date_list = []
for x in range(delivered_date.shape[0]) :
    delivered_date_list.append(delivered_date[x][0])
    
delivered_date_list


# In[53]:


category_delivery_df['order_delivered_customer_date'] = pd.to_datetime(delivered_date_list)
category_delivery_df


# In[54]:


category_delivery_df['delivered_date'] = category_delivery_df['order_delivered_customer_date'] - category_delivery_df['purchase_date']
category_delivery_df = category_delivery_df.drop(columns = {'order_delivered_customer_date', 'purchase_date'})
category_delivery_df


# In[55]:


# 카테고리별 배송까지 걸린 날짜의 평균 피벗테이블 생성
category_delivery_pt = pd.pivot_table(data = category_delivery_df, 
                                   index = 'product_category_name_english', 
                                   values = 'delivered_date', 
                                   aggfunc = 'mean').reset_index()
category_delivery_pt = category_delivery_pt.sort_values(by = 'delivered_date', ascending=True)
category_delivery_pt['delivered_date'] = category_delivery_pt['delivered_date'].dt.days
category_delivery_pt


# In[56]:


px.line(category_delivery_pt, 
        x = 'product_category_name_english', 
        y = 'delivered_date',
        labels={'product_category_name_english' : '카테고리 명', 'delivered_date' : '평균 배송 시간'}, 
        title = '카테고리별 평균 배송 시간')


# 다음 그래프는 카테고리별 평균 배송시간을 시각화한 것으로 가장 배송시간이 빠른 카테고리는 'arts_and_craftmanship' 이며, 'la_cuisine', 'books_imported', 'party_supplies', 'fashion_childrens_clothes' 가 뒤를 잇는 것을 확인할 수 있다. 반대로 가장 배송시간이 느린 카테고리는 'office_furniture'이며 평균 배송시간은 20일이다. 뒤를 이어 'fashion_shoes', 'home_comfort_2', 'christmas_supplies', 'security_and_services' 등이 있다.

# ### 배송시간별 평균 평점

# In[57]:


delivery_score_df = olist_df[['order_delivered_customer_date', 'purchase_date', 'review_score']].dropna(axis = 0).reset_index()
delivery_score_df = delivery_score_df.drop(columns = {'index'})
delivery_score_df


# In[58]:


delivered_date = delivery_score_df['order_delivered_customer_date'].str.split()

delivered_date_list = []
for x in range(delivered_date.shape[0]) :
    delivered_date_list.append(delivered_date[x][0])
    
delivered_date_list


# In[59]:


delivery_score_df['order_delivered_customer_date'] = pd.to_datetime(delivered_date_list)
delivery_score_df


# In[60]:


delivery_score_df['delivered_date'] = delivery_score_df['order_delivered_customer_date'] - delivery_score_df['purchase_date']
delivery_score_df = delivery_score_df.drop(columns = {'order_delivered_customer_date', 'purchase_date'})
delivery_score_df['delivered_date'] = delivery_score_df['delivered_date'].dt.days
delivery_score_df


# In[61]:


delivery_dic = {1 : '0~5days', 2 : '5~10days', 3 : '10~15days', 4 : '15~20days', 5 : '20days~'}

delivery_legend_list = []
for date in delivery_score_df['delivered_date'] :
    if 0 <= date < 5 :
        delivery_legend_list.append(1)
    elif 5 <= date < 10 :
        delivery_legend_list.append(2)
    elif 10 <= date < 15 :
        delivery_legend_list.append(3)
    elif 15 <= date < 20 :
        delivery_legend_list.append(4)
    else :
        delivery_legend_list.append(5)
        
delivery_legend_list


# In[62]:


delivery_score_df['delivery_legend'] = delivery_legend_list
delivery_score_df


# In[63]:


delivery_score_pt = pd.pivot_table(data = delivery_score_df, 
                                   index = 'delivery_legend', 
                                   values = 'review_score', 
                                   aggfunc = 'mean').reset_index()
delivery_score_pt


# In[64]:


delivery_score_pt['delivery_legend'] = delivery_dic.values()
delivery_score_pt


# In[65]:


px.bar(delivery_score_pt, x = 'delivery_legend', y = 'review_score', 
       labels = {'delivery_legend' : '배송시간', 'review_score' : '평균 평점'}, 
       title='배송시간별 평균 평점', color=["rgb(239,209,159)", "rgb(255,185,144)", "rgb(255,190,159)", "rgb(255,163,139)", "rgb(255,179,171)"], 
       color_discrete_map="identity")


# 다음 그래프는 배송시간에 따른 평점을 알아본 그래프로 배송 시간이 길수록 고객의 서비스 불만족이 높아지고 부정적인 리뷰를 받을 가능성이 높아진다고 말할 수 있다.

# ### 주문 상태 분포

# In[66]:


order_status_df = pd.DataFrame(olist_df['order_status'].value_counts()).reset_index()
order_status_df = order_status_df.rename(columns = {'index' : 'order_status', 'order_status' : 'total'})
order_status_df


# In[67]:


px.pie(order_status_df, names='order_status', values='total', color_discrete_sequence=px.colors.qualitative.Pastel1)


# 다음 파이 차트는 주문 현황에 대한 데이터로 배송된 주문이 대부분을 차지한다. 배송된 주문을 제외한 나머지 데이터중에서 취소된 주문이 42%, 청구서가 발행된 주문이 29%, 처리중인 주문이 28%로 확인할 수 있다.

# ### 카테고리별 실제 배송 날짜와 예상 배송일 차이

# In[68]:


category_delivery_dif_df = olist_df[['product_category_name_english', 'purchase_date', 'order_estimated_delivery_date', 'order_delivered_customer_date']].dropna(axis = 0).reset_index()
category_delivery_dif_df = category_delivery_dif_df.drop(columns = {'index'})
category_delivery_dif_df


# In[69]:


# 결측치 확인
category_delivery_dif_df.isnull().sum()


# In[70]:


order_estimated_delivery_date_list = category_delivery_dif_df['order_estimated_delivery_date'].str.split()
order_delivered_customer_date_list = category_delivery_dif_df['order_delivered_customer_date'].str.split()


# In[71]:


estimated_date_list = []
delivered_date_list = []
for x in range(order_estimated_delivery_date_list.shape[0]) :
    estimated_date_list.append(order_estimated_delivery_date_list[x][0])
    delivered_date_list.append(order_delivered_customer_date_list[x][0])


# In[72]:


category_delivery_dif_df['order_estimated_delivery_date'] = pd.to_datetime(estimated_date_list)
category_delivery_dif_df['order_delivered_customer_date'] = pd.to_datetime(delivered_date_list)


# In[73]:


category_delivery_dif_df


# In[74]:


category_delivery_dif_df['exp_date'] = (category_delivery_dif_df['order_estimated_delivery_date'] - category_delivery_dif_df['purchase_date']).dt.days
category_delivery_dif_df['act_date'] = (category_delivery_dif_df['order_delivered_customer_date'] - category_delivery_dif_df['purchase_date']).dt.days
category_delivery_dif_df = category_delivery_dif_df.drop(columns = {'order_delivered_customer_date', 'purchase_date', 'order_estimated_delivery_date'})
category_delivery_dif_df


# In[75]:


(category_delivery_dif_df['act_date'] >= 20).sum()


# In[76]:


category_delivery_dif_pt = pd.pivot_table(data=category_delivery_dif_df, 
                                          index='product_category_name_english', 
                                          values = ['exp_date', 'act_date'], 
                                          aggfunc= 'mean').reset_index().rename(columns = {'index' : 'product_category_name_english'})
category_delivery_dif_pt


# In[77]:


matplotlib.rc_file_defaults()
ax1 = sns.set_style(style=None, rc=None )

fig, ax1 = plt.subplots(figsize=(12,6))

sns.lineplot(data = category_delivery_dif_pt['act_date'], marker='o', sort = False, ax=ax1).set(ylim=(0, 35))
ax2 = ax1.twinx()

sns.lineplot(data = category_delivery_dif_pt, x='product_category_name_english', y='exp_date', 
             alpha=0.5, ax=ax2, marker='o', color = 'r').set(ylim=(0, 35))


# 다음 그래프는 카테고리별 예상 배송시간과 실제 배송시간을 나타낸 그래프로 예상 배송 시간과 실제 배송 시간 사이에 대략 두배 정도의 차이가 있는 것을 확인할 수 있다. 예를 들어 '농업과 상업' 카테고리에 경우 예상 배송 시간은 약 22일이고 실제 배송 시간은 약 11일 정도 소요되었다.

# ### 제품의 부피, 무게별 제품 수

# In[78]:


product_volume_df = products_df[['product_length_cm','product_height_cm','product_width_cm']]
product_weight_df = products_df[['product_weight_g']]
product_volume_df


# In[79]:


product_weight_df


# In[80]:


product_volume_df['volume'] = product_volume_df['product_length_cm'] * product_volume_df['product_height_cm'] * product_volume_df['product_width_cm']
product_volume_df = product_volume_df.drop(columns = {'product_length_cm', 'product_height_cm', 'product_width_cm'})
product_volume_df


# In[81]:


product_volume_list = []
for volume in product_volume_df['volume'] :
    if 0 <= volume < 5000 :
        product_volume_list.append(1)
    elif 5000 <= volume < 10000 :
        product_volume_list.append(2)
    elif 10000 <= volume < 30000 :
        product_volume_list.append(3)
    elif 30000 <= volume < 50000 :
        product_volume_list.append(4)
    else :
        product_volume_list.append(5)
        
product_weight_list = []
for weight in product_weight_df['product_weight_g'] :
    if 0 <= weight < 1000 :
        product_weight_list.append(1)
    elif 1000 <= weight < 3000 :
        product_weight_list.append(2)
    elif 3000 <= weight < 7000 :
        product_weight_list.append(3)
    elif 7000 <= weight < 15000 :
        product_weight_list.append(4)
    else :
        product_weight_list.append(5)
        
product_weight_list


# In[82]:


product_volume_df['volume_legend'] = product_volume_list
product_weight_df['weight_legend'] = product_weight_list


# In[83]:


product_volume_pt = pd.pivot_table(data = product_volume_df, 
                                   index = 'volume_legend', 
                                   values = 'volume', 
                                   aggfunc = 'count').reset_index()
product_volume_pt


# In[84]:


product_weight_pt = pd.pivot_table(data = product_weight_df, 
                                   index = 'weight_legend', 
                                   values = 'product_weight_g', 
                                   aggfunc = 'count').reset_index()
product_weight_pt


# In[85]:


weight_dic = {1:'매우 가벼움', 2 : '가벼움', 3 : '보통', 4 : '무거움', 5 : '매우 무거움'}
volume_dic = {1:'매우 작음', 2:'작음', 3:'보통', 4:'큼', 5:'매우 큼'}
product_volume_pt['volume_legend'] = volume_dic.values()
product_weight_pt['weight_legend'] = weight_dic.values()
product_volume_pt


# In[86]:


from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=1, cols=2, shared_yaxes=True)

fig.add_trace(go.Bar(x=list(product_volume_pt['volume_legend']), y=list(product_volume_pt['volume']),
                    marker=dict(color=[0, 3, 6], coloraxis="coloraxis")),
              1, 1)

fig.add_trace(go.Bar(x=list(product_weight_pt['weight_legend']), y=list(product_weight_pt['product_weight_g']),
                    marker=dict(color=[0, 3, 6], coloraxis="coloraxis")),
              1, 2)

fig.update_layout(coloraxis=dict(colorscale='peach'), showlegend=False)
fig.show()


# 다음 그래프는 제품의 부피, 무게별 제품의 수를 나타낸 것으로 부피의 경우 0 ~ 5000 cm^3 을 매우 작음, 5000 ~ 10000 cm^3 을 작음, 10000 ~ 30000 cm^3 을 보통, 30000 ~ 50000 cm^3 을 큼, 50000 cm^3 이상을 매우 큼으로 표시했고, 무게의 경우 0 ~ 1kg 을 매우 가벼움, 1~ 3 kg 을 가벼움, 3 ~ 7 kg을 보통, 7 ~ 15kg을 무거움, 15kg 이상을 매우 무거움으로 표시했다. 부피에서는 매우 작은 제품이 가장 많이 나타났고, 무게에서는 매우 가벼운 제품이 가장 많이 나타났다.

# ### 카테고리별 평균 평점

# In[87]:


category_score_df = olist_df[['product_category_name_english', 'review_score']]
category_score_df


# In[88]:


category_score_pt = pd.pivot_table(data = category_score_df, 
                                   index='product_category_name_english', 
                                   values='review_score', 
                                   aggfunc='mean').reset_index()
category_score_pt = category_score_pt.sort_values(by = 'review_score', ascending=False)
category_score_pt


# In[89]:


category_score_pt.tail()


# In[90]:


px.line(category_score_pt, x = 'product_category_name_english', y = 'review_score', 
        labels={'product_category_name_english' : '카테고리', 'review_score' : '평균 평점'}, 
        title='카테고리별 평균 평점')


# 다음 그래프는 카테고리별 평균 평점을 시각화한 그래프로 가장 평점이 높은 카테고리 5개는 'cds_dvds_musicals', 'books_general_interest', 'costruction_tools_tools', 'books_technical', 'flowers'이고, 가장 평점이 낮은 카테고리 5개는 'security_and_services', 'office_furniture', 'fashion_male_clothing', 'fashion_female_clothing', 'diapers_and_hygiene' 이다.

# ### 제품의 사진 수별 주문 건수

# In[91]:


order_photos_df = olist_df[['order_id', 'product_photos_qty']]
order_photos_df


# In[92]:


order_photos_pt = pd.pivot_table(data = order_photos_df, 
                                 index='product_photos_qty', 
                                 values='order_id', 
                                 aggfunc='count').reset_index()
order_photos_pt


# In[93]:


px.bar(order_photos_pt, x = 'product_photos_qty', y = 'order_id', 
       color = ["rgb(239,209,159)", "rgb(255,185,144)", "rgb(255,190,159)", "rgb(255,163,139)", "rgb(255,179,171)", 
                "rgb(255,177,187)", "rgb(255,163,181)", "rgb(252,175,192)", "rgb(250,187,203)", "rgb(248,163,188)", 
                "rgb(239,209,159)", "rgb(255,185,144)", "rgb(255,190,159)", "rgb(255,163,139)", "rgb(255,179,171)", 
                "rgb(239,209,159)", "rgb(255,185,144)", "rgb(255,190,159)", "rgb(255,163,139)"],
       color_discrete_map="identity", labels={'product_photos_qty' : '제품 사진 수', 'order_id' : '주문 건수'}, 
       title='제품 사진 수별 주문 건수')


# 다음 그래프는 제품을 보여주는 사진 수별 주문 건수를 나타낸 그래프로 사진 수가 적을수록 주문 건수가 많은 것으로 보이는 데, 이는 대부분의 제품이 제품을 보여주는 사진을 적게 올리기 때문이다. 따라서 제품을 보여주는 사진 수와 주문 건수에 대해서는 관련이 없어보인다.

# ### 제품 설명 길이별 주문 건수

# In[94]:


order_description_df = olist_df[['order_id', 'product_description_lenght']]
order_description_df


# In[95]:


description_length_dic = {1:'0~500자', 2:'500~1000자', 3:'1000~1500자', 4:'1500자~2000자', 5:'2000자 이상'}

description_length_list = []
for length in order_description_df['product_description_lenght'] :
    if 0 <= length < 500 :
        description_length_list.append(1)
    elif 500 <= length < 1000 :
        description_length_list.append(2)
    elif 1000 <= length < 1500 :
        description_length_list.append(3)
    elif 1500 <= length < 2000 :
        description_length_list.append(4)
    else :
        description_length_list.append(5)
        
description_length_list


# In[96]:


order_description_df['length_legend'] = description_length_list
order_description_df


# In[97]:


order_description_pt = pd.pivot_table(data = order_description_df, 
                                      index='length_legend', 
                                      values = 'order_id', 
                                      aggfunc='count').reset_index()
order_description_pt


# In[98]:


order_description_pt['length_legend'] = description_length_dic.values()
order_description_pt


# In[99]:


px.bar(order_description_pt, x = 'length_legend', y='order_id', 
       labels = {'length_legend':'설명 길이', 'order_id':'주문 건수'}, 
       title = '제품 설명 길이별 주문 건수', color = ["rgb(239,209,159)", "rgb(255,185,144)", "rgb(255,190,159)", "rgb(255,163,139)", "rgb(255,179,171)"], 
       color_discrete_map='identity')


# 다음 그래프는 제품을 설명하는 글자 수별 주문 건수를 나타낸 그래프로 역시 제품의 설명을 적게 적은 제품이 많기 때문에 제품의 설명하는 글자 수와 주문 건수와는 연관성이 없을 것 같다.

# # 분석

# In[100]:


# 취소된 주문 행 삭제 및 인덱스 초기화
mask_delivered = (olist_df['order_status'] == 'delivered')
olist_df = olist_df[mask_delivered].reset_index().drop(columns = {'index'})


# ### 배송이 20일 이상 걸린 구매자와 판매자의 위치 중앙값 표시

# In[101]:


# 특정 컬럼만 추출
geo_seller_customer_df = olist_df[['customer_id', 'seller_id', 'order_approved_at', 'order_delivered_customer_date', 'customer_zip_code_prefix', 'seller_zip_code_prefix']]
geo_seller_customer_df


# In[102]:


geo_df = geolocation_df[['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng']]
geo_df = geo_df.rename(columns = {'geolocation_zip_code_prefix' : 'zip_code_prefix'})
geo_df


# In[103]:


# 중복행 제거
geo_df = geo_df[~geo_df.duplicated(['zip_code_prefix'])]
# 인덱스 초기화
geo_df = geo_df.reset_index().drop(columns = {'index'})
geo_df


# In[105]:


# 데이터 형변환
geo_seller_customer_df['order_approved_at'] = pd.to_datetime(geo_seller_customer_df['order_approved_at'])
geo_seller_customer_df['order_delivered_customer_date'] = pd.to_datetime(geo_seller_customer_df['order_delivered_customer_date'])
geo_seller_customer_df


# In[106]:


# 실제 배송까지 걸린 날짜 계산
geo_seller_customer_df['delivery_date'] = (geo_seller_customer_df['order_delivered_customer_date'] - geo_seller_customer_df['order_approved_at']).dt.days
geo_seller_customer_df


# In[107]:


# 배송일이 20일 이상 걸린 값만 추출하기 위해 필터 생성
mask_delivery = (geo_seller_customer_df['delivery_date'] >= 20) == True


# In[108]:


# 배송일이 20일 이상 걸린 데이터와 그렇지 않은 데이터 분리
geo_seller_customer_df_20 = geo_seller_customer_df[mask_delivery]
geo_seller_customer_df_0 = geo_seller_customer_df[~mask_delivery]
geo_seller_customer_df_0


# In[109]:


# 인덱스 초기화
geo_seller_customer_df_20 = geo_seller_customer_df_20.reset_index()
geo_seller_customer_df_20 = geo_seller_customer_df_20.drop(columns = {'index', 'order_approved_at', 'order_delivered_customer_date'})
geo_seller_customer_df_0 = geo_seller_customer_df_0.reset_index()
geo_seller_customer_df_0 = geo_seller_customer_df_0.drop(columns = {'index', 'order_approved_at', 'order_delivered_customer_date'})
geo_seller_customer_df_0


# In[110]:


geo_df = geo_df.rename(columns = {'zip_code_prefix' : 'customer_zip_code_prefix'})
geo_df


# In[111]:


# geo 데이터셋과 join하여 구매자의 위도, 경도 값 불러오기 
geo_seller_customer_df_20 = geo_seller_customer_df_20.merge(geo_df, how = 'inner', on = 'customer_zip_code_prefix')
geo_seller_customer_df_0 = geo_seller_customer_df_0.merge(geo_df, how = 'inner', on = 'customer_zip_code_prefix')
geo_seller_customer_df_0


# In[112]:


geo_df = geo_df.rename(columns = {'customer_zip_code_prefix' : 'seller_zip_code_prefix'})
geo_df


# In[113]:


# geo 데이터셋과 join하여 판매자의 위도, 경도 값 불러오기 
geo_seller_customer_df_20 = geo_seller_customer_df_20.merge(geo_df, how = 'inner', on = 'seller_zip_code_prefix')
geo_seller_customer_df_0 = geo_seller_customer_df_0.merge(geo_df, how = 'inner', on = 'seller_zip_code_prefix')


# In[114]:


# 컬럼명 변경
geo_seller_customer_df_20 = geo_seller_customer_df_20.rename(columns = {'geolocation_lat_x' : 'customer_lat', 'geolocation_lng_x' : 'customer_lng', 
                                                                  'geolocation_lat_y' : 'seller_lat', 'geolocation_lng_y' : 'seller_lng'})
geo_seller_customer_df_0 = geo_seller_customer_df_0.rename(columns = {'geolocation_lat_x' : 'customer_lat', 'geolocation_lng_x' : 'customer_lng', 
                                                                  'geolocation_lat_y' : 'seller_lat', 'geolocation_lng_y' : 'seller_lng'})


# In[115]:


# 구매자와 판매자의 위치 중앙값 계산
geo_seller_customer_df_20['middle_location_lat'] = (geo_seller_customer_df_20['customer_lat'] + geo_seller_customer_df_20['seller_lat']) / 2
geo_seller_customer_df_20['middle_location_lng'] = (geo_seller_customer_df_20['customer_lng'] + geo_seller_customer_df_20['seller_lng']) / 2
geo_seller_customer_df_20


# In[116]:


geo_seller_customer_df_20.info()


# In[117]:


# pax의 허브 위치
pax_hub_loc = ['CAJAZEIRAS', 'CAMAÇARI', 'LAURO DE FREITAS', 'PARIPE', 'SALVADOR', 'SUSSUARANA', 'CARIACICA', 'SERRA', 'VILA VELHA', 'VITORIA', 'BELO HORIZONTE', 'BETIM', 'CLAUDIO', 'CONTAGEM', 'ESMERALDAS', 'NOVA LIMA', 'SANTA LUZIA', 'ARAPONGAS', 'ARAUCARIA', 'CAMPINA GRANDE DO SUL', 'CAMPO LARGO', 'COLOMBO', 'CURITIBA', 'IBIPORÃ', 'LONDRINA', 'MARINGÁ', 'PINHAIS', 'QUATRO BARRAS', 'ROLÂNDIA', 'SÃO JOSÉ DOS PINHAIS', 'BELFORD ROXO', 'DUQUE DE CAXIAS', 'ITABORAI', 'MAGÉ', 'MARICA', 'MESQUITA', 'NILOPOLIS', 'NITERÓI', 'NOVA IGUAÇU', 'PETRÓPOLIS', 'RIO DE JANEIRO', 'SÃO GONÇALO', 'TERESÓPOLIS', 'ALVORADA', 'CACHOEIRINHA', 'CANOAS', 'ESTEIO', 'GRAVATAI', 'NOVO HAMBURGO', 'PORTO ALEGRE', 'SÃO LEOPOLDO', 'VIAMÃO', 'ARAQUARI', 'BALNEARIO CAMBURIU', 'BIGUAÇU', 'BLUMENAU', 'BRUSQUE', 'CAMBORIU', 'FLORIANOPOLIS', 'INDAIAL', 'ITAJAI', 'ITAPEMA', 'JARAGUA DO SUL', 'JOINVILLE', 'PALHOÇA', 'PAULO LOPES', 'PORTO BELO', 'SÃO JOSÉ', 'TIJUCAS', 'TIMBÓ', 'ABC', 'AGUAS DE LINDÓIA', 'AGUAS DE SÃO PEDRO', 'AMERICANA', 'AMPARO', 'ARAÇARIGUAMA', 'ARAÇATUBA', 'ARAÇOIABA DA SERRA', 'ARARAQUARA', 'ARARAS', 'ATIBAIA', 'AURIFLAMA', 'BAURU', 'BIRIGUI', 'BRAGANÇA PAULISTA', 'CAMPINAS', 'CAPIVARI', 'FRANCA', 'GRANDE SP CENTRO', 'GRANDE SP EXTREMO LESTE', 'GRANDE SP ZONA LESTE', 'GRANDE SP ZONA NORTE', 'GRANDE SP ZONA OESTE', 'GRANDE SP ZONA SUL', 'GUARUJÁ', 'GUARULHOS', 'HOLAMBRA', 'HORTOLÂNDIA', 'IBITINGA', 'INDAITUBA', 'ITATIBA', 'ITU', 'ITUPEVA', 'JACAREI', 'JAGUARIUNA', 'JUNDÍAI', 'LEME', 'LIMEIRA', 'MIRASSOL', 'MOGI GUAÇU', 'MOGI MIRIM', 'NOVA ODESSA', 'PAULINIA', 'PEDREIRA', 'PIRACICABA', 'PRAIA GRANDE', 'RIBEIRÃO PRETO', 'RIO CLARO', 'SALTO', 'SALTO DE PIRAPORA', 'SANTA BARBARÁ D`OESTE', 'SANTOS', 'SÃO CARLOS', 'SÃO JOSÉ DO RIO PRETO', 'SÃO JOSÉ DOS CAMPOS', 'SÃO PEDRO', 'SÃO VICENTE', 'SERRA NEGRA', 'SOCORRO', 'SOROCABA', 'SUMARÉ', 'TAUBATÉ', 'TREMEMBÉ', 'VALINHOS', 'VARZEA PAULISTA', 'VINHEDO', 'VOTORANTIM']
pax_hub_lat = [-22.970335218409375, -12.70666869753941, -12.898049184832574, -12.824798277138134, -12.95359198623381, -12.932202708510019, -20.264446592806486, -20.128232378329855, -20.352596622065178, -20.31020129868826, -19.91980569261237, -19.961403132172737, -20.44198210753781, -19.93638408401379, -19.781156593290042, -20.055281794523097, -19.775071894193363, -23.405946654405213, -25.575896300684146, -25.36101591363883, -25.461461057554537, -25.367771856859296, -25.44357806334101, -23.273871470422893, -23.31732223397535, -23.420332956050064, -25.442954072726472, -25.370971103898906, -23.31510595336214, -25.512965311887516, -22.72908001006993, -22.66930680089637, -22.741962957226576, -22.652769459413502, -22.92170357326002, -22.784024988167708, -22.80942366198844, -22.9100731584514, -22.748566391559805, -22.50895122428255, -22.898233240848864, -22.829183663800162, -22.41772108969229, -30.01853342197006, -29.934416458444044, -29.91154808243195, -29.85003578841549, -29.935833418463805, -29.689757372108005, -30.051132411298415, -29.765077541474756, -30.07255656281994, -26.37551507326834, -26.998221274748577, -27.504295545813086, -26.907759869041197, -27.101591035676037, -27.02407832457899, -27.596767354648925, -26.906417529047168, -26.908982525974384, -27.09234525530705, -26.487862870686527, -26.30026037003235, -27.65366759999554, -27.964166079583112, -27.15583050399459, -27.5968475197764, -27.237527241478045, -26.824601631365585, -23.48241065314698, -22.4803383505265, -22.60017694096736, -22.737182855930975, -22.703874563544037, -23.434812775192928, -21.205488017982983, -23.50795658807933, -21.778658252521698, -22.363285009928315, -23.12147268234561, -20.68381384008095, -22.32277623204647, -21.290929412680807, -22.947052608103448, -22.913574346726705, -22.99533452091998, -20.534528190551864, -24.007613472503987, -23.53351935899565, -23.520644121750614, -23.4806724600753, -23.576544433067653, -23.65318263444507, -23.990390658551174, -23.457646949312593, -22.628671821163298, -22.885722544193978, -21.7562740620215, -23.100557395015986, -23.00184437516689, -23.26528547635812, -23.15442688152421, -23.301809004658296, -22.689699891151314, -23.170109430940435, -22.184906416837787, -22.56643203535106, -20.813835862143037, -22.354028349621476, -22.432121633471134, -22.78819150113137, -22.767957217267796, -22.73654347897486, -22.725698397285566, -24.027533818628715, -21.172569307591417, -22.394062302750093, -23.18459475393135, -23.64965322996743, -22.751730614998927, -23.94886997161969, -22.013601248101846, -20.807166618304556, -23.221986088696188, -22.551054933631207, -23.955588831054275, -22.61444806611925, -22.590714481297915, -23.473464557641407, -22.82418854366856, -23.024342750882916, -22.96907304762552, -22.9825502360054, -23.21415497034185, -23.037985204564905, -23.539657585753574]
pax_hub_lng = [-46.996773288976065, -38.32825372381056, -38.303720973745186, -38.47170387155965 ,-38.464362925373166, -38.4445461790032, -40.420390791149785, -40.30844987551427, -40.3085868385769, -40.30596055498719, -43.93796089224067, -44.201595512518274, -44.76999610942155, -44.05222288984372, -44.15704607062486, -43.91522866298033, -43.87377485797719, -51.44147706561292, -49.39145011292083, -49.099943889642056, -49.53752385836781, -49.18515371807826, -49.27514400994387, -51.05850752411874, -51.165207058912515, -51.93593622664081, -49.17719827980482, -49.07858325424554, -51.364047011722164, -49.16029334562719, -43.375908679639636, -43.27617787007242, -42.86021517749669, -43.034045073697165, -42.821168539301624, -43.424632502374266, -43.417083133394115, -43.065734448361034, -43.45990790172098, -43.186736898418005, -43.25373411766153, -43.0483204404351, -42.979581745227364, -51.06701666227799, -51.088411897599634, -51.182444483791365, -51.16392718931037, -51.00918942289806, -51.13424687734604, -51.1922599692965, -51.151374437419385, -51.091934541599954, -48.72105366357277, -48.63346410590039, -48.65310264758068, -49.095682857199726, -48.91738901914537, -48.65114832424737, -48.53349957494475, -49.24330198638281, -48.68465889267293, -48.61517228375711, -49.08410652501424, -48.84067077591271, -48.67636082182255, -48.684403150306366, -48.574445986041226, -48.6405378381976, -48.640700384726216, -49.275104805347866, -46.58919745677903, -46.6341090101095, -47.87539448473464, -47.33609804707113, -46.774641182415344, -47.07049042249403, -50.44231263479587, -47.60180201006515, -48.17164632465582, -47.38233565279243, -46.56311412902339, -50.55608567748728, -49.07269912257158, -50.338704978708165, -46.548546156880064, -47.064493345517, -47.50865604399596, -47.399461924279166, -46.42089897617436, -46.379765671576564, -46.43740066414146, -46.65682127472775, -46.70795728856722, -46.65972524129583, -46.26170890917105, -46.52894234613105, -47.05298158369596, -47.21812799888296, -48.82849928247488, -47.216545558791566, -46.83046457543357, -47.29845097850872, -47.04793480943061, -45.97226560571564, -46.98931880249635, -46.90121091447215, -47.38590414309035, -47.405372646766864, -49.50420192050283, -46.94531854370923, -46.96307555665996, -47.30096028814883, -47.1600830564044, -46.89662539453268, -47.64003149607724, -46.49722647023753, -47.807739175812934, -47.561926780879304, -47.315726774045444, -47.57842933478814, -47.39924246862966, -46.33283095505667, -47.8986330232055, -49.37686558130122, -45.89837816831652, -47.91773092325548, -46.39910902586462, -46.71708541976795, -46.525814640212666, -47.47631347864185, -47.27143146729259, -45.563016534621454, -45.543780984853264, -47.00403816897193, -46.82823519198839, -46.98798052516761, -47.44415409075792]


# In[118]:


# 데이터프레임 형태로 변환
pax_hub_df = pd.DataFrame({'pax_hub_loc' : pax_hub_loc, 'pax_hub_lat':pax_hub_lat, 'pax_hub_lng':pax_hub_lng})
pax_hub_df


# In[119]:


import folium
import json

# 지도 생성
map = folium.Map(location=[-15.7801, -47.9292], tiles="cartodbpositron", zoom_start=4)

geo = json.load(open('./brazil_geo.json'))

# FeatureGroups 생성
customer_group = folium.FeatureGroup(name='Customer Locations')
seller_group = folium.FeatureGroup(name='Seller Locations')
middle_location_group = folium.FeatureGroup(name='Middle Locations')
pax_group = folium.FeatureGroup(name='Pax Hubs')

# 구매자 위치 표시
for index, row in geo_seller_customer_df_20.iterrows():
    customer_lat = row['customer_lat']
    customer_lng = row['customer_lng']
    folium.Circle(location=[customer_lat, customer_lng], radius=1, color = 'rgb(6, 224, 208)').add_to(customer_group)

# 판매자 위치 표시
for index, row in geo_seller_customer_df_20.iterrows():
    seller_lat = row['seller_lat']
    seller_lng = row['seller_lng']
    folium.Circle(location=[seller_lat, seller_lng], radius=1, color='rgb(255, 0, 255)').add_to(seller_group)

# 구매자와 판매자의 위치 중앙값 표시
for index, row in geo_seller_customer_df_20.iterrows():
    middle_lat = row['middle_location_lat']
    middle_lng = row['middle_location_lng']
    folium.Circle(location=[middle_lat, middle_lng], radius=1, color='rgb(0, 0, 128)').add_to(middle_location_group)

# Pax의 허브 위치 마커로 표시
for index, row in pax_hub_df.iterrows():
    pax_lat = row['pax_hub_lat']
    pax_lng = row['pax_hub_lng']
    folium.Marker(location=[pax_lat, pax_lng], icon=folium.Icon(color='beige')).add_to(pax_group)

# 각 주별 경계선 표시
folium.Choropleth(geo_data = geo, line_color='black', line_opacity = 1, fill_opacity=0).add_to(map)
    
customer_group.add_to(map)
seller_group.add_to(map)
middle_location_group.add_to(map)
pax_group.add_to(map)


# 레이어 컨트롤을 맵에 부착
folium.LayerControl().add_to(map)

map


# ### 배송시간이 20일 이상 걸린 구매자와 판매자 사이의 평균 거리 / 배송시간이 20일 미만 걸린 구매자와 판매자 사이의 평균 거리

# In[120]:


# 위도와 경도를 통해 거리(단위 : km) 구하는 함수
def haversine_distance(lat1, lon1, lat2, lon2):
    # 지구의 반지름 (평균 반지름은 약 6,371 km)
    R = 6371.0

    # 위도와 경도를 라디안으로 변환
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # 위도와 경도 간의 차이 계산
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine 공식을 사용하여 거리 계산
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

# 함수 적용
for index, row in geo_seller_customer_df_20.iterrows():
    lat1, lng1, lat2, lng2 = row['customer_lat'], row['customer_lng'], row['seller_lat'], row['seller_lng']
    distance = haversine_distance(lat1, lng1, lat2, lng2)
    # 결과를 새로운 열에 저장 (대각선에 있는 거리를 제외한 경우)
    if lat1 != lat2 and lng1 != lng2:
        geo_seller_customer_df_20.at[index,'seller_customer_distance'] = round(distance, 1)
        
for index, row in geo_seller_customer_df_0.iterrows():
    lat1, lng1, lat2, lng2 = row['customer_lat'], row['customer_lng'], row['seller_lat'], row['seller_lng']
    distance = haversine_distance(lat1, lng1, lat2, lng2)
    # 결과를 새로운 열에 저장 (대각선에 있는 거리를 제외한 경우)
    if lat1 != lat2 and lng1 != lng2:
        geo_seller_customer_df_0.at[index,'seller_customer_distance'] = round(distance, 1)


# In[121]:


# 배송이 20일 미만 걸린 구매자와 판매자의 거리 평균
x = geo_seller_customer_df_0['seller_customer_distance'].mean()


# In[122]:


# 배송이 20일 이상 걸린 구매자와 판매자의 거리 평균
y = geo_seller_customer_df_20['seller_customer_distance'].mean()


# In[123]:


distance_dif = []
distance_dif.append(x)
distance_dif.append(y)
distance_dif


# In[124]:


# 인덱스 초기화 및 컬럼명 변경
distance_dif_df = pd.DataFrame(distance_dif).reset_index().rename(columns = {'index' : '배송 시간', 0 : '평균 거리(km)'})
distance_dif_df


# In[125]:


# 데이터 변경
distance_dif_df.loc[1,'배송 시간'] = '20일 이상'
distance_dif_df.loc[0,'배송 시간'] = '20일 미만'
distance_dif_df


# In[126]:


px.bar(distance_dif_df, x = '배송 시간', y = '평균 거리(km)', color = '배송 시간')


# ### 지역별 평균 배송 시간

# In[127]:


state = ['RR', 'AP', 'AM', 'AL', 'PA', 'MA', 'SE', 'CE', 'AC', 'PB',
         'PI', 'RO', 'RN', 'BA', 'PE', 'MT', 'TO', 'ES', 'MS', 'GO', 
         'RJ', 'RS', 'SC', 'DF', 'MG', 'PR', 'SP']
avg_delivery = [29.6, 26.7, 25.9, 23.8, 23.3, 21.2, 21.1, 20.9, 20.8, 20.1, 
                19.1, 19.0, 18.9, 18.9, 18.0, 17.6, 17.3, 15.4, 15.2, 15.1, 
                14.9, 14.9, 14.5, 12.5, 11.6, 11.5, 8.3]


# In[128]:


state_delivery_df = pd.DataFrame(avg_delivery, state).reset_index()
state_delivery_df = state_delivery_df.rename(columns = {0 : 'avg_delivery', 'index' : 'state'})
state_delivery_df


# In[129]:


map_delivery = folium.Map(location=[-15.7801, -47.9292], tiles="cartodbpositron", zoom_start=4)

folium.Choropleth(
    geo_data=geo,
    name='지역별 평균 배송시간',
    data=state_delivery_df,
    columns=['state', 'avg_delivery'],
    key_on='id',
    fill_color='PuRd',
    fill_opacity=0.7,
    line_opacity=0.5
).add_to(map_delivery)

map_delivery


# ### 지역별 판매자 수

# In[130]:


state = ['RR', 'AP', 'AM', 'AL', 'PA', 'MA', 'SE', 'CE', 'AC', 'PB',
         'PI', 'RO', 'RN', 'BA', 'PE', 'MT', 'TO', 'ES', 'MS', 'GO', 
         'RJ', 'RS', 'SC', 'DF', 'MG', 'PR', 'SP']
count_seller = [0, 0, 1, 0, 0, 1, 2, 13, 1, 6, 1, 2, 5, 20, 9, 4, 0, 24, 5, 37, 175, 130, 193, 29, 241, 354, 1774]


# In[131]:


count_seller_df = pd.DataFrame(count_seller, state).reset_index()
count_seller_df = count_seller_df.rename(columns = {0 : 'count_seller', 'index' : 'state'})
count_seller_df


# In[132]:


map_seller = folium.Map(location=[-15.7801, -47.9292], tiles="cartodbpositron", zoom_start=4)

folium.Choropleth(
        geo_data=geo,
        name='지역별 평균 배송시간',
        data=count_seller_df,
        columns=['state', 'count_seller'],
        key_on='id',
        fill_color='PuRd',
        fill_opacity=0.7,
        line_opacity=0.5,
).add_to(map_seller)

map_seller


# ### 지역별 선호 카테고리 조사

# In[133]:


customer_favorite_category_df = pd.read_excel('./customer_favorite_category.xlsx')
customer_favorite_category_df


# In[134]:


# 고객 주에 따른 지역 컬럼 추가
for index, row in customer_favorite_category_df.iterrows():
    state = row['customer_state']
    region = get_region(state)
    customer_favorite_category_df.at[index,'region'] = region
    
customer_favorite_category_df


# In[135]:


# 주의 한글 이름 컬럼 추가
for index, row in customer_favorite_category_df.iterrows():
    state = row['customer_state']
    kor_name = get_kor_state(state)
    customer_favorite_category_df.at[index,'kor_state'] = kor_name
customer_favorite_category_df


# In[136]:


# 각 지역별로 필터 생성
mask_region_southeast = (customer_favorite_category_df['region'] == '남동부')
mask_region_south = (customer_favorite_category_df['region'] == '남부')
mask_region_north = (customer_favorite_category_df['region'] == '북부')
mask_region_northeast = (customer_favorite_category_df['region'] == '북동부')
mask_region_middlewest = (customer_favorite_category_df['region'] == '중서부')

# 각 지역별로 데이터 프레임을 나누기
customer_favorite_category_southeast_df = customer_favorite_category_df[mask_region_southeast]
customer_favorite_category_south_df = customer_favorite_category_df[mask_region_south]
customer_favorite_category_north_df = customer_favorite_category_df[mask_region_north]
customer_favorite_category_northeast_df = customer_favorite_category_df[mask_region_northeast]
customer_favorite_category_middlewest_df = customer_favorite_category_df[mask_region_middlewest]

# 남동부와 남부는 같이 보기위해 합침
customer_favorite_category_southeast_df = pd.concat([customer_favorite_category_southeast_df, customer_favorite_category_south_df])
customer_favorite_category_southeast_df


# ### 남동부, 남부 지역 선호 카테고리

# In[137]:


fig = px.bar(customer_favorite_category_southeast_df, 
       x = 'kor_state', y = 'count(*)', color = 'product_category_name_english', 
       barmode='group', labels={'count(*)' : '구매량', 'kor_state' : '주'}, text_auto=True)
fig.update_traces(textfont_size=12,textfont_color='black',textfont_family = "Times", textangle=0, textposition="outside")
fig.show()


# ### 남부 지역 선호 카테고리

# In[138]:


fig = px.bar(customer_favorite_category_south_df, 
       x = 'kor_state', y = 'count(*)', color = 'product_category_name_english', 
       barmode='group', labels={'count(*)' : '구매량', 'kor_state' : '주'}, text_auto=True)
fig.update_traces(textfont_size=12,textfont_color='black',textfont_family = "Times", textangle=0, textposition="outside")
fig.show()


# ### 북부 지역 선호 카테고리

# In[139]:


fig = px.bar(customer_favorite_category_north_df, 
       x = 'kor_state', y = 'count(*)', color = 'product_category_name_english', 
       barmode='group', labels={'count(*)' : '구매량', 'kor_state' : '주'}, text_auto=True)
fig.update_traces(textfont_size=12,textfont_color='black',textfont_family = "Times", textangle=0, textposition="outside")
fig.show()


# ### 북동부 지역 선호 카테고리

# In[140]:


fig = px.bar(customer_favorite_category_northeast_df, 
       x = 'kor_state', y = 'count(*)', color = 'product_category_name_english', 
       barmode='group', labels={'count(*)' : '구매량', 'kor_state' : '주'}, text_auto=True)
fig.update_traces(textfont_size=12,textfont_color='black',textfont_family = "Times", textangle=0, textposition="outside")
fig.show()


# ### 중서부 지역 선호 카테고리

# In[141]:


fig = px.bar(customer_favorite_category_middlewest_df, 
       x = 'kor_state', y = 'count(*)', color = 'product_category_name_english', 
       barmode='group', labels={'count(*)' : '구매량', 'kor_state' : '주'}, text_auto=True)
fig.update_traces(textfont_size=12,textfont_color='black',textfont_family = "Times", textangle=0, textposition="outside")
fig.show()


# ### 지역별 평균 지출 금액

# In[142]:


# 특정 컬럼만 추출
state_payment_df = olist_df[['customer_state', 'payment_value']]
state_payment_df


# In[143]:


state_payment_pt = pd.pivot_table(data = state_payment_df, 
                                  values = 'payment_value', index = 'customer_state', aggfunc='mean')
state_payment_pt = state_payment_pt.reset_index()
state_payment_pt


# In[144]:


map_payment_value = folium.Map(location=[-15.7801, -47.9292], tiles="cartodbpositron", zoom_start=4)

folium.Choropleth(
        geo_data=geo,
        data=state_payment_pt,
        columns=['customer_state', 'payment_value'],
        key_on='id',
        fill_color='PuRd',
        fill_opacity=0.7,
        line_opacity=0.5,
).add_to(map_payment_value)

map_payment_value


# ### 지역별 평균 운임료

# In[145]:


# 구매자 주와 배송비 컬럼만 추출
state_freight_value_df = olist_df[['customer_state', 'freight_value']]
state_freight_value_df


# In[146]:


# 구매자 주별로 평균 운임료 피벗테이블 생성
state_freight_value_pt = pd.pivot_table(data = state_freight_value_df,
                                        values = 'freight_value', 
                                        index = 'customer_state', 
                                        aggfunc='mean')
state_freight_value_pt = state_freight_value_pt.reset_index()
state_freight_value_pt


# In[147]:


map_freight_value = folium.Map(location=[-15.7801, -47.9292], tiles="cartodbpositron", zoom_start=4)

folium.Choropleth(
        geo_data=geo,
        data=state_freight_value_pt,
        columns=['customer_state', 'freight_value'],
        key_on='id',
        fill_color='PuRd',
        fill_opacity=0.7,
        line_opacity=0.5,
).add_to(map_freight_value)

map_freight_value


# ### 판매자의 지역별로 주별 평균 배송비 시각화

# #### 판매자가 남동부, 남부 일때

# In[148]:


mask_southeast = (olist_df['seller_region'] == '남동부')
mask_south = (olist_df['seller_region'] == '남부')
olist_southeast = olist_df[mask_southeast]
olist_south = olist_df[mask_south]
olist_south_east = pd.concat([olist_southeast, olist_south])
olist_south_east


# In[149]:


olist_south_east_pt = pd.pivot_table(data = olist_south_east, 
                                     index = 'customer_state', 
                                     values = 'freight_value', 
                                     aggfunc='mean').reset_index()
olist_south_east_pt


# In[150]:


map_south_east = folium.Map(location=[-15.7801, -47.9292], tiles="cartodbpositron", zoom_start=4)

folium.Choropleth(
    geo_data=geo,
    name='남부, 남동부 판매자일 때 지역별 평균 운임료',
    data=olist_south_east_pt,
    columns=['customer_state', 'freight_value'],
    key_on='id',
    fill_color='PuRd',
    fill_opacity=0.7,
    line_opacity=0.5
).add_to(map_south_east)

map_south_east


# #### 판매자가 북동부 일때

# In[151]:


mask_northeast = (olist_df['seller_region'] == '북동부')
olist_northeast = olist_df[mask_northeast]
olist_northeast


# In[152]:


olist_northeast_pt = pd.pivot_table(data = olist_northeast, 
                                     index = 'customer_state', 
                                     values = 'freight_value', 
                                     aggfunc='mean').reset_index()
olist_northeast_pt


# In[153]:


map_northeast = folium.Map(location=[-15.7801, -47.9292], tiles="cartodbpositron", zoom_start=4)

folium.Choropleth(
    geo_data=geo,
    name='북동부 판매자일 때 지역별 평균 운임료',
    data=olist_northeast_pt,
    columns=['customer_state', 'freight_value'],
    key_on='id',
    fill_color='PuRd',
    fill_opacity=0.7,
    line_opacity=0.5
).add_to(map_northeast)

map_northeast


# #### 판매자가 북부일 때

# In[154]:


mask_north = (olist_df['seller_region'] == '북부')
olist_north = olist_df[mask_north]
olist_north


# In[155]:


olist_north_pt = pd.pivot_table(data = olist_north, 
                                     index = 'customer_state', 
                                     values = 'freight_value', 
                                     aggfunc='mean').reset_index()
olist_north_pt


# In[156]:


map_north = folium.Map(location=[-15.7801, -47.9292], tiles="cartodbpositron", zoom_start=4)

folium.Choropleth(
    geo_data=geo,
    name='북부 판매자일 때 지역별 평균 운임료',
    data=olist_north_pt,
    columns=['customer_state', 'freight_value'],
    key_on='id',
    fill_color='PuRd',
    fill_opacity=0.7,
    line_opacity=0.5
).add_to(map_north)

map_north


# #### 판매자가 중서부 일때

# In[157]:


mask_middlewest = (olist_df['seller_region'] == '중서부')
olist_middlewest = olist_df[mask_middlewest]
olist_middlewest


# In[158]:


olist_middlewest_pt = pd.pivot_table(data = olist_middlewest, 
                                     index = 'customer_state', 
                                     values = 'freight_value', 
                                     aggfunc='mean').reset_index()
olist_middlewest_pt


# In[159]:


map_middlewest = folium.Map(location=[-15.7801, -47.9292], tiles="cartodbpositron", zoom_start=4)

folium.Choropleth(
    geo_data=geo,
    name='중서부 판매자일 때 지역별 평균 운임료',
    data=olist_middlewest_pt,
    columns=['customer_state', 'freight_value'],
    key_on='id',
    fill_color='PuRd',
    fill_opacity=0.7,
    line_opacity=0.5
).add_to(map_middlewest)

map_middlewest


# ### 같은 주에서의 배송 / 다른 주로의 배송 배송비 차이

# In[160]:


mask_same = (olist_df['seller_state'] == olist_df['customer_state'])
cus_sell_same = olist_df[mask_same].reset_index()
cus_sell_dif = olist_df[~mask_same].reset_index()
cus_sell_same['state'] = '같은 주로 배송'
cus_sell_dif['state'] = '다른 주로 배송'
cus_sell_same


# In[161]:


cus_sell_same = cus_sell_same[['freight_value', 'state']]
cus_sell_dif = cus_sell_dif[['freight_value', 'state']]
cus_sell_dif['freight_value'].mean()


# In[162]:


cus_sell_same['freight_value'].mean()


# In[163]:


cus_sell_df = pd.concat([cus_sell_same, cus_sell_dif])
cus_sell_df


# In[164]:


cus_sell_df = cus_sell_df.reset_index().drop(columns = 'index')
cus_sell_df


# In[165]:


px.histogram(cus_sell_df, x = 'freight_value', color = 'state')

