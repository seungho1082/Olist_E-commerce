use olist_ecommerce;
select count(*) from olist_orders_dataset;

/*
■■ step1. 테이블간 관계 설정 ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
각 테이블의 컬럼에 기본키, 외래키, on delete cascade 설정
*/
-- 컬럼 확인
desc olist_customers_dataset;
desc olist_geolocation_dataset;
desc olist_order_items_dataset;
desc olist_order_payments_dataset;
desc olist_order_reviews_dataset;
desc olist_orders_dataset;
desc olist_products_dataset;
desc olist_sellers_dataset;
desc product_category_name_translation;

-- 제약조건 추가 
-- 고객 테이블
alter table olist_customers_dataset add primary key (customer_id);
-- 판매자 테이블
alter table olist_sellers_dataset add primary key (seller_id);
-- 주문 테이블
alter table olist_orders_dataset add primary key (order_id);
alter table olist_orders_dataset add FOREIGN KEY (customer_id) references olist_customers_dataset(customer_id);
-- 결제 테이블
alter table olist_order_payments_dataset add foreign key (order_id) references olist_orders_dataset(order_id) on delete cascade;
-- 리뷰 테이블 
-- alter table olist_order_reviews_dataset add primary key (review_id); -- 실패
select count(*) from olist_order_reviews_dataset group by review_id; -- 중복값 존재(17개 리뷰 아이디가 2개씩 존재)

alter table olist_order_reviews_dataset add foreign key (order_id) references olist_orders_dataset(order_id) on delete cascade;
--  제품 테이블
alter table olist_products_dataset add primary key(product_id);
-- 물품주문 테이블
-- alter table olist_order_items_dataset add primary key(order_item_id); -- 실패
select count(*) from olist_order_items_dataset GROUP BY order_item_id; -- 중복값 존재 
alter table olist_order_items_dataset add foreign key(order_id) references olist_orders_dataset(order_id) on delete cascade;
alter table olist_order_items_dataset add foreign key(seller_id) references olist_sellers_dataset(seller_id); 
alter table olist_order_items_dataset add foreign key(product_id) references olist_products_dataset(product_id);

-- ERD다이어그램 업데이트 
/*
■■ step2. 전처리 ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

▶ olist_orders_dataset 테이블
	✔ 1-1. order_status = 'canceled' 행 삭제
	✔ 1-2. 판매 사이클에 맞지 않는 데이터 삭제 
▶ olist_order_payments_dataset 테이블
	  2-1. payment_value 이상치 제거
▶ olist_sellers_dataset 테이블
	✔ 3-1. 도시명이 아닌 행 삭제  (* olist_orders_dataset 삭제할때 해당행 정리됨)  
    ✔ 3-2. seller_state 컬럼 삭제 
▶ olist_products_dataset에 카테고리가 없는 제품 존재 (1603행)
	✔ 4-1. category is null인 주문 삭제 
 */
-- 1-1.
select * from olist_orders_dataset where order_status = 'canceled';
delete from olist_orders_dataset where order_status = 'canceled';
-- 1-2.
select * from olist_orders_dataset;
select * from olist_orders_dataset where order_approved_at > order_delivered_carrier_date;
select count(*) from olist_orders_dataset where order_approved_at > order_delivered_carrier_date; -- 1359행
delete from olist_orders_dataset where order_approved_at > order_delivered_carrier_date;
select * from olist_orders_dataset where order_delivered_carrier_date > order_delivered_customer_date;
select count(*) from olist_orders_dataset where order_delivered_carrier_date > order_delivered_customer_date ; -- 23행
delete from olist_orders_dataset where order_delivered_carrier_date > order_delivered_customer_date;

-- 3-1.
select * from olist_sellers_dataset; -- olist_orders_dataset 삭제할때 해당행 정리됨
-- 3-2.
-- alter table olist_sellers_dataset drop column seller_state; ( ◪ 팀 의견. )


-- olist_products_dataset에 카테고리가 없는 제품 존재 (총 1603행 -> 1578행, 이전 쿼리들에서 필터링 되어 수치 변경)
select * from olist_products_dataset;
select * from olist_order_items_dataset join olist_products_dataset using(product_id) where product_id in (select product_id from olist_products_dataset where product_category_name is null );
select count(*) from olist_order_items_dataset join olist_products_dataset using(product_id) where product_id in (select product_id from olist_products_dataset where product_category_name is null );
-- 1578행

select * from olist_orders_dataset where order_id in (select order_id from olist_order_items_dataset join olist_products_dataset using(product_id) where product_id in (select product_id from olist_products_dataset where product_category_name is null )
);
select count(*) from olist_orders_dataset where order_id in (select order_id from olist_order_items_dataset join olist_products_dataset using(product_id) where product_id in (select product_id from olist_products_dataset where product_category_name is null )
); -- 1426 카테고리가 없는 제품을 주문(하나의 주문에는 여러개의 물품주문이 달릴 수 있음)
/*
의문. 하나의 주문에 여러 물품 주문이 달린 경우. 
어떤 물품 주문은 카테고리명이 없어 지우려는 것이나 어떤 물품 주문은 카테고리명이 있는 것이어서 좋은 데이터도 날려버리는 건 아닐까?
1578 - 1426 = 152개.(전체 주문 건 수(99441)에 비하면 차지하는 포션이 작은 편이므로 삭제하는 것으로 결정)
*/

select count(*) from olist_orders_dataset; -- 97434
select count(*) from olist_order_items_dataset; -- 110507
delete from  olist_orders_dataset where order_id in (select order_id from olist_order_items_dataset join olist_products_dataset using(product_id) where product_id in (select product_id from olist_products_dataset where product_category_name is null )); 
-- 1426행  삭제 
select count(*) from olist_orders_dataset; -- 96008
select count(*) from olist_order_items_dataset; -- 108845 (1662개의 제품 주문이 있었음)

-- drop DATABASE olist_ecommerce;
select * from olist_order_items_dataset LIMIT 10;

-- 지역별 판매자 카테고리
SELECT 
    CN.product_category_name_english,
	SDGD.geolocation_state,
	count(DISTINCT OID.seller_id) AS count_seller
FROM olist_order_items_dataset OID
JOIN olist_products_dataset PD ON OID.product_id = PD.product_id
JOIN product_category_name_translation CN ON PD.product_category_name = CN.product_category_name
JOIN 
(SELECT SD.seller_id, SD.seller_zip_code_prefix, GD.geolocation_state
FROM olist_sellers_dataset SD
JOIN (SELECT DISTINCT geolocation_zip_code_prefix AS zip_code , geolocation_state FROM olist_geolocation_dataset) GD 
ON SD.seller_zip_code_prefix = GD.zip_code) AS SDGD ON OID.seller_id = SDGD.seller_id
WHERE SDGD.geolocation_state = 'PR'
GROUP BY SDGD.geolocation_state, CN.product_category_name_english
ORDER BY SDGD.geolocation_state, count(DISTINCT OID.seller_id) DESC;

-- 지역별 주문 횟수
SELECT CD.customer_state, count(CD.customer_id) AS count_order
FROM olist_orders_dataset OD
JOIN olist_customers_dataset CD ON OD.customer_id = CD.customer_id
-- GROUP BY CD.customer_state
ORDER BY count(CD.customer_id) DESC;

-- 주별 판매자 수
SELECT 
	SDGD.geolocation_state,
	count(DISTINCT OID.seller_id) AS count_seller
FROM olist_order_items_dataset OID
JOIN olist_products_dataset PD ON OID.product_id = PD.product_id
JOIN product_category_name_translation CN ON PD.product_category_name = CN.product_category_name
JOIN 
(SELECT SD.seller_id, SD.seller_zip_code_prefix, GD.geolocation_state
FROM olist_sellers_dataset SD
JOIN (SELECT DISTINCT geolocation_zip_code_prefix AS zip_code , geolocation_state FROM olist_geolocation_dataset) GD 
ON SD.seller_zip_code_prefix = GD.zip_code) AS SDGD ON OID.seller_id = SDGD.seller_id
GROUP BY SDGD.geolocation_state
ORDER BY count(DISTINCT OID.seller_id) DESC;

-- 지역별 평균 지출 금액
SELECT
	CD.customer_state,
	SUM(PD.payment_value) / count(CD.customer_id) AS average_value
FROM olist_orders_dataset OD
JOIN olist_customers_dataset CD ON OD.customer_id = CD.customer_id
JOIN olist_order_payments_dataset PD ON OD.order_id = PD.order_id
GROUP BY CD.customer_state
ORDER BY AVG(PD.payment_value) DESC;

-- 지역별 선호 카테고리
SELECT 
		cus.customer_state,
		(
			SELECT CNT.product_category_name_english
			FROM product_category_name_translation CNT
			JOIN olist_products_dataset PD ON PD.product_category_name = CNT.product_category_name
			JOIN olist_order_items_dataset OID ON PD.product_id = OID.product_id
			JOIN olist_orders_dataset OD ON OID.order_id = OD.order_id
			JOIN olist_customers_dataset CD ON CD.customer_id = OD.customer_id
			WHERE CD.customer_state = cus.customer_state
			GROUP BY CNT.product_category_name_english
			ORDER BY count(*) DESC
			LIMIT 1
        ) AS most_common_category,
        count(ord.order_id)
FROM olist_customers_dataset cus
JOIN olist_orders_dataset ord ON cus.customer_id = ord.customer_id
GROUP BY cus.customer_state
ORDER BY count(ord.order_id) DESC;

SELECT SDGD.geolocation_state,
count(DISTINCT OID.seller_id)
FROM olist_order_items_dataset OID
JOIN olist_products_dataset PD ON OID.product_id = PD.product_id
JOIN product_category_name_translation CN ON PD.product_category_name = CN.product_category_name
JOIN 
(SELECT SD.seller_id, SD.seller_zip_code_prefix, GD.geolocation_state
FROM olist_sellers_dataset SD
JOIN (SELECT DISTINCT geolocation_zip_code_prefix AS zip_code , geolocation_state FROM olist_geolocation_dataset) GD 
ON SD.seller_zip_code_prefix = GD.zip_code) AS SDGD ON OID.seller_id = SDGD.seller_id
WHERE CN.product_category_name_english = 'sports_leisure'
GROUP BY geolocation_state;